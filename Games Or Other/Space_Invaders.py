
import pygame
import random
import sys
import math
from array import array
from pathlib import Path

pygame.init()

# ==========================================
# SPACE INVADERS - ARCADE EDITION
# ==========================================

WIDTH, HEIGHT = 800, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE INVADERS - ARCADE EDITION")
clock = pygame.time.Clock()

# COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (80, 255, 100)
RED = (255, 75, 75)
CYAN = (70, 220, 255)
YELLOW = (255, 230, 70)
GREY = (120, 120, 120)

FONT = pygame.font.Font(None, 30)
BIG_FONT = pygame.font.Font(None, 68)
SMALL_FONT = pygame.font.Font(None, 22)

# ==========================================
# SOUND EFFECTS - GENERATED IN PYTHON
# ==========================================

sound_enabled = True
sounds = {}

try:
    pygame.mixer.init(frequency=22050, size=-16, channels=1)

    def make_tone(start_frequency, duration, volume=0.3,
                  end_frequency=None):
        sample_rate = 22050
        samples = array("h")
        count = int(sample_rate * duration)

        for i in range(count):
            progress = i / max(1, count)
            frequency = start_frequency

            if end_frequency is not None:
                frequency += (
                    end_frequency - start_frequency
                ) * progress

            envelope = 1 - progress
            wave = math.sin(
                2 * math.pi * frequency * i / sample_rate
            )

            value = int(
                wave * envelope * volume * 32767
            )

            samples.append(value)

        return pygame.mixer.Sound(buffer=samples.tobytes())

    sounds["shoot"] = make_tone(850, 0.10, 0.25, 250)
    sounds["explosion"] = make_tone(180, 0.30, 0.4, 45)
    sounds["march"] = make_tone(100, 0.12, 0.15, 70)
    sounds["star"] = make_tone(700, 0.15, 0.25, 1200)
    sounds["hit"] = make_tone(250, 0.25, 0.35, 80)

except pygame.error:
    sound_enabled = False


def play_sound(name):
    if sound_enabled and name in sounds:
        sounds[name].play()


# ==========================================
# HIGH SCORE SYSTEM
# ==========================================

HIGH_SCORE_FILE = Path("highscore.txt")


def load_high_score():
    try:
        return int(HIGH_SCORE_FILE.read_text().strip())
    except (ValueError, OSError):
        return 0


high_score = load_high_score()


def save_high_score():
    try:
        HIGH_SCORE_FILE.write_text(str(high_score))
    except OSError:
        pass


# ==========================================
# ALIEN PIXEL ART
# ==========================================

ALIEN_1 = [
    "00100100",
    "00011000",
    "00111100",
    "01111110",
    "11011011",
    "11111111",
    "10100101",
    "00100100"
]

ALIEN_1_ALT = [
    "00100100",
    "10011001",
    "10111101",
    "11111111",
    "01111110",
    "00111100",
    "01000010",
    "10000001"
]

ALIEN_2 = [
    "00011000",
    "00111100",
    "01111110",
    "11011011",
    "11111111",
    "00100100",
    "01000010",
    "10000001"
]

ALIEN_2_ALT = [
    "00011000",
    "10111101",
    "11111111",
    "11011011",
    "01111110",
    "00100100",
    "01011010",
    "10100101"
]

ALIEN_3 = [
    "00011000",
    "00111100",
    "01111110",
    "11011011",
    "11111111",
    "10100101",
    "00100100",
    "01000010"
]

ALIEN_3_ALT = [
    "00011000",
    "00111100",
    "01111110",
    "11011011",
    "11111111",
    "00111100",
    "01000010",
    "10000001"
]


def draw_sprite(surface, pattern, x, y, size, colour):
    for row, line in enumerate(pattern):
        for col, pixel in enumerate(line):
            if pixel == "1":
                pygame.draw.rect(
                    surface,
                    colour,
                    (
                        int(x + col * size),
                        int(y + row * size),
                        size,
                        size
                    )
                )


# ==========================================
# BACKGROUND
# ==========================================

background_stars = [
    (
        random.randrange(WIDTH),
        random.randrange(HEIGHT),
        random.choice([1, 1, 2])
    )
    for _ in range(100)
]


def draw_background():
    screen.fill(BLACK)

    for x, y, size in background_stars:
        pygame.draw.rect(
            screen,
            (85, 105, 100),
            (x, y, size, size)
        )


# ==========================================
# GAME CREATION
# ==========================================

def create_aliens():
    aliens = []

    for row in range(5):
        for col in range(10):

            if row == 0:
                frames = [ALIEN_1, ALIEN_1_ALT]
                colour = RED
                points = 30

            elif row <= 2:
                frames = [ALIEN_2, ALIEN_2_ALT]
                colour = CYAN
                points = 20

            else:
                frames = [ALIEN_3, ALIEN_3_ALT]
                colour = GREEN
                points = 10

            aliens.append({
                "rect": pygame.Rect(
                    100 + col * 60,
                    100 + row * 45,
                    32,
                    32
                ),
                "frames": frames,
                "colour": colour,
                "points": points
            })

    return aliens


def create_shields():
    shields = []

    for shield_x in [120, 305, 490, 675]:

        for row in range(5):
            for col in range(8):

                if row < 2 and (col < 2 or col > 5):
                    continue

                shields.append(
                    pygame.Rect(
                        shield_x + col * 6,
                        500 + row * 6,
                        6,
                        6
                    )
                )

    return shields


def reset_game():
    return {
        "player": pygame.Rect(375, 575, 50, 25),
        "aliens": create_aliens(),
        "player_bullets": [],
        "enemy_bullets": [],
        "shields": create_shields(),
        "score": 0,
        "lives": 3,
        "level": 1,
        "direction": 1,
        "alien_speed": 0.8,
        "alien_timer": 0,
        "animation_timer": 0,
        "animation_frame": 0,
        "enemy_timer": 0,
        "shoot_timer": 0,
        "player_hit_timer": 0,
        "march_timer": 0
    }


game = reset_game()
state = "menu"


# ==========================================
# DRAW PLAYER
# ==========================================

def draw_player():
    x = game["player"].x
    y = game["player"].y

    pygame.draw.rect(screen, GREEN, (x + 20, y, 10, 10))
    pygame.draw.rect(screen, GREEN, (x + 10, y + 10, 30, 8))
    pygame.draw.rect(screen, GREEN, (x, y + 18, 50, 7))


# ==========================================
# DRAW HUD
# ==========================================

def draw_hud():
    pygame.draw.rect(
        screen, (12, 25, 15),
        (0, 0, WIDTH, 55)
    )

    pygame.draw.line(
        screen, GREEN,
        (0, 55), (WIDTH, 55), 2
    )

    score = FONT.render(
        f"SCORE {game['score']}", True, WHITE
    )

    best = FONT.render(
        f"BEST {high_score}", True, YELLOW
    )

    lives = FONT.render(
        f"LIVES {game['lives']}", True, GREEN
    )

    level = FONT.render(
        f"WAVE {game['level']}", True, CYAN
    )

    screen.blit(score, (18, 16))
    screen.blit(best, (235, 16))
    screen.blit(level, (440, 16))
    screen.blit(lives, (WIDTH - 120, 16))


# ==========================================
# DRAW ALIENS
# ==========================================

def draw_aliens():
    for alien in game["aliens"]:

        frame = alien["frames"][game["animation_frame"]]

        draw_sprite(
            screen,
            frame,
            alien["rect"].x,
            alien["rect"].y,
            4,
            alien["colour"]
        )


# ==========================================
# DRAW SHIELDS
# ==========================================

def draw_shields():
    for block in game["shields"]:
        pygame.draw.rect(screen, GREEN, block)


# ==========================================
# DRAW BULLETS
# ==========================================

def draw_bullets():
    for bullet in game["player_bullets"]:
        pygame.draw.rect(screen, WHITE, bullet)

    for bullet in game["enemy_bullets"]:
        pygame.draw.rect(screen, RED, bullet)


# ==========================================
# NEXT WAVE
# ==========================================

def new_wave():
    game["level"] += 1
    game["aliens"] = create_aliens()
    game["alien_speed"] += 0.35
    game["shields"] = create_shields()
    game["player_bullets"].clear()
    game["enemy_bullets"].clear()


# ==========================================
# MENU
# ==========================================

def draw_menu():
    draw_sprite(
        screen, ALIEN_1,
        WIDTH // 2 - 32, 220, 8, RED
    )

    draw_sprite(
        screen, ALIEN_2,
        WIDTH // 2 - 32, 320, 8, CYAN
    )

    draw_sprite(
        screen, ALIEN_3,
        WIDTH // 2 - 32, 420, 8, GREEN
    )

    draw_text = BIG_FONT.render(
        "SPACE INVADERS", True, GREEN
    )

    screen.blit(
        draw_text,
        draw_text.get_rect(
            center=(WIDTH // 2, 115)
        )
    )

    message = FONT.render(
        "PRESS SPACE TO START", True, WHITE
    )

    screen.blit(
        message,
        message.get_rect(
            center=(WIDTH // 2, 525)
        )
    )

    best = SMALL_FONT.render(
        f"HIGH SCORE: {high_score}", True, YELLOW
    )

    screen.blit(
        best,
        best.get_rect(
            center=(WIDTH // 2, 565)
        )
    )

    controls = SMALL_FONT.render(
        "ARROWS: MOVE     SPACE: SHOOT",
        True, GREY
    )

    screen.blit(
        controls,
        controls.get_rect(
            center=(WIDTH // 2, 610)
        )
    )


# ==========================================
# GAME OVER
# ==========================================

def draw_game_over():
    draw_hud()

    title = BIG_FONT.render(
        "GAME OVER", True, RED
    )

    score = FONT.render(
        f"YOUR SCORE: {game['score']}", True, WHITE
    )

    best = FONT.render(
        f"HIGH SCORE: {high_score}", True, YELLOW
    )

    restart = FONT.render(
        "PRESS SPACE TO RESTART", True, GREEN
    )

    for text, y in [
        (title, 230),
        (score, 320),
        (best, 370),
        (restart, 450)
    ]:
        screen.blit(
            text,
            text.get_rect(
                center=(WIDTH // 2, y)
            )
        )


# ==========================================
# MAIN GAME LOOP
# ==========================================

running = True

while running:

    dt = clock.tick(60) / 1000

    draw_background()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_m:
                sound_enabled = not sound_enabled

            if event.key == pygame.K_SPACE:

                if state == "menu":
                    game = reset_game()
                    state = "playing"

                elif state == "game_over":
                    game = reset_game()
                    state = "playing"

                elif state == "playing":

                    if (
                        game["shoot_timer"] <= 0
                        and len(game["player_bullets"]) < 2
                    ):
                        bullet = pygame.Rect(
                            game["player"].centerx - 2,
                            game["player"].top - 15,
                            4, 15
                        )

                        game["player_bullets"].append(bullet)
                        game["shoot_timer"] = 0.3
                        play_sound("shoot")

    # ======================================
    # MENU
    # ======================================

    if state == "menu":

        draw_menu()

    # ======================================
    # PLAYING
    # ======================================

    elif state == "playing":

        player = game["player"]
        keys = pygame.key.get_pressed()

        # PLAYER MOVEMENT
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= 6

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += 6

        player.clamp_ip(
            pygame.Rect(0, 55, WIDTH, HEIGHT - 55)
        )

        # TIMERS
        game["shoot_timer"] = max(
            0, game["shoot_timer"] - dt
        )

        game["player_hit_timer"] = max(
            0, game["player_hit_timer"] - dt
        )

        game["animation_timer"] += dt

        if game["animation_timer"] >= 0.4:
            game["animation_timer"] = 0
            game["animation_frame"] = (
                1 - game["animation_frame"]
            )

        # ALIEN MOVEMENT
        move = game["alien_speed"] * dt * 60
        hit_edge = False

        for alien in game["aliens"]:

            alien["rect"].x += game["direction"] * move

            if (
                alien["rect"].right >= WIDTH - 15
                or alien["rect"].left <= 15
            ):
                hit_edge = True

        if hit_edge:

            game["direction"] *= -1

            for alien in game["aliens"]:
                alien["rect"].y += 18

            play_sound("march")

        # PLAYER BULLETS
        for bullet in game["player_bullets"][:]:

            bullet.y -= 9

            if bullet.bottom < 55:
                game["player_bullets"].remove(bullet)
                continue

            # HIT ALIENS
            for alien in game["aliens"][:]:

                if bullet.colliderect(alien["rect"]):

                    game["score"] += alien["points"]
                    game["aliens"].remove(alien)
                    game["player_bullets"].remove(bullet)

                    play_sound("explosion")

                    if game["score"] > high_score:
                        high_score = game["score"]
                        save_high_score()

                    break

            # HIT SHIELDS
            if bullet in game["player_bullets"]:

                for block in game["shields"][:]:

                    if bullet.colliderect(block):

                        game["shields"].remove(block)
                        game["player_bullets"].remove(bullet)
                        break

        # ENEMY SHOOTING
        game["enemy_timer"] += dt

        if game["enemy_timer"] >= max(
            0.35, 1.2 - game["level"] * 0.08
        ) and game["aliens"]:

            game["enemy_timer"] = 0

            shooter = random.choice(game["aliens"])

            bullet = pygame.Rect(
                shooter["rect"].centerx - 2,
                shooter["rect"].bottom,
                4, 14
            )

            game["enemy_bullets"].append(bullet)

        # ENEMY BULLET MOVEMENT
        for bullet in game["enemy_bullets"][:]:

            bullet.y += 5 + game["level"] * 0.2

            if bullet.top > HEIGHT:
                game["enemy_bullets"].remove(bullet)
                continue

            # SHIELD COLLISION
            for block in game["shields"][:]:

                if bullet.colliderect(block):

                    game["shields"].remove(block)

                    if bullet in game["enemy_bullets"]:
                        game["enemy_bullets"].remove(bullet)

                    break

            # PLAYER COLLISION
            if bullet in game["enemy_bullets"]:

                if (
                    bullet.colliderect(player)
                    and game["player_hit_timer"] <= 0
                ):

                    game["enemy_bullets"].remove(bullet)
                    game["lives"] -= 1
                    game["player_hit_timer"] = 1.2

                    play_sound("hit")

                    if game["lives"] <= 0:
                        state = "game_over"

        # ALIEN REACHES PLAYER
        for alien in game["aliens"]:

            if alien["rect"].bottom >= player.top:
                state = "game_over"

        # NEXT WAVE
        if not game["aliens"]:
            new_wave()

        # DRAW GAME
        draw_hud()
        draw_shields()
        draw_aliens()
        draw_bullets()

        # BLINK PLAYER AFTER BEING HIT
        if (
            game["player_hit_timer"] <= 0
            or int(game["player_hit_timer"] * 10) % 2 == 0
        ):
            draw_player()

        pygame.draw.line(
            screen, GREEN,
            (0, HEIGHT - 35),
            (WIDTH, HEIGHT - 35), 2
        )

        # SOUND STATUS
        sound_text = SMALL_FONT.render(
            "SOUND: ON (M)" if sound_enabled
            else "SOUND: OFF (M)",
            True, GREY
        )

        screen.blit(sound_text, (10, HEIGHT - 25))

    # ======================================
    # GAME OVER
    # ======================================

    elif state == "game_over":

        draw_game_over()

    pygame.display.flip()


save_high_score()
pygame.quit()
sys.exit()

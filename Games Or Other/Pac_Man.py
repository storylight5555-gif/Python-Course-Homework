import pygame
import random
import math
from array import array
from collections import deque
from pathlib import Path

# ============================================================
# RETRO GAMES - GAME 02: PAC-MAN
# Visual style matched to Space Invaders - Arcade Edition
# ============================================================

pygame.mixer.pre_init(frequency=22050, size=-16, channels=1)
pygame.init()

WIDTH, HEIGHT = 800, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RETRO GAMES - GAME 02: PAC-MAN")
clock = pygame.time.Clock()

# ---------------- COLOURS ----------------

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (80, 255, 100)
DARK_GREEN = (12, 25, 15)
RED = (255, 75, 75)
PINK = (255, 130, 200)
CYAN = (70, 220, 255)
ORANGE = (255, 165, 70)
YELLOW = (255, 230, 70)
BLUE = (35, 75, 255)
LIGHT_BLUE = (90, 145, 255)
GREY = (120, 120, 120)
FRIGHT_BLUE = (40, 65, 220)

FONT = pygame.font.Font(None, 30)
BIG_FONT = pygame.font.Font(None, 68)
SMALL_FONT = pygame.font.Font(None, 22)

# ---------------- GAME LAYOUT ----------------

TILE = 25
COLS = 21
ROWS = 22
MAZE_X = (WIDTH - COLS * TILE) // 2
MAZE_Y = 82
HUD_HEIGHT = 55

# # = wall, . = pellet, o = power pellet, space = empty
MAZE_TEMPLATE = [
    "#####################",
    "#.........#.........#",
    "#.###.###.#.###.###.#",
    "#o###.###.#.###.###o#",
    "#...................#",
    "#.###.#.#####.#.###.#",
    "#.....#...#...#.....#",
    "#####.###.#.###.#####",
    "    #.#.......#.#    ",
    "#####.#.##.##.#.#####",
    "     ...........     ",
    "#####.#.##.##.#.#####",
    "    #.#.......#.#    ",
    "#####.#.#####.#.#####",
    "#.........#.........#",
    "#.###.###.#.###.###.#",
    "#o..#...........#..o#",
    "###.#.#.#####.#.#.###",
    "#.....#.......#.....#",
    "#.########.########.#",
    "#...................#",
    "#####################"
]

# ---------------- SOUND EFFECTS ----------------

sound_enabled = True
sounds = {}
music_channel = None


def make_tone(start_frequency, duration, volume=0.25,
              end_frequency=None):
    sample_rate = 22050
    samples = array("h")
    count = int(sample_rate * duration)

    for i in range(count):
        progress = i / max(1, count)
        frequency = start_frequency

        if end_frequency is not None:
            frequency += (end_frequency - start_frequency) * progress

        envelope = 1 - progress
        wave = math.sin(2 * math.pi * frequency * i / sample_rate)
        samples.append(int(wave * envelope * volume * 32767))

    return pygame.mixer.Sound(buffer=samples.tobytes())


def make_arcade_music():
    # Original synthesized loop, not a recording of the Pac-Man soundtrack.
    sample_rate = 22050
    notes = [523, 659, 784, 659, 587, 698, 880, 698,
             523, 659, 784, 988, 880, 784, 659, 523]
    samples = array("h")

    for frequency in notes:
        count = int(sample_rate * 0.12)
        for i in range(count):
            progress = i / count
            envelope = min(1, i / 180) * (1 - progress)
            wave = math.sin(2 * math.pi * frequency * i / sample_rate)
            samples.append(int(wave * envelope * 0.075 * 32767))

    return pygame.mixer.Sound(buffer=samples.tobytes())


try:
    pygame.mixer.init(frequency=22050, size=-16, channels=1)
    sounds["eat"] = make_tone(900, 0.055, 0.18, 650)
    sounds["power"] = make_tone(260, 0.35, 0.3, 900)
    sounds["ghost"] = make_tone(1100, 0.18, 0.3, 500)
    sounds["death"] = make_tone(400, 0.65, 0.3, 90)
    sounds["start"] = make_tone(500, 0.25, 0.2, 950)
    arcade_music = make_arcade_music()
except pygame.error:
    sound_enabled = False
    arcade_music = None


def play_sound(name):
    if sound_enabled and name in sounds:
        sounds[name].play()


def start_music():
    global music_channel
    if sound_enabled and arcade_music:
        if music_channel:
            music_channel.stop()
        music_channel = arcade_music.play(-1)


def stop_music():
    global music_channel
    if music_channel:
        music_channel.stop()
        music_channel = None


# ---------------- HIGH SCORE ----------------

HIGH_SCORE_FILE = Path("pacman_highscore.txt")


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


# ---------------- BACKGROUND ----------------

background_stars = [
    (random.randrange(WIDTH), random.randrange(HEIGHT),
     random.choice([1, 1, 2]))
    for _ in range(100)
]


def draw_background():
    screen.fill(BLACK)

    for x, y, size in background_stars:
        pygame.draw.rect(screen, (85, 105, 100), (x, y, size, size))


# ---------------- MAZE AND GAME SETUP ----------------

def build_maze():
    maze = []
    pellets = set()
    power_pellets = set()

    for y, line in enumerate(MAZE_TEMPLATE):
        row = list(line)

        for x, tile in enumerate(row):
            if tile == ".":
                pellets.add((x, y))
            elif tile == "o":
                power_pellets.add((x, y))

        maze.append(row)

    return maze, pellets, power_pellets


PLAYER_START = (10, 16)
GHOST_STARTS = [(8, 10), (9, 10), (11, 10), (12, 10)]
GHOST_COLOURS = [RED, PINK, CYAN, ORANGE]

PLAYER_STEP_MS = 155
GHOST_STEP_MS = 285
POWER_DURATION_MS = 7000


def reset_positions():
    player = list(PLAYER_START)
    ghosts = []

    for index, position in enumerate(GHOST_STARTS):
        ghosts.append({
            "pos": list(position),
            "home": list(position),
            "colour": GHOST_COLOURS[index],
            "mode": "normal",
            "release_at": index * 450
        })

    return player, ghosts


def reset_game():
    maze, pellets, power_pellets = build_maze()
    player, ghosts = reset_positions()

    return {
        "maze": maze,
        "pellets": pellets,
        "power_pellets": power_pellets,
        "player": player,
        "ghosts": ghosts,
        "direction": (0, 0),
        "next_direction": (0, 0),
        "score": 0,
        "lives": 3,
        "power_until": 0,
        "player_timer": 0,
        "ghost_timer": 0,
        "level": 1,
        "paused": False
    }


game = reset_game()
state = "menu"


# ---------------- MOVEMENT AND PATHFINDING ----------------

def can_move(x, y):
    if not (0 <= x < COLS and 0 <= y < ROWS):
        return False
    return game["maze"][y][x] != "#"


def moved_position(position, direction):
    return (
        position[0] + direction[0],
        position[1] + direction[1]
    )


def find_path(start, target):
    """Breadth-first search finds a route through the maze."""
    start = tuple(start)
    target = tuple(target)

    if start == target:
        return []

    queue = deque([(start, [])])
    visited = {start}
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    while queue:
        position, path = queue.popleft()

        for direction in directions:
            nxt = moved_position(position, direction)

            if not can_move(*nxt) or nxt in visited:
                continue

            new_path = path + [direction]

            if nxt == target:
                return new_path

            visited.add(nxt)
            queue.append((nxt, new_path))

    return []


def move_player():
    position = game["player"]
    next_direction = game["next_direction"]
    direction = game["direction"]

    # Turn as soon as the requested corridor is open.
    target = moved_position(position, next_direction)
    if can_move(*target):
        direction = next_direction

    target = moved_position(position, direction)
    if can_move(*target):
        position[0], position[1] = target

    game["direction"] = direction

    tile = tuple(position)

    if tile in game["pellets"]:
        game["pellets"].remove(tile)
        game["score"] += 10
        play_sound("eat")

    if tile in game["power_pellets"]:
        game["power_pellets"].remove(tile)
        game["score"] += 50
        game["power_until"] = pygame.time.get_ticks() + POWER_DURATION_MS
        play_sound("power")


def move_ghosts():
    now = pygame.time.get_ticks()
    frightened = now < game["power_until"]
    player_position = game["player"]

    for ghost in game["ghosts"]:
        if now < ghost["release_at"]:
            continue

        position = ghost["pos"]

        # Eaten ghosts travel back to their home tile as just eyes.
        if ghost["mode"] == "eyes":
            path = find_path(position, ghost["home"])
            if path:
                position[0], position[1] = moved_position(position, path[0])

            if position == ghost["home"]:
                ghost["mode"] = "normal"
            continue

        if frightened:
            possible = []
            for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nxt = moved_position(position, direction)
                if can_move(*nxt):
                    possible.append(direction)

            if possible:
                # Prefer moves that increase distance from Pac-Man.
                random.shuffle(possible)
                possible.sort(
                    key=lambda d: abs(position[0] + d[0] - player_position[0])
                    + abs(position[1] + d[1] - player_position[1]),
                    reverse=True
                )
                direction = possible[0]
                position[0], position[1] = moved_position(position, direction)
        else:
            path = find_path(position, player_position)
            if path:
                position[0], position[1] = moved_position(position, path[0])


# ---------------- COLLISIONS AND LIVES ----------------

def reset_after_hit():
    global state

    game["lives"] -= 1
    play_sound("death")

    if game["lives"] <= 0:
        state = "game_over"
        stop_music()
        return

    player, ghosts = reset_positions()
    game["player"] = player
    game["ghosts"] = ghosts
    game["direction"] = (0, 0)
    game["next_direction"] = (0, 0)
    game["power_until"] = 0
    game["player_timer"] = pygame.time.get_ticks()
    game["ghost_timer"] = pygame.time.get_ticks()


def check_collisions():
    now = pygame.time.get_ticks()
    frightened = now < game["power_until"]

    for ghost in game["ghosts"]:
        if ghost["mode"] == "eyes":
            continue

        if ghost["pos"] == game["player"]:
            if frightened:
                ghost["mode"] = "eyes"
                game["score"] += 200
                play_sound("ghost")
            else:
                reset_after_hit()
                return


# ---------------- DRAW HUD ----------------

def draw_hud():
    pygame.draw.rect(screen, (12, 25, 15), (0, 0, WIDTH, 55))
    pygame.draw.line(screen, GREEN, (0, 55), (WIDTH, 55), 2)

    score_text = FONT.render(f"SCORE {game['score']}", True, WHITE)
    best_text = FONT.render(f"BEST {high_score}", True, YELLOW)
    game_text = FONT.render("GAME 02", True, CYAN)
    lives_text = FONT.render(f"LIVES {game['lives']}", True, GREEN)

    screen.blit(score_text, (18, 16))
    screen.blit(best_text, (205, 16))
    screen.blit(game_text, (425, 16))
    screen.blit(lives_text, (WIDTH - 125, 16))


# ---------------- DRAW MAZE ----------------

def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            if game["maze"][y][x] == "#":
                rect = pygame.Rect(
                    MAZE_X + x * TILE + 2,
                    MAZE_Y + y * TILE + 2,
                    TILE - 4,
                    TILE - 4
                )
                pygame.draw.rect(screen, BLUE, rect, border_radius=5)
                pygame.draw.rect(screen, LIGHT_BLUE, rect, 1, border_radius=5)


def draw_pellets():
    for x, y in game["pellets"]:
        cx = MAZE_X + x * TILE + TILE // 2
        cy = MAZE_Y + y * TILE + TILE // 2
        pygame.draw.circle(screen, (255, 225, 180), (cx, cy), 3)

    pulse = 6 + int(2 * math.sin(pygame.time.get_ticks() / 140))
    for x, y in game["power_pellets"]:
        cx = MAZE_X + x * TILE + TILE // 2
        cy = MAZE_Y + y * TILE + TILE // 2
        pygame.draw.circle(screen, WHITE, (cx, cy), pulse)


# ---------------- DRAW PAC-MAN ----------------

def draw_player():
    x, y = game["player"]
    cx = MAZE_X + x * TILE + TILE // 2
    cy = MAZE_Y + y * TILE + TILE // 2

    direction_angles = {
        (1, 0): 0,
        (-1, 0): math.pi,
        (0, -1): -math.pi / 2,
        (0, 1): math.pi / 2
    }

    angle = direction_angles.get(game["direction"], 0)
    chomp = abs(math.sin(pygame.time.get_ticks() / 65)) * 0.65

    pygame.draw.circle(screen, YELLOW, (cx, cy), 11)

    mouth_points = [
        (cx, cy),
        (cx + 17 * math.cos(angle - chomp),
         cy + 17 * math.sin(angle - chomp)),
        (cx + 17 * math.cos(angle + chomp),
         cy + 17 * math.sin(angle + chomp))
    ]
    pygame.draw.polygon(screen, BLACK, mouth_points)


# ---------------- DRAW GHOSTS ----------------

def draw_ghosts():
    now = pygame.time.get_ticks()
    frightened = now < game["power_until"]

    for ghost in game["ghosts"]:
        x, y = ghost["pos"]
        cx = MAZE_X + x * TILE + TILE // 2
        cy = MAZE_Y + y * TILE + TILE // 2

        # Eaten ghost: eyes only, travelling home.
        if ghost["mode"] == "eyes":
            pygame.draw.circle(screen, WHITE, (cx - 5, cy), 5)
            pygame.draw.circle(screen, WHITE, (cx + 5, cy), 5)
            pygame.draw.circle(screen, BLUE, (cx - 4, cy), 2)
            pygame.draw.circle(screen, BLUE, (cx + 6, cy), 2)
            continue

        colour = FRIGHT_BLUE if frightened else ghost["colour"]
        if frightened and now > game["power_until"] - 1800:
            if (now // 180) % 2:
                colour = WHITE

        # Rounded ghost head and body.
        pygame.draw.circle(screen, colour, (cx, cy - 3), 10)
        pygame.draw.rect(screen, colour, (cx - 10, cy - 3, 20, 12))

        # Animated scalloped feet.
        frame = (now // 130) % 2
        if frame == 0:
            feet = [
                (cx - 10, cy + 8), (cx - 5, cy + 5),
                (cx, cy + 8), (cx + 5, cy + 5),
                (cx + 10, cy + 8)
            ]
        else:
            feet = [
                (cx - 10, cy + 5), (cx - 5, cy + 8),
                (cx, cy + 5), (cx + 5, cy + 8),
                (cx + 10, cy + 5)
            ]
        pygame.draw.polygon(screen, colour, feet)

        if frightened:
            pygame.draw.circle(screen, WHITE, (cx - 4, cy - 2), 2)
            pygame.draw.circle(screen, WHITE, (cx + 4, cy - 2), 2)
            pygame.draw.line(screen, WHITE, (cx - 5, cy + 4), (cx + 5, cy + 4), 2)
        else:
            pygame.draw.circle(screen, WHITE, (cx - 4, cy - 3), 4)
            pygame.draw.circle(screen, WHITE, (cx + 4, cy - 3), 4)
            pygame.draw.circle(screen, BLACK, (cx - 3, cy - 2), 2)
            pygame.draw.circle(screen, BLACK, (cx + 5, cy - 2), 2)


# ---------------- MENUS ----------------

def draw_centered(text, font, colour, y):
    image = font.render(text, True, colour)
    screen.blit(image, image.get_rect(center=(WIDTH // 2, y)))


def draw_menu():
    draw_centered("RETRO GAMES", BIG_FONT, GREEN, 105)
    draw_centered("GAME 02", FONT, CYAN, 165)
    draw_centered("PAC-MAN", BIG_FONT, YELLOW, 245)

    # Small Pac-Man and ghost preview.
    pygame.draw.circle(screen, YELLOW, (WIDTH // 2 - 105, 350), 23)
    pygame.draw.polygon(
        screen, BLACK,
        [(WIDTH // 2 - 105, 350),
         (WIDTH // 2 - 83, 338),
         (WIDTH // 2 - 83, 362)]
    )

    for index, colour in enumerate(GHOST_COLOURS):
        gx = WIDTH // 2 - 30 + index * 42
        gy = 350
        pygame.draw.circle(screen, colour, (gx, gy - 3), 12)
        pygame.draw.rect(screen, colour, (gx - 12, gy - 3, 24, 13))
        pygame.draw.circle(screen, WHITE, (gx - 5, gy - 4), 4)
        pygame.draw.circle(screen, WHITE, (gx + 5, gy - 4), 4)
        pygame.draw.circle(screen, BLACK, (gx - 4, gy - 4), 2)
        pygame.draw.circle(screen, BLACK, (gx + 6, gy - 4), 2)

    draw_centered("PRESS SPACE TO START", FONT, WHITE, 455)
    draw_centered(f"HIGH SCORE: {high_score}", SMALL_FONT, YELLOW, 500)
    draw_centered("ARROWS / WASD: MOVE     P: PAUSE     M: SOUND", SMALL_FONT, GREY, 555)
    draw_centered("ESC: QUIT", SMALL_FONT, GREY, 585)


def draw_game_over():
    draw_hud()
    draw_centered("GAME OVER", BIG_FONT, RED, 245)
    draw_centered(f"YOUR SCORE: {game['score']}", FONT, WHITE, 325)
    draw_centered(f"HIGH SCORE: {high_score}", FONT, YELLOW, 370)
    draw_centered("PRESS SPACE TO RESTART", FONT, GREEN, 445)


def draw_pause():
    shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    shade.fill((0, 0, 0, 175))
    screen.blit(shade, (0, 0))
    draw_centered("PAUSED", BIG_FONT, YELLOW, HEIGHT // 2 - 20)
    draw_centered("PRESS P TO CONTINUE", FONT, WHITE, HEIGHT // 2 + 35)


# ---------------- MAIN LOOP ----------------

running = True
last_player_move = 0
last_ghost_move = 0

while running:
    dt = clock.tick(60)
    now = pygame.time.get_ticks()

    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_m:
                sound_enabled = not sound_enabled
                if sound_enabled and state == "playing" and not game["paused"]:
                    start_music()
                else:
                    stop_music()

            if event.key == pygame.K_SPACE:
                if state in ("menu", "game_over"):
                    game = reset_game()
                    state = "playing"
                    last_player_move = now
                    last_ghost_move = now
                    play_sound("start")
                    start_music()

            if event.key == pygame.K_p and state == "playing":
                game["paused"] = not game["paused"]
                if game["paused"]:
                    stop_music()
                elif sound_enabled:
                    start_music()

            if state == "playing":
                if event.key in (pygame.K_UP, pygame.K_w):
                    game["next_direction"] = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    game["next_direction"] = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    game["next_direction"] = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    game["next_direction"] = (1, 0)

    if state == "menu":
        draw_menu()

    elif state == "playing":
        if not game["paused"]:
            if now - last_player_move >= PLAYER_STEP_MS:
                move_player()
                check_collisions()
                last_player_move = now

            if state == "playing" and now - last_ghost_move >= GHOST_STEP_MS:
                move_ghosts()
                check_collisions()
                last_ghost_move = now

            if game["score"] > high_score:
                high_score = game["score"]
                save_high_score()

            if not game["pellets"] and not game["power_pellets"]:
                # Start the next round with a fresh maze and a small speed increase.
                game["level"] += 1
                game["maze"], game["pellets"], game["power_pellets"] = build_maze()
                game["player"], game["ghosts"] = reset_positions()
                game["direction"] = (0, 0)
                game["next_direction"] = (0, 0)
                game["power_until"] = 0
                game["player_timer"] = 0
                game["ghost_timer"] = 0
                # Gradually increase the challenge, with a sensible speed limit.
                game["level"] = min(game["level"], 8)

        draw_hud()
        draw_maze()
        draw_pellets()
        draw_player()
        draw_ghosts()

        footer = SMALL_FONT.render(
            "ARROWS / WASD: MOVE     P: PAUSE     M: SOUND",
            True, GREY
        )
        screen.blit(footer, footer.get_rect(center=(WIDTH // 2, HEIGHT - 13)))

        if game["paused"]:
            draw_pause()

    elif state == "game_over":
        draw_game_over()

    pygame.display.flip()

save_high_score()
stop_music()
pygame.quit()

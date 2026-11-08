
import pygame
import random
import math
import os
import struct
import array

pygame.init()

# ==========================================
# TETRIS - RETRO GAMES COLLECTION
# GAME 03
# ==========================================

WIDTH = 800
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RETRO GAMES - TETRIS 03")

clock = pygame.time.Clock()

# Colours
BLACK = (3, 5, 10)
WHITE = (240, 245, 255)
GREEN = (0, 255, 120)
DARK_GREEN = (0, 100, 60)
GREY = (100, 110, 125)
CYAN = (0, 220, 255)
PURPLE = (175, 70, 255)
YELLOW = (255, 220, 40)
RED = (255, 65, 90)

# Fonts
font_small = pygame.font.SysFont("consolas", 18)
font_medium = pygame.font.SysFont("consolas", 25, bold=True)
font_large = pygame.font.SysFont("consolas", 48, bold=True)
font_title = pygame.font.SysFont("consolas", 65, bold=True)

# Game settings
COLS = 10
ROWS = 20
CELL = 26

BOARD_X = 270
BOARD_Y = 65

BOARD_WIDTH = COLS * CELL
BOARD_HEIGHT = ROWS * CELL

# High score
HIGH_SCORE_FILE = "tetris_highscore.txt"

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))
    except:
        pass

best_score = load_high_score()

# ==========================================
# SOUND EFFECTS
# ==========================================

sound_enabled = True

def make_tone(frequency, duration, volume=0.25):
    try:
        sample_rate = 22050
        samples = int(sample_rate * duration)
        wave = array.array("h")

        for i in range(samples):
            value = math.sin(
                2 * math.pi * frequency * i / sample_rate
            )
            fade = min(1, i / 200, (samples-i) / 500)
            wave.append(int(value * 32767 * volume * fade))

        return pygame.mixer.Sound(buffer=wave.tobytes())
    except:
        return None

try:
    pygame.mixer.init(frequency=22050, size=-16, channels=1)
    move_sound = make_tone(330, 0.045)
    rotate_sound = make_tone(520, 0.07)
    drop_sound = make_tone(160, 0.12)
    clear_sound = make_tone(750, 0.18)
    gameover_sound = make_tone(100, 0.5)
    level_sound = make_tone(950, 0.2)
except:
    move_sound = None
    rotate_sound = None
    drop_sound = None
    clear_sound = None
    gameover_sound = None
    level_sound = None

def play_sound(sound):
    if sound_enabled and sound:
        try:
            sound.play()
        except:
            pass

# ==========================================
# BACKGROUND
# ==========================================

stars = []

for i in range(85):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.choice([1, 1, 2])
    ])

def draw_background():
    screen.fill(BLACK)

    for star in stars:
        x, y, size = star

        pygame.draw.circle(
            screen,
            (35, 65, 75),
            (x, y),
            size
        )

        star[1] += size * 0.15

        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)

# ==========================================
# TETROMINO SHAPES
# ==========================================

SHAPES = [
    # I
    [
        "....",
        "XXXX",
        "....",
        "...."
    ],

    # O
    [
        ".XX.",
        ".XX.",
        "....",
        "...."
    ],

    # T
    [
        ".X..",
        "XXX.",
        "....",
        "...."
    ],

    # L
    [
        "..X.",
        "XXX.",
        "....",
        "...."
    ],

    # J
    [
        "X...",
        "XXX.",
        "....",
        "...."
    ],

    # S
    [
        ".XX.",
        "XX..",
        "....",
        "...."
    ],

    # Z
    [
        "XX..",
        ".XX.",
        "....",
        "...."
    ]
]

COLORS = [
    CYAN,
    YELLOW,
    PURPLE,
    (255, 150, 40),
    (70, 110, 255),
    GREEN,
    RED
]

# ==========================================
# PIECE CLASS
# ==========================================

class Piece:

    def __init__(self):
        self.shape_id = random.randrange(len(SHAPES))
        self.shape = SHAPES[self.shape_id]
        self.color = COLORS[self.shape_id]

        self.x = 3
        self.y = -1

    def blocks(self):
        result = []

        for row in range(4):
            for col in range(4):
                if self.shape[row][col] == "X":
                    result.append((
                        self.x + col,
                        self.y + row
                    ))

        return result

    def rotate(self, clockwise=True):
        matrix = [
            list(row) for row in self.shape
        ]

        if clockwise:
            rotated = [
                list(row) for row in zip(*matrix[::-1])
            ]
        else:
            rotated = [
                list(row) for row in zip(*matrix)
            ][::-1]

        self.shape = [
            "".join(row) for row in rotated
        ]

# ==========================================
# GAME CLASS
# ==========================================

class Game:

    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = [
            [None for _ in range(COLS)]
            for _ in range(ROWS)
        ]

        self.score = 0
        self.lines = 0
        self.level = 1

        self.current = Piece()
        self.next_piece = Piece()

        self.fall_timer = 0
        self.fall_speed = 650

        self.game_over = False

    def valid(self, piece):
        for x, y in piece.blocks():

            if x < 0 or x >= COLS:
                return False

            if y >= ROWS:
                return False

            if y >= 0 and self.grid[y][x] is not None:
                return False

        return True

    def lock_piece(self):

        for x, y in self.current.blocks():

            if y < 0:
                self.game_over = True
                play_sound(gameover_sound)
                return

            self.grid[y][x] = self.current.color

        self.clear_lines()

        self.current = self.next_piece
        self.next_piece = Piece()

        if not self.valid(self.current):
            self.game_over = True
            play_sound(gameover_sound)

    def clear_lines(self):

        new_grid = [
            row for row in self.grid
            if any(cell is None for cell in row)
        ]

        cleared = ROWS - len(new_grid)

        if cleared > 0:

            for i in range(cleared):
                new_grid.insert(
                    0,
                    [None for _ in range(COLS)]
                )

            self.grid = new_grid

            points = {
                1: 100,
                2: 300,
                3: 500,
                4: 800
            }

            self.score += points.get(cleared, 0) * self.level

            self.lines += cleared

            old_level = self.level

            self.level = 1 + self.lines // 10

            self.fall_speed = max(
                90,
                650 - (self.level - 1) * 50
            )

            if self.level > old_level:
                play_sound(level_sound)
            else:
                play_sound(clear_sound)

    def move(self, dx, dy):

        self.current.x += dx
        self.current.y += dy

        if not self.valid(self.current):
            self.current.x -= dx
            self.current.y -= dy
            return False

        return True

    def rotate_piece(self, clockwise=True):

        old_shape = self.current.shape

        self.current.rotate(clockwise)

        # Small wall adjustments
        if self.valid(self.current):
            play_sound(rotate_sound)
            return

        for adjustment in [-1, 1, -2, 2]:
            self.current.x += adjustment

            if self.valid(self.current):
                play_sound(rotate_sound)
                return

            self.current.x -= adjustment

        self.current.shape = old_shape

    def hard_drop(self):

        distance = 0

        while self.move(0, 1):
            distance += 1

        self.score += distance * 2

        play_sound(drop_sound)
        self.lock_piece()

    def update(self, dt):

        if self.game_over:
            return

        self.fall_timer += dt

        if self.fall_timer >= self.fall_speed:
            self.fall_timer = 0

            if not self.move(0, 1):
                self.lock_piece()

# ==========================================
# DRAWING
# ==========================================

def draw_text(text, font, color, x, y, center=False):

    image = font.render(text, True, color)

    rect = image.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(image, rect)

def draw_glow_rect(rect, color):

    glow = pygame.Surface(
        (rect.width + 12, rect.height + 12),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        glow,
        (*color, 35),
        (6, 6, rect.width, rect.height),
        border_radius=5
    )

    screen.blit(
        glow,
        (rect.x - 6, rect.y - 6)
    )

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=3
    )

def draw_block(x, y, color, size=CELL):

    rect = pygame.Rect(
        x,
        y,
        size,
        size
    )

    draw_glow_rect(rect, color)

    inner = rect.inflate(-5, -5)

    pygame.draw.rect(
        screen,
        color,
        inner,
        border_radius=2
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (inner.x + 2, inner.y + 2),
        (inner.right - 3, inner.y + 2),
        1
    )

def draw_board(game):

    board_rect = pygame.Rect(
        BOARD_X,
        BOARD_Y,
        BOARD_WIDTH,
        BOARD_HEIGHT
    )

    pygame.draw.rect(
        screen,
        (8, 13, 23),
        board_rect
    )

    pygame.draw.rect(
        screen,
        GREEN,
        board_rect,
        2
    )

    # Grid
    for row in range(ROWS):
        for col in range(COLS):

            x = BOARD_X + col * CELL
            y = BOARD_Y + row * CELL

            pygame.draw.rect(
                screen,
                (22, 32, 43),
                (x, y, CELL, CELL),
                1
            )

            color = game.grid[row][col]

            if color:
                draw_block(x, y, color)

    # Current falling piece
    if not game.game_over:

        for x, y in game.current.blocks():

            if y >= 0:
                draw_block(
                    BOARD_X + x * CELL,
                    BOARD_Y + y * CELL,
                    game.current.color
                )

    # Border
    pygame.draw.rect(
        screen,
        GREEN,
        board_rect,
        2
    )

def draw_next_piece(game):

    x_start = 610
    y_start = 250

    draw_text(
        "NEXT",
        font_medium,
        CYAN,
        x_start,
        y_start - 40
    )

    pygame.draw.rect(
        screen,
        (10, 18, 28),
        (x_start - 12, y_start, 125, 110)
    )

    pygame.draw.rect(
        screen,
        CYAN,
        (x_start - 12, y_start, 125, 110),
        1
    )

    for row in range(4):
        for col in range(4):

            if game.next_piece.shape[row][col] == "X":

                draw_block(
                    x_start + col * 23,
                    y_start + row * 23 + 5,
                    game.next_piece.color,
                    23
                )

def draw_hud(game):

    # Left side
    draw_text(
        "RETRO",
        font_medium,
        GREEN,
        45,
        35
    )

    draw_text(
        "GAME 03",
        font_small,
        GREY,
        45,
        68
    )

    draw_text(
        "TETRIS",
        font_large,
        WHITE,
        45,
        120
    )

    pygame.draw.line(
        screen,
        DARK_GREEN,
        (45, 185),
        (225, 185),
        2
    )

    draw_text(
        "SCORE",
        font_small,
        GREY,
        45,
        210
    )

    draw_text(
        str(game.score),
        font_large,
        GREEN,
        45,
        240
    )

    draw_text(
        "BEST",
        font_small,
        GREY,
        45,
        315
    )

    draw_text(
        str(max(best_score, game.score)),
        font_medium,
        YELLOW,
        45,
        342
    )

    # Right side
    draw_text(
        "LEVEL",
        font_small,
        GREY,
        610,
        65
    )

    draw_text(
        str(game.level),
        font_large,
        GREEN,
        610,
        95
    )

    draw_text(
        "LINES",
        font_small,
        GREY,
        610,
        175
    )

    draw_text(
        str(game.lines),
        font_large,
        CYAN,
        610,
        200
    )

    draw_next_piece(game)

    pygame.draw.line(
        screen,
        DARK_GREEN,
        (610, 390),
        (755, 390),
        2
    )

    draw_text(
        "CONTROLS",
        font_small,
        GREEN,
        610,
        410
    )

    draw_text(
        "ARROWS  MOVE",
        font_small,
        GREY,
        610,
        445
    )

    draw_text(
        "UP      ROTATE",
        font_small,
        GREY,
        610,
        470
    )

    draw_text(
        "SPACE   DROP",
        font_small,
        GREY,
        610,
        495
    )

    draw_text(
        "P       PAUSE",
        font_small,
        GREY,
        610,
        520
    )

    draw_text(
        "M       SOUND",
        font_small,
        GREY,
        610,
        545
    )

def draw_footer():

    pygame.draw.line(
        screen,
        DARK_GREEN,
        (45, 605),
        (755, 605),
        1
    )

    draw_text(
        "RETRO GAMES COLLECTION",
        font_small,
        GREY,
        45,
        618
    )

    draw_text(
        "03 / TETRIS",
        font_small,
        GREEN,
        755,
        618,
        center=True
    )

# ==========================================
# SCREENS
# ==========================================

def draw_menu():

    draw_text(
        "RETRO GAMES",
        font_medium,
        GREEN,
        400,
        110,
        center=True
    )

    draw_text(
        "TETRIS",
        font_title,
        WHITE,
        400,
        230,
        center=True
    )

    draw_text(
        "GAME 03",
        font_medium,
        CYAN,
        400,
        290,
        center=True
    )

    # Decorative blocks
    colors = [CYAN, PURPLE, YELLOW, RED, GREEN]

    for i, color in enumerate(colors):

        draw_block(
            290 + i * 45,
            350,
            color,
            30
        )

    draw_text(
        "PRESS ENTER TO START",
        font_medium,
        GREEN,
        400,
        455,
        center=True
    )

    draw_text(
        "ARROWS TO MOVE  |  SPACE TO DROP",
        font_small,
        GREY,
        400,
        510,
        center=True
    )

    draw_text(
        "P = PAUSE     M = SOUND     ESC = EXIT",
        font_small,
        GREY,
        400,
        540,
        center=True
    )

def draw_pause():

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    draw_text(
        "PAUSED",
        font_large,
        YELLOW,
        400,
        270,
        center=True
    )

    draw_text(
        "PRESS P TO CONTINUE",
        font_medium,
        GREEN,
        400,
        340,
        center=True
    )

def draw_game_over(game):

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    draw_text(
        "GAME OVER",
        font_large,
        RED,
        400,
        235,
        center=True
    )

    draw_text(
        "FINAL SCORE: " + str(game.score),
        font_medium,
        WHITE,
        400,
        315,
        center=True
    )

    draw_text(
        "PRESS ENTER TO RESTART",
        font_medium,
        GREEN,
        400,
        390,
        center=True
    )

# ==========================================
# MAIN GAME LOOP
# ==========================================

game = Game()

state = "menu"
running = True

paused = False

move_repeat = 0
soft_drop_timer = 0

while running:

    dt = clock.tick(60)

    draw_background()

    # --------------------------------------
    # EVENTS
    # --------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_m:
                sound_enabled = not sound_enabled

            if state == "menu":

                if event.key == pygame.K_RETURN:
                    game.reset()
                    state = "playing"

            elif state == "playing":

                if event.key == pygame.K_p:
                    paused = not paused

                if not paused and not game.game_over:

                    if event.key in (
                        pygame.K_LEFT,
                        pygame.K_a
                    ):
                        if game.move(-1, 0):
                            play_sound(move_sound)

                    elif event.key in (
                        pygame.K_RIGHT,
                        pygame.K_d
                    ):
                        if game.move(1, 0):
                            play_sound(move_sound)

                    elif event.key in (
                        pygame.K_UP,
                        pygame.K_x
                    ):
                        game.rotate_piece(True)

                    elif event.key == pygame.K_z:
                        game.rotate_piece(False)

                    elif event.key == pygame.K_SPACE:
                        game.hard_drop()

            if state == "playing" and game.game_over:

                if event.key == pygame.K_RETURN:
                    state = "menu"

    # --------------------------------------
    # GAME UPDATE
    # --------------------------------------

    if state == "playing" and not paused:

        if not game.game_over:

            game.update(dt)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_DOWN]:
                soft_drop_timer += dt

                if soft_drop_timer >= 55:

                    soft_drop_timer = 0

                    if game.move(0, 1):
                        game.score += 1
                    else:
                        game.lock_piece()

            else:
                soft_drop_timer = 0

        if game.score > best_score:
            best_score = game.score
            save_high_score(best_score)

    # --------------------------------------
    # DRAW SCREENS
    # --------------------------------------

    if state == "menu":

        draw_menu()

    elif state == "playing":

        draw_board(game)
        draw_hud(game)
        draw_footer()

        if paused:
            draw_pause()

        if game.game_over:
            draw_game_over(game)

    # --------------------------------------

    pygame.display.flip()

pygame.quit()

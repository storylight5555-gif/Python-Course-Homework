# re, and update the display:
#     a) Draw player at (playerX, playerY).
#     b) Display score using `show_score(textX, textY)`.
#     c) Refresh the screen using `pygame.display.update()`.1) Import required modules:
#    a) Import `math` to calculate distance for collision detection.
#    b) Import `random` to generate random enemy positions.
#    c) Import `pygame` to create the game window, load images, and handle events.
import math
import pygame
import random
# 2) Create constants to control game settings:
#    a) Screen size, player start position, enemy start range.
#    b) Enemy movement speed (X and Y), bullet speed, collision distance threshold.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
PLAYER_START_X = 370
PLAYER_START_Y = 380
ENEMY_START_Y_MIN = 50
ENEMY_START_Y_MAX = 150
ENEMY_SPEED_X = 1
ENEMY_SPEED_Y = 1
BULLET_SPEED_Y = 10
COLLISION_DISTANCE = 27
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
BULLET_WIDTH = 16
BULLET_HEIGHT = 32
UFO_WIDTH = 64
UFO_HEIGHT = 64

# 3) Initialize pygame using `pygame.init()`.
pygame.init()

# --- BACKGROUND MUSIC SETUP ---
# Initialize the sound mixer
pygame.mixer.init()
# Load your audio track file path
pygame.mixer.music.load("C:\\Users\\karth\\OneDrive\\Desktop\\Python Course\\Homework\\Background.mp3")
# Set default volume layout (0.0 to 1.0)
pygame.mixer.music.set_volume(0.5)
# Play track seamlessly on loop using -1
pygame.mixer.music.play(-1)
# ------------------------------

# 4) Create the game window (screen) using `pygame.display.set_mode(...)`.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# 5) Load background image using `pygame.image.load('background.png')`.
background = pygame.image.load("C:\\Users\\karth\\OneDrive\\Desktop\\Python Course\\Module4\\Lesson5\\Planet_bg.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
# 6) Set the game title and icon:
#    a) Use `pygame.display.set_caption("Space Invader")`.
pygame.display.set_caption("Space Invader")
#    b) Load icon image `ufo.png` and apply using `pygame.display.set_icon(icon)`.
icon = pygame.image.load("C:\\Users\\karth\\OneDrive\\Desktop\\Python Course\\Module4\\Lesson5\\Space_ship_1.png")
icon = pygame.transform.scale(icon, (UFO_WIDTH, UFO_HEIGHT))
pygame.display.set_icon(icon)
# 7) Setup the player:
#    a) Load the player image `player.png`.
player_img = pygame.image.load("C:\\Users\\karth\\OneDrive\\Desktop\\Python Course\\Module4\\Lesson5\\Space_ship_1.png")
player_img = pygame.transform.scale(
player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
#    b) Set initial player position using `playerX` and `playerY`.
playerX = PLAYER_START_X
playerY = PLAYER_START_Y
#    c) Create `playerX_change = 0` to control horizontal movement.
playerX_change = 0
# 8) Setup enemies using lists (multiple enemies):
#    a) Create empty lists for enemy image, x/y positions, and x/y movement changes.
enemyImg= []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
#    b) Set `num_of_enemies = 6`.
num_of_enemy = 7
# 9) Use a loop to create each enemy:
#    a) Load enemy image `enemy.png` and append it to `enemyImg`.
#    b) Set random starting X position within the screen width.
#    c) Set random starting Y position between ENEMY_START_Y_MIN and ENEMY_START_Y_MAX.
#    d) Set initial X speed (ENEMY_SPEED_X) and Y drop speed (ENEMY_SPEED_Y).
for _i in range(num_of_enemy):
    img = pygame.image.load("c:\\Users\\karth\\OneDrive\\Desktop\\Python Course\\Module4\\Lesson5\\Alien_2.png")
    img = pygame.transform.scale(img, (ENEMY_WIDTH, ENEMY_HEIGHT))
    enemyImg.append(img)
    enemyX.append(random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH))
    enemyY.append(random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))
    enemyX_change.append(ENEMY_SPEED_X)
    enemyY_change.append(ENEMY_SPEED_Y)
# 10) Setup bullet:
#     a) Load bullet image `bullet.png`.
bulletImg = pygame.image.load("C:\\Users\\karth\\OneDrive\\Desktop\\Python Course\\Module4\\Lesson5\\Bullet.png")
#     b) Set bullet starting positions and movement speed.
bulletX = 0
bulletY = PLAYER_START_Y
bulletX_change = 0
bulletY_change = BULLET_SPEED_Y
#     c) Use `bullet_state = "ready"` to track if bullet can be fired or is already moving.
bullet_state = "ready"
# 11) Setup score display:
#     a) Initialize `score_value = 0`.
score_value = 0
#     b) Load a font using `pygame.font.Font(...)`.
score_font = pygame.font.Font("freesansbold.ttf", 32)
#     c) Set score text position (textX, textY).
textX = 10
textY = 10
# 12) Setup game-over text font using a larger font size.
game_over_font = pygame.font.Font("freesansbold.ttf", 64)
# 13) Define helper functions:
#     a) `show_score(x, y)` to render and display the score on the screen.
def show_score(x, y):
    score = score_font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
#     b) `game_over_text()` to display "GAME OVER" on the screen.
def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
#     c) `player(x, y)` to draw the player image at (x, y).
def player(x, y):                 
    screen.blit(player_img, (x, y))
#     d) `enemy(x, y, i)` to draw the i-th enemy at (x, y).
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
#     e) `fire_bullet(x, y)`:
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
#        - Set `bullet_state` to "fire"
#        - Draw the bullet slightly offset from the player position.
#     f) `isCollision(enemyX, enemyY, bulletX, bulletY)`:
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return distance < COLLISION_DISTANCE
#        - Calculate distance between enemy and bullet using the distance formula.
#        - Return True if distance is less than COLLISION_DISTANCE.

# 14) Start the main game loop with `running = True`.
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
# 15) Every frame inside the loop:
#     a) Clear the screen and draw the background image.

# 16) Handle events (keyboard and quit):
#     a) If `pygame.QUIT`, stop the loop.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
#     b) If a key is pressed (`pygame.KEYDOWN`):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        
#        - LEFT arrow sets `playerX_change = -5`.
#        - RIGHT arrow sets `playerX_change = 5`.
#        - SPACE fires the bullet only if `bullet_state` is "ready":
#          i) Set `bulletX = playerX`
#          ii) Call `fire_bullet(bulletX, bulletY)`
#     c) If key is released (`pygame.KEYUP`) for LEFT/RIGHT:
#        - Set `playerX_change = 0` to stop movement.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
# 17) Update player movement:
#     a) Add `playerX_change` to `playerX`.
#     b) Clamp player position so it stays inside the screen boundaries.
    playerX += playerX_change
    playerX = max(0, min(playerX, SCREEN_WIDTH - PLAYER_WIDTH))
# 18) Update enemy movement for each enemy:
#     a) If any enemy goes below Y > 340:
#        - Move all enemies off-screen (enemyY = 2000)
#        - Display "GAME OVER"
#        - Break out of enemy loop.
    for i in range (num_of_enemy):
        if enemyY[i] > 340:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break
#     b) Move enemy horizontally using `enemyX_change[i]`.
        enemyX[i] += enemyX_change[i]
#     c) If enemy hits left/right edge:
#        - Reverse direction by multiplying speed by -1.
#        - Move enemy downward by adding `enemyY_change[i]`.
        if enemyX[i] <= 0:
            enemyX_change[i] = ENEMY_SPEED_X
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= SCREEN_WIDTH - ENEMY_WIDTH:
            enemyX_change[i] = -ENEMY_SPEED_X
            enemyY[i] += enemyY_change[i]

        # Check collision between enemy and bullet
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = PLAYER_START_Y
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
            enemyY[i] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)

        # Draw enemy
        enemy(enemyX[i], enemyY[i], i)

    # 19) Update bullet movement
    if bulletY <= 0:
        bulletY = PLAYER_START_Y
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # 20) Draw player, score, and refresh display
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

import pygame
import math
import sys

# 1. CORE ENGINE & GRAPHICS SETUP
pygame.init()
WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro 3D Raycaster Engine")
clock = pygame.time.Clock()

# Color Definitions
SKY_COLOR = (45, 45, 65)
FLOOR_COLOR = (70, 70, 70)
WALL_COLOR_LIGHT = (190, 30, 30)
HUD_PANEL = (20, 20, 25)
TEXT_GOLD = (230, 180, 50)

# 2. THE LEVEL BLUEPRINT (Grid Map Layout)
# 1-4 represent different structural walls; 0 represents walkable hallway space
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

MAP_W = len(MAP[0])
MAP_H = len(MAP)
TILE_SIZE = 64

# Camera Matrix Parameters
FOV = math.pi / 3  # 60-degree field of view field arch
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH
STEP_ANGLE = FOV / NUM_RAYS
RENDER_DISTANCE = 1200

# 3. PLAYER ENTITY TRACKING
px, py = 120.0, 120.0  # Spawning coordinates
p_angle = 0.0          # Facing direction vector angle
speed = 180.0          # Pixels per second forward velocity
rot_speed = 3.0        # Radians per second rotational velocity

# Weapon Sprite Animation State Controllers
is_shooting = False
weapon_frame = 0
weapon_cooldown = 0

def draw_weapon_sprite(surface, frame, shooting):
    """Draws a vector-constructed retro blaster gun that scales with the window."""
    wx = WIDTH // 2
    wy = HEIGHT - 40
    
    # Idle bounce displacement calculations
    bobbing = int(math.sin(pygame.time.get_ticks() * 0.005) * 4) if not shooting else 0
    wy += bobbing

    if shooting:
        # Flash frame muzzle burst indicators
        if frame == 1:
            pygame.draw.circle(surface, (255, 230, 100), (wx, wy - 110), 35)
            pygame.draw.circle(surface, (255, 100, 30), (wx, wy - 110), 20)
        wy += 15  # Recoil kick down effect vector structural frame translation

    # Left / Right dual barrel base structural assembly drawing layout
    pygame.draw.rect(surface, (30, 30, 35), (wx - 35, wy - 80, 25, 90))
    pygame.draw.rect(surface, (30, 30, 35), (wx + 10, wy - 80, 25, 90))
    # Dark central mechanisms housing block
    pygame.draw.rect(surface, (15, 15, 18), (wx - 20, wy - 60, 40, 70))
    # Double steel barrel tips
    pygame.draw.rect(surface, (70, 75, 80), (wx - 30, wy - 95, 15, 20))
    pygame.draw.rect(surface, (70, 75, 80), (wx + 15, wy - 95, 15, 20))
    # Deep core barrel exhaust cavities
    pygame.draw.circle(surface, (5, 5, 5), (wx - 23, wy - 95), 5)
    pygame.draw.circle(surface, (5, 5, 5), (wx + 22, wy - 95), 5)

def draw_minimap(surface, scale=12):
    """Renders a fully interactive top-down navigation radar widget layout."""
    for r in range(MAP_H):
        for c in range(MAP_W):
            if MAP[r][c] > 0:
                pygame.draw.rect(surface, (100, 100, 110), (c * scale + 15, r * scale + 15, scale - 1, scale - 1))
            else:
                pygame.draw.rect(surface, (40, 40, 45), (c * scale + 15, r * scale + 15, scale - 1, scale - 1))
                
    # Plot player location tracking point
    mx = int(px / TILE_SIZE * scale) + 15
    my = int(py / TILE_SIZE * scale) + 15
    pygame.draw.circle(surface, (255, 50, 50), (mx, my), 4)
    # Draw simple viewing path direction line pointing out of player dot
    pygame.draw.line(surface, (255, 200, 50), (mx, my), (mx + int(math.cos(p_angle) * 12), my + int(math.sin(p_angle) * 12)), 2)

# 4. MAIN EMULATION SIMULATION RUNNING TIMELINE LOOP
while True:
    dt = clock.tick(60) / 1000.0  # Smooth framerate delta timing modifier constant

    # System event loop monitoring
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not is_shooting:
                    is_shooting = True
                    weapon_frame = 1
                    weapon_cooldown = 0.25
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click to shoot
                if not is_shooting:
                    is_shooting = True
                    weapon_frame = 1
                    weapon_cooldown = 0.25

    # Core Input Matrices & Sliding Block Collision Vector Math Checking
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:  p_angle -= rot_speed * dt
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: p_angle += rot_speed * dt
    
    # Calculate looking vectors
    move_x = math.cos(p_angle) * speed * dt
    move_y = math.sin(p_angle) * speed * dt

    if keys[pygame.K_w]:
        # Wall sliding check: only step position coordinate index forward if layout field returns empty corridor 0 block space
        if MAP[int(py / TILE_SIZE)][int((px + move_x * 2.5) / TILE_SIZE)] == 0: px += move_x
        if MAP[int((py + move_y * 2.5) / TILE_SIZE)][int(px / TILE_SIZE)] == 0: py += move_y
    if keys[pygame.K_s]:
        if MAP[int(py / TILE_SIZE)][int((px - move_x * 2.5) / TILE_SIZE)] == 0: px -= move_x
        if MAP[int((py - move_y * 2.5) / TILE_SIZE)][int(px / TILE_SIZE)] == 0: py -= move_y

    # Process animation timer ticks
    if is_shooting:
        weapon_cooldown -= dt
        if weapon_cooldown <= 0:
            weapon_frame += 1
            if weapon_frame > 2:
                is_shooting = False
                weapon_frame = 0
            else:
                weapon_cooldown = 0.12

    # 5. GRAPHICS RENDERING SEQUENCE PIPELINE LAYERS
    # Render static background horizons sky box upper hemisphere half and floor lower hemisphere half base fields
    pygame.draw.rect(screen, SKY_COLOR, (0, 0, WIDTH, HEIGHT // 2))
    pygame.draw.rect(screen, FLOOR_COLOR, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))

    # The Raycasting Loop Sequence Block
    start_angle = p_angle - HALF_FOV
    for ray in range(NUM_RAYS):
        ray_angle = start_angle + ray * STEP_ANGLE
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # Enhanced DDA Step Alternative Fast Raycaster Loop
        for depth in range(1, RENDER_DISTANCE, 4):
            tx = px + cos_a * depth
            ty = py + sin_a * depth

            gx, gy = int(tx / TILE_SIZE), int(ty / TILE_SIZE)

            if 0 <= gx < MAP_W and 0 <= gy < MAP_H:
                wall_type = MAP[gy][gx]
                if wall_type > 0:
                    # Clear camera lens calculation algorithm filters out perspective fish-eye curved wall bending distortions
                    depth *= math.cos(ray_angle - p_angle)
                    
                    # Compute wall heights based on geometric distance tracking values
                    wall_height = min(HEIGHT, int((TILE_SIZE * 540) / (depth + 0.0001)))
                    
                    # Setup custom block group colors depending on wall layout IDs found inside arrays
                    base_color = WALL_COLOR_LIGHT if wall_type == 1 else (40, 150, 40) if wall_type == 2 else (40, 40, 170) if wall_type == 3 else (150, 150, 30)
                    
                    # Shading calculations: make objects darker the further away they are into depth channels
                    shading_factor = max(0.1, min(1.0, 350.0 / (depth + 0.001)))
                    
                    # Apply color tuple transformation elements safely
                    r_c = int(base_color[0] * shading_factor)
                    g_c = int(base_color[1] * shading_factor)
                    b_c = int(base_color[2] * shading_factor)

                    # Draw wall column projection line sequence arrays across screen viewport surface space
                    y0 = (HEIGHT // 2) - (wall_height // 2)
                    y1 = (HEIGHT // 2) + (wall_height // 2)
                    pygame.draw.line(screen, (r_c, g_c, b_c), (ray, y0), (ray, y1))
                    break

    # RENDER INTERACTIVE INTERFACE FOREGROUND LAYERS OVER THE 3D CANVAS VIEWPORT SPACE
    draw_weapon_sprite(screen, weapon_frame, is_shooting)
    draw_minimap(screen, scale=14)

    # Render a crosshair right in the middle of the screen
    pygame.draw.line(screen, (255, 255, 255), (WIDTH // 2 - 8, HEIGHT // 2), (WIDTH // 2 + 8, HEIGHT // 2), 2)
    pygame.draw.line(screen, (255, 255, 255), (WIDTH // 2, HEIGHT // 2 - 8), (WIDTH // 2, HEIGHT // 2 + 8), 2)

    # Final frame swap update pushing drawn assets buffer canvas layers straight onto monitor physical device panel elements
    pygame.display.flip()

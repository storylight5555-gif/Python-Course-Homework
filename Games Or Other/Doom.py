import pygame
import math
import sys
import random

# 1. CORE ENGINE & GRAPHICS SETUP
pygame.init()
WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro 3D Raycaster Engine - Alien Invasion")
clock = pygame.time.Clock()

# Color Definitions
SKY_COLOR = (45, 45, 65)
FLOOR_COLOR = (70, 70, 70)
WALL_COLOR_LIGHT = (190, 30, 30)
HUD_PANEL = (20, 20, 25)
TEXT_GOLD = (230, 180, 50)
HEALTH_RED = (200, 30, 30)
HEALTH_GREEN = (30, 180, 50)

# 2. THE LEVEL BLUEPRINT (Grid Map Layout)
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
MAP_W = len(MAP[0])
MAP_H = len(MAP)
TILE_SIZE = 64

# Camera Matrix Parameters
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH
STEP_ANGLE = FOV / NUM_RAYS
RENDER_DISTANCE = 1200

# 3. PLAYER & SYSTEMS TRACKING
px, py = 120.0, 120.0
p_angle = 0.0
speed = 180.0
rot_speed = 3.0
player_health = 100

# Weapon Sprite Animation State Controllers
is_shooting = False
weapon_frame = 0
weapon_cooldown = 0
has_deal_damage = False

# 4. ALIEN ENTITY CLASS
class Alien:
    def __init__(self):
        # Spawn randomly in empty space (0)
        while True:
            self.x = random.randint(1, MAP_W - 2) * TILE_SIZE + TILE_SIZE // 2
            self.y = random.randint(1, MAP_H - 2) * TILE_SIZE + TILE_SIZE // 2
            if MAP[int(self.y / TILE_SIZE)][int(self.x / TILE_SIZE)] == 0:
                break
        
        self.health = 3
        self.flash_timer = 0.0
        self.speed = 50.0
        self.move_timer = 0
        self.move_angle = random.uniform(0, math.pi * 2)
        self.attack_cooldown = 0.0

    def update(self, dt, player_x, player_y):
        if self.flash_timer > 0:
            self.flash_timer -= dt
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        # Simple AI: Wander around, or hunt if close
        dist_to_player = math.hypot(player_x - self.x, player_y - self.y)
        
        if dist_to_player < 250: # Hunt player
            self.move_angle = math.atan2(player_y - self.y, player_x - self.x)
            # Attack if within melee range
            if dist_to_player < 40 and self.attack_cooldown <= 0:
                global player_health
                player_health = max(0, player_health - 15)
                self.attack_cooldown = 1.0 # 1 second cooldown
        else: # Random walk behavior
            self.move_timer -= dt
            if self.move_timer <= 0:
                self.move_angle = random.uniform(0, math.pi * 2)
                self.move_timer = random.uniform(1.0, 3.0)

        # Move alien with basic wall sliding collision
        mx = math.cos(self.move_angle) * self.speed * dt
        my = math.sin(self.move_angle) * self.speed * dt
        if MAP[int(self.y / TILE_SIZE)][int((self.x + mx * 2) / TILE_SIZE)] == 0:
            self.x += mx
        if MAP[int((self.y + my * 2) / TILE_SIZE)][int(self.x / TILE_SIZE)] == 0:
            self.y += my

# Spawn 4 random initial aliens
aliens = [Alien() for _ in range(4)]

# 5. RENDER FUNCTIONS
def draw_weapon_sprite(surface, frame, shooting):
    wx, wy = WIDTH // 2, HEIGHT - 40
    bobbing = int(math.sin(pygame.time.get_ticks() * 0.005) * 4) if not shooting else 0
    wy += bobbing
    
    if shooting:
        if frame == 1:
            pygame.draw.circle(surface, (255, 230, 100), (wx, wy - 110), 35)
            pygame.draw.circle(surface, (255, 100, 30), (wx, wy - 110), 20)
        wy += 15
        
    pygame.draw.rect(surface, (30, 30, 35), (wx - 35, wy - 80, 25, 90))
    pygame.draw.rect(surface, (30, 30, 35), (wx + 10, wy - 80, 25, 90))
    pygame.draw.rect(surface, (15, 15, 18), (wx - 20, wy - 60, 40, 70))
    pygame.draw.rect(surface, (70, 75, 80), (wx - 30, wy - 95, 15, 20))
    pygame.draw.rect(surface, (70, 75, 80), (wx + 15, wy - 95, 15, 20))
    pygame.draw.circle(surface, (5, 5, 5), (wx - 23, wy - 95), 5)
    pygame.draw.circle(surface, (5, 5, 5), (wx + 22, wy - 95), 5)

def draw_hud(surface, health):
    # Health Bar Container Box
    pygame.draw.rect(surface, HUD_PANEL, (20, HEIGHT - 50, 220, 30))
    pygame.draw.rect(surface, (50, 50, 60), (20, HEIGHT - 50, 220, 30), 2)
    # Fill Amount
    if health > 0:
        health_width = int(216 * (health / 100))
        color = HEALTH_GREEN if health > 35 else HEALTH_RED
        pygame.draw.rect(surface, color, (22, HEIGHT - 48, health_width, 24))

def draw_minimap(surface, scale=12):
    for r in range(MAP_H):
        for c in range(MAP_W):
            if MAP[r][c] > 0:
                pygame.draw.rect(surface, (100, 100, 110), (c * scale + 15, r * scale + 15, scale - 1, scale - 1))
            else:
                pygame.draw.rect(surface, (40, 40, 45), (c * scale + 15, r * scale + 15, scale - 1, scale - 1))
    
    # Plot Aliens on Radar map
    for alien in aliens:
        ax = int(alien.x / TILE_SIZE * scale) + 15
        ay = int(alien.y / TILE_SIZE * scale) + 15
        pygame.draw.circle(surface, (30, 220, 30), (ax, ay), 3)

    mx = int(px / TILE_SIZE * scale) + 15
    my = int(py / TILE_SIZE * scale) + 15
    pygame.draw.circle(surface, (255, 50, 50), (mx, my), 4)
    pygame.draw.line(surface, (255, 200, 50), (mx, my), (mx + int(math.cos(p_angle) * 12), my + int(math.sin(p_angle) * 12)), 2)

# 6. MAIN EMULATION RUNNING TIMELINE LOOP
while True:
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
           (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            if not is_shooting and player_health > 0:
                is_shooting = True
                weapon_frame = 1
                weapon_cooldown = 0.25
                has_deal_damage = False # Reset dynamic damage trigger registration
                    
    # Player controls (Only work if alive)
    if player_health > 0:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: p_angle -= rot_speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: p_angle += rot_speed * dt
        
        move_x = math.cos(p_angle) * speed * dt
        move_y = math.sin(p_angle) * speed * dt
        
        if keys[pygame.K_w]:
            if MAP[int(py / TILE_SIZE)][int((px + move_x * 2.5) / TILE_SIZE)] == 0: px += move_x
            if MAP[int((py + move_y * 2.5) / TILE_SIZE)][int(px / TILE_SIZE)] == 0: py += move_y
        if keys[pygame.K_s]:
            if MAP[int(py / TILE_SIZE)][int((px - move_x * 2.5) / TILE_SIZE)] == 0: px -= move_x
            if MAP[int((py - move_y * 2.5) / TILE_SIZE)][int(px / TILE_SIZE)] == 0: py -= move_y

    # Update dynamic alien structures
    for alien in aliens:
        alien.update(dt, px, py)
            
    # Weapon State Machine Mechanics
    if is_shooting:
        weapon_cooldown -= dt
        if weapon_cooldown <= 0:
            weapon_frame += 1
            if weapon_frame > 2:
                is_shooting = False
                weapon_frame = 0
            else:
                weapon_cooldown = 0.12

    # 7. GRAPHICS RENDERING SEQUENCE PIPELINE LAYERS
    pygame.draw.rect(screen, SKY_COLOR, (0, 0, WIDTH, HEIGHT // 2))
    pygame.draw.rect(screen, FLOOR_COLOR, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
    
    # Raycast walls and store wall-depth values to buffer layout array
    wall_depth_buffer = [float('inf')] * NUM_RAYS
    start_angle = p_angle - HALF_FOV
    
    for ray in range(NUM_RAYS):
        ray_angle = start_angle + ray * STEP_ANGLE
        sin_a = math.sin(ray_angle) if math.sin(ray_angle) != 0 else 0.0001
        cos_a = math.cos(ray_angle) if math.cos(ray_angle) != 0 else 0.0001
        
        x_grid, y_grid = int(px / TILE_SIZE), int(py / TILE_SIZE)
        delta_dist_x, delta_dist_y = abs(1 / cos_a), abs(1 / sin_a)
        
        if cos_a < 0:
            step_x = -1
            side_dist_x = (px / TILE_SIZE - x_grid) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (x_grid + 1.0 - px / TILE_SIZE) * delta_dist_x
            
        if sin_a < 0:
            step_y = -1
            side_dist_y = (py / TILE_SIZE - y_grid) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (y_grid + 1.0 - py / TILE_SIZE) * delta_dist_y
            
        hit, side, depth = False, 0, 0
        while not hit and depth * TILE_SIZE < RENDER_DISTANCE:
            if side_dist_x < side_dist_y:
                depth = side_dist_x
                side_dist_x += delta_dist_x
                x_grid += step_x
                side = 0
            else:
                depth = side_dist_y
                side_dist_y += delta_dist_y
                y_grid += step_y
                side = 1
                
            if 0 <= x_grid < MAP_W and 0 <= y_grid < MAP_H:
                if MAP[y_grid][x_grid] > 0: hit = True
        
        if hit:
            depth_pixels = depth * TILE_SIZE
            depth_pixels *= math.cos(ray_angle - p_angle)
            wall_depth_buffer[ray] = depth_pixels # Save to depth map buffer
            
            wall_height = min(HEIGHT, int((TILE_SIZE * 540) / (depth_pixels + 0.0001)))
            base_color = WALL_COLOR_LIGHT if MAP[y_grid][x_grid] == 1 else (40, 150, 40)
            shading_factor = max(0.1, min(1.0, 350.0 / (depth_pixels + 0.001)))
            if side == 1: shading_factor *= 0.7
            
            y0 = (HEIGHT // 2) - (wall_height // 2)
            y1 = (HEIGHT // 2) + (wall_height // 2)

            pygame.draw.line(screen, (int(base_color[0]*shading_factor), int(base_color[1]*shading_factor), int(base_color[2]*shading_factor)), (ray, y0), (ray, y1))
            # 8. SPRITE RAYCASTING PIPELINE (Render Aliens)
        # (This line finishes the Raycasting Loop Wall Drawing phase)
        pygame.draw.line(screen, (int(base_color[0]*shading_factor), int(base_color[1]*shading_factor), int(base_color[2]*shading_factor)), (ray, y0), (ray, y1))

    # 8. SPRITE RAYCASTING PIPELINE (Render Aliens)
    # Sort alien objects from furthest to closest to prevent render overlaps
    aliens.sort(key=lambda a: math.hypot(px - a.x, py - a.y), reverse=True)
    
    for alien in list(aliens):
        # Calculate coordinate system distance tracking vectors
        sprite_x = alien.x - px
        sprite_y = alien.y - py
        
        # Translate position using camera angle calculations matrix geometry
        s_cos = math.cos(p_angle)
        s_sin = math.sin(p_angle)
        transform_x = sprite_x * s_sin - sprite_y * s_cos
        transform_y = sprite_x * s_cos + sprite_y * s_sin  # Distance tracking depth coordinate channel
        
        if transform_y <= 10: 
            continue  # Sprite is behind or directly on the camera matrix line
            
        # Perspective projection alignment positioning logic checks
        sprite_screen_x = int((WIDTH / 2) * (1 + transform_x / transform_y))
        sprite_size = min(2000, int((TILE_SIZE * 540) / transform_y))
        shading = max(0.1, min(1.0, 350.0 / (transform_y + 0.001)))
        
        # Draw column-by-column scaling sequence safely with z-buffer hiding
        start_x = max(0, sprite_screen_x - sprite_size // 2)
        end_x = min(WIDTH, sprite_screen_x + sprite_size // 2)
        
        # Combat checks: Is the alien targeted directly inside the center crosshair?
        if is_shooting and not has_deal_damage and weapon_frame == 1:
            if start_x <= WIDTH // 2 <= end_x and transform_y < wall_depth_buffer[WIDTH // 2]:
                alien.health -= 1
                alien.flash_timer = 0.15
                has_deal_damage = True  # Prevent continuous multi-damage triggers inside a single click phase
                if alien.health <= 0:
                    aliens.remove(alien)
                    continue
                    
        # Draw the vector alien shape column sequences on canvas layers safely
        for stripe in range(start_x, end_x):
            if 0 <= stripe < WIDTH and transform_y < wall_depth_buffer[stripe]:
                # Slice calculation matching vertical grid heights
                y_start = max(0, (HEIGHT // 2) - (sprite_size // 2))
                y_end = min(HEIGHT, (HEIGHT // 2) + (sprite_size // 2))
                
                # Alien color definition (Flashes white-red if shot)
                alien_color = (255, 60, 60) if alien.flash_timer > 0 else (60, 220, 80)
                r = int(alien_color[0] * shading)
                g = int(alien_color[1] * shading)
                b = int(alien_color[2] * shading)
                
                # Draw visual center bulk mass column stripes
                pygame.draw.line(screen, (r, g, b), (stripe, y_start + sprite_size//4), (stripe, y_end - sprite_size//4))
                
                # Draw stylized alien glowing central eye core structures
                if y_start + sprite_size//3 < HEIGHT // 2 < y_end - sprite_size//3:
                    if abs(stripe - sprite_screen_x) < sprite_size // 10:
                        pygame.draw.line(screen, (255, 255, 0), (stripe, HEIGHT // 2 - 2), (stripe, HEIGHT // 2 + 2))

    # Respawn replacements continuously if count gets too low
    if len(aliens) < 3:
        aliens.append(Alien())

    # RENDER INTERACTIVE INTERFACE FOREGROUND LAYERS
    if player_health > 0:
        draw_weapon_sprite(screen, weapon_frame, is_shooting)
        # Render a crosshair right in the middle of the screen
        pygame.draw.line(screen, (255, 255, 255), (WIDTH // 2 - 8, HEIGHT // 2), (WIDTH // 2 + 8, HEIGHT // 2), 2)
        pygame.draw.line(screen, (255, 255, 255), (WIDTH // 2, HEIGHT // 2 - 8), (WIDTH // 2, HEIGHT // 2 + 8), 2)
    else:
        # Game Over Banner display layout text matrices
        font = pygame.font.SysFont(None, 72)
        text = font.render("GAME OVER", True, (220, 30, 30))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 40))

    draw_minimap(screen, scale=14)
    draw_hud(screen, player_health)
    
    pygame.display.flip()
        # (This line finishes the Raycasting Loop Wall Drawing phase)
            # Setup custom block group colors depending on wall layout IDs found inside arrays
    base_color = WALL_COLOR_LIGHT if MAP[y_grid][x_grid] == 1 else (40, 150, 40)
    shading_factor = max(0.1, min(1.0, 350.0 / (depth_pixels + 0.001)))
    if side == 1: 
            shading_factor *= 0.7
            
        # FIX: Unpack the RGB tuple elements individually to safely apply the float shading modifier
        r_c = int(base_color[0] * shading_factor)
    g_c = int(base_color[1] * shading_factor)
    b_c = int(base_color[2] * shading_factor)
        
    y0 = (HEIGHT // 2) - (wall_height // 2)
    y1 = (HEIGHT // 2) + (wall_height // 2)
        
        # Draw wall column projection line using the individual calculated color pieces
    pygame.draw.line(screen, (r_c, g_c, b_c), (ray, y0), (ray, y1))




    # 8. SPRITE RAYCASTING PIPELINE (Render Aliens)
    # Sort alien objects from furthest to closest to prevent render overlaps
    aliens.sort(key=lambda a: math.hypot(px - a.x, py - a.y), reverse=True)
    
    for alien in list(aliens):
        # Calculate coordinate system distance tracking vectors
        sprite_x = alien.x - px
        sprite_y = alien.y - py
        
        # Translate position using camera angle calculations matrix geometry
        s_cos = math.cos(p_angle)
        s_sin = math.sin(p_angle)
        transform_x = sprite_x * s_sin - sprite_y * s_cos
        transform_y = sprite_x * s_cos + sprite_y * s_sin  # Distance tracking depth coordinate channel
        
        if transform_y <= 10: 
            continue  # Sprite is behind or directly on the camera matrix line
            
        # Perspective projection alignment positioning logic checks
        sprite_screen_x = int((WIDTH / 2) * (1 + transform_x / transform_y))
        sprite_size = min(2000, int((TILE_SIZE * 540) / transform_y))
        shading = max(0.1, min(1.0, 350.0 / (transform_y + 0.001)))
        
        # Draw column-by-column scaling sequence safely with z-buffer hiding
        start_x = max(0, sprite_screen_x - sprite_size // 2)
        end_x = min(WIDTH, sprite_screen_x + sprite_size // 2)
        
        # Combat checks: Is the alien targeted directly inside the center crosshair?
        if is_shooting and not has_deal_damage and weapon_frame == 1:
            if start_x <= WIDTH // 2 <= end_x and transform_y < wall_depth_buffer[WIDTH // 2]:
                alien.health -= 1
                alien.flash_timer = 0.15
                has_deal_damage = True  # Prevent continuous multi-damage triggers inside a single click phase
                if alien.health <= 0:
                    aliens.remove(alien)
                    continue
                    
        # Draw the vector alien shape column sequences on canvas layers safely
        for stripe in range(start_x, end_x):
            if 0 <= stripe < WIDTH and transform_y < wall_depth_buffer[stripe]:
                # Slice calculation matching vertical grid heights
                y_start = max(0, (HEIGHT // 2) - (sprite_size // 2))
                y_end = min(HEIGHT, (HEIGHT // 2) + (sprite_size // 2))
                
                # Alien color definition (Flashes white-red if shot)
                alien_color = (255, 60, 60) if alien.flash_timer > 0 else (60, 220, 80)
                r = int(alien_color[0] * shading)
                g = int(alien_color[1] * shading)
                b = int(alien_color[2] * shading)
                
                # Draw visual center bulk mass column stripes
                pygame.draw.line(screen, (r, g, b), (stripe, y_start + sprite_size//4), (stripe, y_end - sprite_size//4))
                
                # Draw stylized alien glowing central eye core structures
                if y_start + sprite_size//3 < HEIGHT // 2 < y_end - sprite_size//3:
                    if abs(stripe - sprite_screen_x) < sprite_size // 10:
                        pygame.draw.line(screen, (255, 255, 0), (stripe, HEIGHT // 2 - 2), (stripe, HEIGHT // 2 + 2))

    # Respawn replacements continuously if count gets too low
    if len(aliens) < 3:
        aliens.append(Alien())

    # RENDER INTERACTIVE INTERFACE FOREGROUND LAYERS
    if player_health > 0:
        draw_weapon_sprite(screen, weapon_frame, is_shooting)
        # Render a crosshair right in the middle of the screen
        pygame.draw.line(screen, (255, 255, 255), (WIDTH // 2 - 8, HEIGHT // 2), (WIDTH // 2 + 8, HEIGHT // 2), 2)
        pygame.draw.line(screen, (255, 255, 255), (WIDTH // 2, HEIGHT // 2 - 8), (WIDTH // 2, HEIGHT // 2 + 8), 2)
    else:
        # Game Over Banner display layout text matrices
        font = pygame.font.SysFont(None, 72)
        text = font.render("GAME OVER", True, (220, 30, 30))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 80))

        # Setup Respawn Button Coordinates
        btn_w, btn_h = 200, 50
        btn_x = WIDTH // 2 - btn_w // 2
        btn_y = HEIGHT // 2 + 10
        btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

        # Mouse hover state tracking
        mouse_pos = pygame.mouse.get_coords() if hasattr(pygame.mouse, "get_coords") else pygame.mouse.get_pos()
        btn_color = (80, 80, 90) if btn_rect.collidepoint(mouse_pos) else (40, 40, 45)

        # Draw Button Box and Outline
        pygame.draw.rect(screen, btn_color, btn_rect)
        pygame.draw.rect(screen, TEXT_GOLD, btn_rect, 2)

        # Render Button Text Label
        btn_font = pygame.font.SysFont(None, 36)
        btn_text = btn_font.render("RESPAWN", True, TEXT_GOLD)
        screen.blit(btn_text, (btn_x + btn_w // 2 - btn_text.get_width() // 2, btn_y + btn_h // 2 - btn_text.get_height() // 2))

        # Check for click activation events inside the button bounding area
        mouse_click = pygame.mouse.get_pressed()
        if mouse_click[0] and btn_rect.collidepoint(mouse_pos):
            # Full Game Engine Variable Reset Chain
            player_health = 100
            px, py = 120.0, 120.0
            p_angle = 0.0
            is_shooting = False
            weapon_frame = 0
            # Wipe active alien arrays clean and generate new ones
            aliens = [Alien() for _ in range(4)]
            pygame.time.wait(150)  # Brief delay to prevent accidental multi-click buffering

    draw_minimap(screen, scale=14)
    draw_hud(screen, player_health)
    
    pygame.display.flip()
        


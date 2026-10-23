import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()

# Window Setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Beach Buggy Pseudo-3D Racer")
clock = pygame.time.Clock()

# Color Palette
SKY_BLUE = (100, 180, 240)
SAND_YELLOW = (235, 210, 160)
WATER_BLUE = (30, 120, 200)
ROAD_GRAY = (90, 95, 100)
CURB_RED = (220, 50, 50)
CURB_WHITE = (240, 240, 240)
PALM_GREEN = (34, 139, 34)
TRUNK_BROWN = (139, 69, 19)

class GameState:
    def __init__(self):
        self.position = 0.0 
        self.player_x = 0.0 
        self.speed = 0.0 
        self.max_speed = 400.0 
        self.accel = 8.0 
        self.breaking = 15.0 
        self.decel = 3.0 
        self.track = []
        self.generate_track()
        self.track_length = len(self.track) * 200 
        self.scenery = []
        self.generate_scenery()
        self.score = 0
        self.game_over = False

    def generate_track(self):
        for _ in range(50): self.track.append(0)   
        for _ in range(40): self.track.append(1.5) 
        for _ in range(30): self.track.append(0)   
        for _ in range(50): self.track.append(-2.5)
        for _ in range(40): self.track.append(0)   
        for _ in range(60): self.track.append(3.5) 
        for _ in range(50): self.track.append(0)   

    def generate_scenery(self):
        for i in range(10, len(self.track) - 10, 3):
            side = random.choice([-1.6, 1.6])
            self.scenery.append([i * 200, side, "tree"])
        for i in range(30, len(self.track) - 10, 15):
            lane = random.choice([-0.5, 0.0, 0.5])
            self.scenery.append([i * 200, lane, "barrel"])

    def get_segment(self, pos):
        idx = int(pos / 200) % len(self.track)
        return self.track[idx]

def draw_palm_tree(surface, x, y, scale):
    if scale <= 0: return
    tw = int(20 * scale)
    th = int(100 * scale)
    if y - th < 0: return
    pygame.draw.rect(surface, TRUNK_BROWN, (x - tw//4, y - th, tw//2, th))
    pygame.draw.circle(surface, PALM_GREEN, (x, y - th), int(35 * scale))
    pygame.draw.circle(surface, (46, 204, 113), (x - int(15*scale), y - th), int(20 * scale))
    pygame.draw.circle(surface, (46, 204, 113), (x + int(15*scale), y - th), int(20 * scale))

def draw_barrel(surface, x, y, scale):
    if scale <= 0: return
    bw = int(30 * scale)
    bh = int(40 * scale)
    pygame.draw.rect(surface, (230, 80, 40), (x - bw//2, y - bh, bw, bh), border_radius=3)
    pygame.draw.rect(surface, (240, 240, 240), (x - bw//2, y - int(bh*0.7), bw, int(6*scale)))

def main():
    state = GameState()
    horizon = 240 

    while True:
        dt = clock.tick(FPS) / 1000.0 

        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and state.game_over:
                state = GameState() 

        # 2. Physics & Real-time Inputs
        if not state.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                state.speed = min(state.speed + state.accel, state.max_speed)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                state.speed = max(state.speed - state.breaking, 0)
            else:
                state.speed = max(state.speed - state.decel, 0)

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                state.player_x -= 0.04 * (state.speed / state.max_speed)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                state.player_x += 0.04 * (state.speed / state.max_speed)

            state.position += state.speed * dt * 30
            current_curve = state.get_segment(state.position)
            state.player_x -= current_curve * 0.005 * (state.speed / state.max_speed)

            if abs(state.player_x) > 1.3:
                state.game_over = True
            state.score += int(state.speed * dt * 0.1)
            if state.position >= state.track_length:
                state.position = 0

        # 3. Graphics Rendering Layout
        screen.fill(WATER_BLUE) 
        pygame.draw.rect(screen, SKY_BLUE, (0, 0, SCREEN_WIDTH, horizon)) 
        pygame.draw.rect(screen, SAND_YELLOW, (0, horizon, SCREEN_WIDTH, SCREEN_HEIGHT - horizon)) 

        dx = 0.0
        cam_curve = 0.0
        render_queue = [] 

        for y in range(SCREEN_HEIGHT - 1, horizon, -2):
            projected_depth = (y - horizon) / (SCREEN_HEIGHT - horizon)
            if projected_depth <= 0.001:  # Protect against division by zero errors
                continue 

            world_z = 200.0 / projected_depth
            line_pos = state.position + world_z
            
            curve_val = state.get_segment(line_pos)
            cam_curve += curve_val * 0.15
            dx += cam_curve
            
            road_center = (SCREEN_WIDTH // 2) + int(dx) - int(state.player_x * SCREEN_WIDTH * 0.4 * projected_depth)
            road_width = int(SCREEN_WIDTH * 0.55 * projected_depth)

            curb_color = CURB_RED if int(line_pos / 40) % 2 == 0 else CURB_WHITE
            road_color = ROAD_GRAY if int(line_pos / 80) % 2 == 0 else (95, 100, 105)

            pygame.draw.rect(screen, curb_color, (road_center - road_width//2 - int(30*projected_depth), y, road_width + int(60*projected_depth), 2))
            pygame.draw.rect(screen, road_color, (road_center - road_width//2, y, road_width, 2))

            for item in state.scenery:
                pos_z, side_offset, type_str = item
                if abs(pos_z - line_pos) < 20: 
                    sprite_x = road_center + int(side_offset * road_width * 0.9)
                    render_queue.append((projected_depth, sprite_x, y, type_str, item))

        render_queue.sort(key=lambda t: t[0])
        for p_depth, sx, sy, item_type, raw_data in render_queue:
            if item_type == "tree":
                draw_palm_tree(screen, sx, sy, p_depth * 1.8)
            elif item_type == "barrel":
                draw_barrel(screen, sx, sy, p_depth * 1.5)

            if sy > SCREEN_HEIGHT - 120 and sy < SCREEN_HEIGHT - 60:
                bx_world = raw_data[1]
                if abs(state.player_x - bx_world) < 0.25:
                    state.game_over = True

        # 4. Draw Player Buggy Sprite
        buggy_x = SCREEN_WIDTH // 2
        buggy_y = SCREEN_HEIGHT - 80
        pygame.draw.ellipse(screen, (10, 10, 10), (buggy_x - 55, buggy_y + 10, 25, 45))
        pygame.draw.ellipse(screen, (10, 10, 10), (buggy_x + 30, buggy_y + 10, 25, 45))
        pygame.draw.rect(screen, (243, 156, 18), (buggy_x - 40, buggy_y, 80, 35), border_radius=12)
        pygame.draw.rect(screen, (241, 196, 15), (buggy_x - 30, buggy_y - 15, 60, 20), border_radius=6)
        pygame.draw.rect(screen, (50, 50, 50), (buggy_x - 22, buggy_y - 10, 44, 12))

        # 5. HUD Dashboard UI
        font = pygame.font.SysFont('Impact', 28)
        score_lbl = font.render(f"SCORE: {state.score}", True, (255, 255, 255))
        speed_lbl = font.render(f"{int(state.speed * 0.5)} MPH", True, (241, 196, 15))
        screen.blit(score_lbl, (20, 20))
        screen.blit(speed_lbl, (SCREEN_WIDTH - 130, 20))

        if state.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            go_font = pygame.font.SysFont('Impact', 64)
            sub_font = pygame.font.SysFont('Arial', 24, bold=True)
            t1 = go_font.render("WIPED OUT!", True, (255, 70, 70))
            t2 = sub_font.render("Press SPACEBAR to Reset Buggy", True, (255, 255, 255))
            screen.blit(t1, t1.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)))
            screen.blit(t2, t2.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30)))

        # CRITICAL FIX: Push the drawn images onto the physical monitor display
        pygame.display.flip()

if __name__ == "__main__":
    main()


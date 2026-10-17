import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
FPS = 60

# Colors
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
GREEN = (34, 139, 34)
YELLOW = (255, 215, 0)

# Setup Display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top-Down Highway Racer")
clock = pygame.time.Clock()

class PlayerCar:
    def __init__(self):
        self.width = 45
        self.height = 80
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 120
        self.speed = 6

    def move(self, keys):
        # Move Left (with boundary checks ensuring car stays on asphalt)
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x > 85:
            self.x -= self.speed
        # Move Right
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x < SCREEN_WIDTH - 85 - self.width:
            self.x += self.speed
        # Move Up
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y > 50:
            self.y -= self.speed
        # Move Down
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y < SCREEN_HEIGHT - self.height - 20:
            self.y += self.speed

    def draw(self, surface):
        # Draw Main Car Body
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height), border_radius=5)
        # Windows
        pygame.draw.rect(surface, (30, 30, 30), (self.x + 5, self.y + 15, self.width - 10, 20))
        pygame.draw.rect(surface, (30, 30, 30), (self.x + 5, self.y + 50, self.width - 10, 15))
        # Headlights
        pygame.draw.rect(surface, YELLOW, (self.x + 4, self.y, 8, 5))
        pygame.draw.rect(surface, YELLOW, (self.x + self.width - 12, self.y, 8, 5))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class TrafficCar:
    def __init__(self, speed):
        self.width = 45
        self.height = 80
        # Spawn randomly in one of the road lanes (between x=85 and x=370)
        self.x = random.randint(85, SCREEN_WIDTH - 85 - self.width)
        self.y = random.randint(-400, -90)
        self.speed = speed
        self.color = random.choice([BLUE, (200, 100, 0), (128, 0, 128), (0, 128, 128)])

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), border_radius=5)
        # Windows
        pygame.draw.rect(surface, (30, 30, 30), (self.x + 5, self.y + 45, self.width - 10, 20))
        # Tail lights
        pygame.draw.rect(surface, (255, 0, 0), (self.x + 4, self.y + self.height - 5, 8, 5))
        pygame.draw.rect(surface, (255, 0, 0), (self.x + self.width - 12, self.y + self.height - 5, 8, 5))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


def draw_environment(surface, road_y):
    # Fill background with grass green
    surface.fill(GREEN)
    # Draw central asphalt highway road
    pygame.draw.rect(surface, GRAY, (75, 0, SCREEN_WIDTH - 150, SCREEN_HEIGHT))
    # Draw solid side white lines
    pygame.draw.line(surface, WHITE, (75, 0), (75, SCREEN_HEIGHT), 5)
    pygame.draw.line(surface, WHITE, (SCREEN_WIDTH - 75, 0), (SCREEN_WIDTH - 75, SCREEN_HEIGHT), 5)
    
    # Draw animated dashed lanes dividing the highway
    lane_x1 = 210
    lane_x2 = 290
    for y in range(-100, SCREEN_HEIGHT + 100, 80):
        pygame.draw.rect(surface, WHITE, (lane_x1, y + (road_y % 80), 6, 40))
        pygame.draw.rect(surface, WHITE, (lane_x2, y + (road_y % 80), 6, 40))


def main():
    player = PlayerCar()
    base_traffic_speed = 4
    traffic_cars = [TrafficCar(base_traffic_speed)]
    
    road_y = 0
    score = 0
    game_active = True

    while True:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_active:
                    # Reset Game State
                    player = PlayerCar()
                    base_traffic_speed = 4
                    traffic_cars = [TrafficCar(base_traffic_speed)]
                    score = 0
                    game_active = True

        if game_active:
            # Handle real-time continuous movement inputs
            keys = pygame.key.get_pressed()
            player.move(keys)

            # Move background road animation
            road_y += base_traffic_speed

            # Manage Traffic Enemy Cars
            for car in traffic_cars:
                car.update()
                
                # Check for crash collisions
                if player.get_rect().colliderect(car.get_rect()):
                    game_active = False

                # If traffic car goes off screen, recycle/replace it
                if car.y > SCREEN_HEIGHT:
                    traffic_cars.remove(car)
                    score += 1
                    # Progressively ramp up game speed difficulty
                    if score % 5 == 0:
                        base_traffic_speed += 0.5
                    traffic_cars.append(TrafficCar(base_traffic_speed))

            # Maintain a multi-car traffic density as score scales up
            if len(traffic_cars) < 3 and random.randint(1, 100) == 1:
                # Ensure they don't instantly spawn on top of each other
                new_car = TrafficCar(base_traffic_speed)
                if all(abs(new_car.y - c.y) > 150 for c in traffic_cars):
                    traffic_cars.append(new_car)

        # Draw Frame Scene
        draw_environment(screen, road_y)
        
        for car in traffic_cars:
            car.draw(screen)
            
        player.draw(screen)

        # Draw HUD UI Score Tracker
        font = pygame.font.SysFont('Arial', 24, bold=True)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (15, 15))

        # Draw Game Over Overlay Screen
        if not game_active:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) # Semi-transparent tint overlay
            screen.blit(overlay, (0,0))
            
            go_font = pygame.font.SysFont('Arial', 36, bold=True)
            text1 = go_font.render("WRECKED!", True, (255, 50, 50))
            text2 = font.render("Press SPACEBAR to Drive Again", True, WHITE)
            
            screen.blit(text1, text1.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30)))
            screen.blit(text2, text2.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20)))

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
SKY_BLUE = (113, 197, 207)
BIRD_YELLOW = (247, 215, 66)
PIPE_GREEN = (115, 191, 46)
GROUND_BROWN = (222, 216, 149)

# Setup Display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird in Python")
clock = pygame.time.Clock()

class Bird:
    def __init__(self):
        self.x = 80
        self.y = SCREEN_HEIGHT // 2
        self.radius = 15
        self.velocity = 0
        self.gravity = 0.4
        self.jump_strength = -6.5

    def flap(self):
        self.velocity = self.jump_strength

    def update(self):
        # Apply physics
        self.velocity += self.gravity
        self.y += int(self.velocity)
        
        # Floor and ceiling boundaries
        if self.y < self.radius:
            self.y = self.radius
            self.velocity = 0
        if self.y > SCREEN_HEIGHT - 40 - self.radius: # 40px is ground height
            self.y = SCREEN_HEIGHT - 40 - self.radius
            return False # Hit ground
        return True

    def draw(self, surface):
        pygame.draw.circle(surface, BIRD_YELLOW, (self.x, self.y), self.radius)
        # Eye
        pygame.draw.circle(surface, (0, 0, 0), (self.x + 6, self.y - 4), 3)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 65
        self.gap = 140
        self.speed = 3
        self.passed = False
        
        # Calculate random height constraints
        min_height = 50
        max_height = SCREEN_HEIGHT - 40 - self.gap - min_height
        self.top_height = random.randint(min_height, max_height)
        self.bottom_y = self.top_height + self.gap
        self.bottom_height = SCREEN_HEIGHT - 40 - self.bottom_y

    def update(self):
        self.x -= self.speed

    def draw(self, surface):
        # Top Pipe
        pygame.draw.rect(surface, PIPE_GREEN, (self.x, 0, self.width, self.top_height))
        # Bottom Pipe
        pygame.draw.rect(surface, PIPE_GREEN, (self.x, self.bottom_y, self.width, self.bottom_height))

    def collide(self, bird):
        # Bird bounding box check
        if bird.x + bird.radius > self.x and bird.x - bird.radius < self.x + self.width:
            # Check top pipe
            if bird.y - bird.radius < self.top_height:
                return True
            # Check bottom pipe
            if bird.y + bird.radius > self.bottom_y:
                return True
        return False

def draw_score(surface, score):
    font = pygame.font.SysFont('Arial', 32, bold=True)
    score_surface = font.render(str(score), True, WHITE)
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 40))
    surface.blit(score_surface, score_rect)

def draw_game_over(surface):
    font = pygame.font.SysFont('Arial', 24, bold=True)
    text = font.render("GAME OVER - Press SPACE to restart", True, (200, 0, 0))
    rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    surface.blit(text, rect)

def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + 100), Pipe(SCREEN_WIDTH + 350)]
    score = 0
    game_active = True

    while True:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_active:
                        bird.flap()
                    else:
                        # Reset game
                        bird = Bird()
                        pipes = [Pipe(SCREEN_WIDTH + 100), Pipe(SCREEN_WIDTH + 350)]
                        score = 0
                        game_active = True

        # Game Logic
        if game_active:
            # Update bird
            if not bird.update():
                game_active = False # Hit ground

            # Update pipes
            for pipe in pipes:
                pipe.update()
                if pipe.collide(bird):
                    game_active = False # Hit pipe
                
                # Check if bird passed the pipe successfully
                if not pipe.passed and pipe.x + pipe.width < bird.x:
                    pipe.passed = True
                    score += 1

            # Remove off-screen pipes and add new ones
            if pipes[0].x < -pipes[0].width:
                pipes.pop(0)
                # Spawn new pipe relative to the current last pipe's position
                pipes.append(Pipe(pipes[-1].x + 250))

        # Rendering
        screen.fill(SKY_BLUE)
        
        for pipe in pipes:
            pipe.draw(screen)
            
        # Draw Ground
        pygame.draw.rect(screen, GROUND_BROWN, (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40))
        pygame.draw.line(screen, (100, 150, 50), (0, SCREEN_HEIGHT - 40), (SCREEN_WIDTH, SCREEN_HEIGHT - 40), 3)

        bird.draw(screen)
        draw_score(screen, score)

        if not game_active:
            draw_game_over(screen)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

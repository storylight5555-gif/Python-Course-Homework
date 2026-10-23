import pygame
import random

pygame.init()
sprite_colour_change_event = pygame.USEREVENT + 1
background_colour_change_event = pygame.USEREVENT + 2

BLUE = pygame.Color('blue')
LIGHT_BLUE = pygame.Color('lightblue')
DARK_BLUE = pygame.Color('darkblue')

YELLOW = pygame.Color('yellow')
RED = pygame.Color('red')
ORANGE = pygame.Color('orange')
WHITE = pygame.Color('white')
GREEN = pygame.Color('green')

class sprite(pygame.sprite.Sprite):
    def __init__(self, colour,height,width):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.velocity = [random.choice([-1, 1]), random.choice([-1, 1])]

    def update(self):
        self.rect.move_ip(self.velocity)
        boundary_hit = False
        if self.rect.left <=0 or self.rect.right >= 500:
            self.velocity[0] = -self.velocity[0]
            boundary_hit = True
        if self.rect.top <=0 or self.rect.bottom >= 400:
            self.velocity[1] = -self.velocity[1]
            boundary_hit = True
        if boundary_hit:
            pygame.event.post(pygame.event.Event(sprite_colour_change_event ))
            pygame.event.post(pygame.event.Event(background_colour_change_event ))
    def change_colour(self):
        self.image.fill(random.choice([YELLOW, RED, ORANGE, WHITE, GREEN]))
def change_background_colour():
    global bg_colour
    bg_colour = random.choice([BLUE, LIGHT_BLUE, DARK_BLUE])
all_sprites_list = pygame.sprite.Group()
sp1 = sprite(WHITE, 50, 50)
sp1.rect.x = random.randint(0, 480)
sp1.rect.y = random.randint(0, 370)
all_sprites_list.add(sp1)
screen = pygame.display.set_mode([500, 400])
pygame.display.set_caption("Boudary Sprite")
bg_colour = BLUE
screen.fill(bg_colour)


done = False
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == sprite_colour_change_event:
            sp1.change_colour()
        elif event.type == background_colour_change_event:
            change_background_colour()
    all_sprites_list.update()
    screen.fill(bg_colour)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(240)
pygame.quit()        
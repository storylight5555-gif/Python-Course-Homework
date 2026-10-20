import pygame

pygame.init()

screen = pygame.display.set_mode((800, 800))
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pygame.draw.circle(screen, (125, 0, 125), (200, 150), 50)
    pygame.draw.circle(screen, (225, 225, 225), (300, 250), 25, 5)
    pygame.display.flip()

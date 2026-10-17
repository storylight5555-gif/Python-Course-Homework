import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Adding Image And Background Image")
bg_img=pygame.transform.scale(pygame.image.load("C:\\Users\\karth\\OneDrive\\Desktop\\Python Course\\Module4\\Lesson1\\Jungle_Background.jpg").convert(), (500, 500))
img=pygame.transform.scale(pygame.image.load("C:\\Users\\karth\\OneDrive\\Desktop\\Python Course\\Module4\\Lesson1\\Parrot_image.jpg").convert_alpha(), (200, 200))
image_rect=img.get_rect(center=(250, 250))


text=pygame.font.Font(None, 36).render("Parrot In a Jungle", True, pygame.Color("black"))
text_rect=text.get_rect(center=(370, 400))
def game_loop():
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(bg_img, (0, 0))
        screen.blit(img, image_rect)
        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

game_loop()

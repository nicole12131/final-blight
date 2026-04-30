import pygame
pygame.init()

def draw_text(text, size, color, surface, x, y):
    font = pygame.font.Font('assets\Darkbyte-4nly6.ttf', size)
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

#example
screen = pygame.display.set_mode((800, 600)) #Screen x, y
draw_text('Hello World!', 32, (0, 255, 255), screen, 100, 100)
#        ^^^^text^^^^^^^^size^^^^^color^^^^^^surface^^^x^^^y^^

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
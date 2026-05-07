import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skill System")

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK = (50, 50, 50)
GREEN = (100, 200, 100)
RED = (255, 64, 64)

font = pygame.font.SysFont(None, 36)

running = True
intro_skipped = False

class SkipButton:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        txt = font.render(self.text, True, DARK)
        screen.blit(txt, (self.rect.x + 15, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

skip_button = SkipButton("Skip", 650, 500, 120, 50)

intro_lines = [
    "Prelude: A kingdom called ArisKatsia",
    "The last king lays slaughtered in front of the prince's eyes.",
    "This is a trial about tragedy.",
    "Now it's only up to you, our last prince, Zan.",
    "THE FINAL BLIGHT"
]

line_index = 0
last_update = pygame.time.get_ticks()
delay = 2500  
print("Dramatic Music Playing...")

while running:
    screen.fill(RED)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if skip_button.is_clicked(event.pos):
                intro_skipped = True
                line_index = len(intro_lines) - 1

    skip_button.draw()


    current_time = pygame.time.get_ticks()

    if current_time - last_update > delay and not intro_skipped:
        if line_index < len(intro_lines) - 1:
            line_index += 1
            last_update = current_time

    text = font.render(intro_lines[line_index], True, WHITE)
    screen.blit(text, (50, HEIGHT // 2))

    if intro_skipped:
        skip_text = font.render(
            "You skipped the intro.", True, GREEN
        )
        screen.blit(skip_text, (50, HEIGHT // 2 + 60))

    pygame.display.flip()

pygame.quit()
sys.exit()



#When the user quit add that it loads the new game into a new csv and start displaying first level 
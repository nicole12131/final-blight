import pygame
import sys


pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skill System")

font = pygame.font.SysFont(None, 36)

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK = (50, 50, 50)
GREEN = (100, 200, 100)
RED = (200, 100, 100)

skills = {"Strength": 1, "Magic": 2}
traits = {"Health": 5, "Stamina": 3}
materials = 250

state = "main"

class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, enabled=True):
        color = GRAY if enabled else RED
        pygame.draw.rect(screen, color, self.rect)
        txt = font.render(self.text, True, DARK)
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


check_btn = Button("Check", 300, 200, 200, 50)
upgrade_btn = Button("Upgrade", 300, 300, 200, 50)
back_btn = Button("Back", 300, 500, 200, 50)

upgrade_buttons = []

y = 180
for s in skills:
    upgrade_buttons.append(("skill", s, 10, Button(f"{s} (+1) - 10", 100, y, 250, 40)))
    y += 60

y = 180
for t in traits:
    upgrade_buttons.append(("trait", t, 5, Button(f"{t} (+1) - 5", 450, y, 250, 40)))
    y += 60


def draw_main():
    screen.fill(WHITE)
    title = font.render("Main Menu", True, DARK)
    screen.blit(title, (320, 50))

    check_btn.draw()
    upgrade_btn.draw()


def draw_check():
    screen.fill(WHITE)
    title = font.render("Check Menu", True, DARK)
    screen.blit(title, (320, 50))

    y1 = 150
    for s, lvl in skills.items():
        txt = font.render(f"{s}: {lvl}", True, DARK)
        screen.blit(txt, (100, y1))
        y1 += 40

    y2 = 150
    for t, lvl in traits.items():
        txt = font.render(f"{t}: {lvl}", True, DARK)
        screen.blit(txt, (450, y2))
        y2 += 40

    back_btn.draw()


def draw_upgrade():
    screen.fill(WHITE)
    title = font.render("Upgrade Menu", True, DARK)
    screen.blit(title, (280, 50))

    mat_txt = font.render(f"Materials: {materials}", True, DARK)
    screen.blit(mat_txt, (300, 100))

    for kind, name, cost, btn in upgrade_buttons:
        enabled = materials >= cost
        btn.draw(enabled)

    back_btn.draw()


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if state == "main":
                if check_btn.is_clicked(pos):
                    state = "check"
                elif upgrade_btn.is_clicked(pos):
                    state = "upgrade"

            elif state == "check":
                if back_btn.is_clicked(pos):
                    state = "main"

            elif state == "upgrade":
                if back_btn.is_clicked(pos):
                    state = "main"

                for kind, name, cost, btn in upgrade_buttons:
                    if btn.is_clicked(pos) and materials >= cost:
                        if kind == "skill":
                            skills[name] += 1
                        else:
                            traits[name] += 1
                        materials -= cost

    
    if state == "main":
        draw_main()
    elif state == "check":
        draw_check()
    elif state == "upgrade":
        draw_upgrade()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
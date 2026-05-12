import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skill System")

clock = pygame.time.Clock()

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
GREEN = (100, 220, 120)
RED = (220, 120, 120)
BLUE = (120, 170, 255)

font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 22)


skills = {
    "Strength": 1,
    "Magic": 2
}

traits = {
    "Health": 5,
    "Stamina": 3
}

materials = 250

state = "main"


class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, enabled=True):
        mouse_pos = pygame.mouse.get_pos()

        if not enabled:
            color = RED
        elif self.rect.collidepoint(mouse_pos):
            color = BLUE
        else:
            color = GRAY

        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)

        txt = small_font.render(self.text, True, BLACK)
        txt_rect = txt.get_rect(center=self.rect.center)
        screen.blit(txt, txt_rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


check_btn = Button("Check Stats", 325, 220, 250, 60)
upgrade_btn = Button("Upgrade", 325, 320, 250, 60)
back_btn = Button("Back", 325, 560, 250, 50)

def get_cost(level):
    return 5 + level * 2

def draw_main():
    screen.fill(WHITE)

    title = font.render("Main Menu", True, BLACK)
    screen.blit(title, (360, 80))

    check_btn.draw()
    upgrade_btn.draw()


def draw_check():
    screen.fill(WHITE)

    title = font.render("Player Stats", True, BLACK)
    screen.blit(title, (350, 50))

    y = 160

    skill_title = font.render("Skills", True, BLACK)
    screen.blit(skill_title, (150, 110))

    for name, level in skills.items():
        txt = small_font.render(f"{name}: {level}", True, BLACK)
        screen.blit(txt, (150, y))
        y += 40

    y = 160

    trait_title = font.render("Traits", True, BLACK)
    screen.blit(trait_title, (550, 110))

    for name, level in traits.items():
        txt = small_font.render(f"{name}: {level}", True, BLACK)
        screen.blit(txt, (550, y))
        y += 40

    back_btn.draw()


def draw_upgrade():
    screen.fill(WHITE)

    title = font.render("Upgrade Menu", True, BLACK)
    screen.blit(title, (330, 50))

    mats = font.render(f"Materials: {materials}", True, BLACK)
    screen.blit(mats, (340, 100))

    buttons = []

    y = 180

    for name, level in skills.items():
        cost = get_cost(level)

        text = f"{name} Lv {level} | Cost: {cost}"

        btn = Button(text, 100, y, 300, 50)

        enabled = materials >= cost
        btn.draw(enabled)

        buttons.append(("skill", name, cost, btn))

        y += 70

    y = 180

    for name, level in traits.items():
        cost = get_cost(level)

        text = f"{name} Lv {level} | Cost: {cost}"

        btn = Button(text, 500, y, 300, 50)

        enabled = materials >= cost
        btn.draw(enabled)

        buttons.append(("trait", name, cost, btn))

        y += 70

    back_btn.draw()

    return buttons


running = True

while running:

    upgrade_buttons = []

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()

            if state == "main":

                if check_btn.clicked(pos):
                    state = "check"

                elif upgrade_btn.clicked(pos):
                    state = "upgrade"

            elif state == "check":

                if back_btn.clicked(pos):
                    state = "main"

            elif state == "upgrade":

                if back_btn.clicked(pos):
                    state = "main"

                for kind, name, cost, btn in upgrade_buttons:

                    if btn.clicked(pos) and materials >= cost:

                        materials -= cost

                        if kind == "skill":
                            skills[name] += 1
                        else:
                            traits[name] += 1

    if state == "main":
        draw_main()

    elif state == "check":
        draw_check()

    elif state == "upgrade":
        upgrade_buttons = draw_upgrade()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
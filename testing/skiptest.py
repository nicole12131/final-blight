import pygame
import sys

sys.path.append('/src')
import font

# --- Initialize Pygame ---
pygame.init()

# --- Screen & Constants ---
screen_width, screen_height = 800, 600
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Skill System")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0) # Defined missing GREEN
run2 = True

# --- Dummy functions/assets to make it run without files ---
def fade(w, h, color):
    # Simplified fade for example
    surface = pygame.Surface((w, h))
    surface.fill(color)
    win.blit(surface, (0,0))
    pygame.display.update()
    pygame.time.delay(10)

# Replaced image loads with surfaces to make code runnable
techi = pygame.Surface((75, 75))
techi.fill((200, 0, 0)) # Red block instead of Techi-Joe.gif
techi_bubble = pygame.Surface((700, 350))
techi_bubble.fill((50, 50, 50)) # Gray box instead of png

# --- Dialogue Data ---
techi_says = [
    "Hello, User!",
    "My name is Techi-Joe.",
    "I'm a programmer,",
    "and this is my first game:",
    "Dunk the Chief!",
    "in Dunk the Chief,",
    "your main objective",
    "is to dunk any US president",
    "you choose",
    "in a cold tub of water!",
    "yay!"
]

# --- writeLikeCode function ---
def writeLikeCode(string, xpos, ypos, font, color):
    """Renders text letter by letter."""
    for i in range(len(string)):
        # Handle events inside loop to prevent freezing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Slice string up to current letter
        current_text = string[:i+1]
        text_surface = font.render(current_text, True, color)
        
        # Clear specific area and redraw text
        # (Using a simpler approach here)
        win.blit(text_surface, (xpos, ypos))
        pygame.display.update()
        pygame.time.delay(30)

# --- Main Loop ---
techi_font = pygame.font.SysFont("Consolas", 25)
bg = pygame.Surface((screen_width, screen_height))
bg.fill(WHITE)

while run2:
    # --- Introduction sequence ---
    # fade(screen_width, screen_height, BLACK) # Uncomment if fade is fixed
    
    for a in range(len(techi_says)):
        # Clear screen and draw background/techi
        win.blit(bg, (0, 0))
        win.blit(techi_bubble, (50, 300)) # Moved to be visible
        win.blit(techi, (100, 350))       # Moved to be visible
        
        # Write text
        writeLikeCode(techi_says[a],draw_text)
        pygame.time.delay(500) # Pause between sentences

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run2 = False
                pygame.quit()
                sys.exit()
    
    run2 = False # End after dialogue for this example

pygame.quit()

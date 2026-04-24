import pygame
from character import Character
from ground import GroundLayer
from world import World

pygame.init()

# Create the game window.
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load ground layers with different Z-heights.
# Z determines elevation (0 = ground, 10 = higher platform, etc.)
world_layers = [
    GroundLayer("testing/ground1.png", 0),
    GroundLayer("testing/ground2.png", 10),
    GroundLayer("testing/ground3.png", 20),
]

# Create the world container.
world = World(world_layers)

# Create the player at world position (400, 300).
player = Character("testing/player.png", 400, 300)

run = True
while run:
    dt = clock.tick(60)  # Limit to 60 FPS.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update player movement, jumping, gravity, and collision.
    player.update(pygame.key.get_pressed(), world, world.layers)

    # Clear screen.
    screen.fill((40, 40, 40))

    # Draw layers in order of height (lowest first).
    for layer in sorted(world.layers, key=lambda l: l.z):
        screen.blit(layer.image, layer.rect)

    # Draw the player sprite (always centered on screen).
    screen.blit(player.image, player.rect)

    pygame.display.update()

pygame.quit()

import pygame

# 1. Initialize Pygame and the display window
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

def create_sprite_with_mask(color, size, shape="circle"):
    """
    Creates a surface (image), its bounding rectangle, and a collision mask.
    """
    # Create a surface with SRCALPHA to support transparency (the 'A' in RGBA)
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    
    if shape == "circle":
        pygame.draw.circle(surf, color, (size//2, size//2), size//2)
    else:
        # Draw a triangle to create transparent areas in the corners of the square surface
        pygame.draw.polygon(surf, color, [(size//2, 0), (size, size), (0, size)])
    
    rect = surf.get_rect()
    
    # 2. Generate a Mask: This treats transparent pixels as 'empty' and colored pixels as 'solid'
    mask = pygame.mask.from_surface(surf)
    
    return surf, rect, mask

# Create the stationary target (Triangle/Star) and the player (Circle)
target_surf, target_rect, target_mask = create_sprite_with_mask((255, 0, 0), 100, "star")
target_rect.center = (300, 200)

player_surf, player_rect, player_mask = create_sprite_with_mask((0, 255, 0), 80, "circle")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 3. Update player position to follow the mouse cursor
    player_rect.center = pygame.mouse.get_pos()

    # 4. Calculate the Offset
    # mask.overlap requires the distance between the top-left corners of the two masks
    offset = (target_rect.x - player_rect.x, target_rect.y - player_rect.y)

    # 5. Pixel-Perfect Collision Check
    # overlap() returns the first point of contact (x, y) or None if no collision
    if player_mask.overlap(target_mask, offset):
        bg_color = (50, 0, 0)  # Turn background dark red on collision
    else:
        bg_color = (30, 30, 30) # Default dark grey

    # 6. Draw everything to the screen
    screen.fill(bg_color)
    screen.blit(target_surf, target_rect)
    screen.blit(player_surf, player_rect)
    
    pygame.display.flip()
    clock.tick(60) # Maintain 60 Frames Per Second

pygame.quit()

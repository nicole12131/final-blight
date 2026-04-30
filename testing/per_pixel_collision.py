import pygame

# 1. Initialize Pygame and the display window
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

def pixel_perfect_collision(mask1, mask2, offset):
    #Checks for pixel-perfect collision between two masks given an offset.
    #Returns True if there's a collision, False otherwise.
    
    return mask1.overlap(mask2, offset) is not None

test_player = pygame.Surface((50, 50), pygame.SRCALPHA)
test_map = pygame.Surface((200, 200), pygame.SRCALPHA)

running = True

def move(player_rect, keys):
    speed = 5
    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed
    if keys[pygame.K_UP]:
        player_rect.y -= speed
    if keys[pygame.K_DOWN]:
        player_rect.y += speed

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    move(test_player.get_rect(), keys)

    # Create masks for collision detection
    player_mask = pygame.mask.from_surface(test_player)
    map_mask = pygame.mask.from_surface(test_map)

    # Calculate offset between player and map
    offset = (test_player.get_rect().x - test_map.get_rect().x, 
              test_player.get_rect().y - test_map.get_rect().y)

    # Check for collision
    collision = pixel_perfect_collision(player_mask, map_mask, offset)

    # Clear screen
    screen.fill((255, 255, 255))

    # Draw the map and player
    screen.blit(test_map, (100, 100))
    screen.blit(test_player, (150, 150))

    # Display collision status
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Collision: {collision}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
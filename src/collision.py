import pygame


def body_collision(character, layer):
    #Simple per-pixel collision detection for wall layers only.
    #Only WallLayer types can collide, and we check the center pixel of the character.
    
    # Only wall layers can collide
    if not hasattr(layer, 'collidable') or not layer.collidable:
        return False
    
    if not layer.mask:
        return False

    # Get the world position (center of character)
    world_x = int(character.world_x)
    world_y = int(character.world_y)
    
    # Check bounds
    if world_x < 0 or world_y < 0 or world_x >= layer.image_size[0] or world_y >= layer.image_size[1]:
        return False
    
    # Check the single center pixel
    try:
        pixel_value = layer.mask.get_at((world_x, world_y))
        return pixel_value > 0  # Any non-zero alpha means collision
    except (IndexError, ValueError):
        return False


def check_collision(character, layers):
    #Check if the character collides with any wall layer.
    
    for layer in layers:
        if body_collision(character, layer):
            return True
    return False

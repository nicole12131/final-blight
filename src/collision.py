import pygame


def body_collision(character, layer):
    """
    Check if the character's body collides with the layer using pixel-by-pixel checking.
    """
    # Only wall layers can collide
    if not hasattr(layer, 'collidable') or not layer.collidable:
        return False
    
    if not layer.mask:
        return False

    # Get character body bounds in world coordinates
    body_width, body_height = character.image.get_size()  # Use sprite size
    body_left = int(character.world_x - body_width // 2)
    body_top = int(character.world_y - body_height // 2)
    body_right = body_left + body_width
    body_bottom = body_top + body_height
    
    # Check bounds
    if (body_right <= 0 or body_bottom <= 0 or 
        body_left >= layer.image_size[0] or body_top >= layer.image_size[1]):
        return False
    
    # Clip to layer bounds
    check_left = max(0, body_left)
    check_top = max(0, body_top)
    check_right = min(layer.image_size[0], body_right)
    check_bottom = min(layer.image_size[1], body_bottom)
    
    # Check pixels in the overlapping area
    for x in range(check_left, check_right):
        for y in range(check_top, check_bottom):
            if layer.mask.get_at((x, y)) > 0:
                return True
    
    return False


def check_collision(character, layers):
    """
    Check if the character collides with any wall layer.
    """
    for layer in layers:
        if body_collision(character, layer):
            return True
    return False

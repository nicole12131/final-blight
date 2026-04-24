import pygame

def foot_collision(character, layer):
    # Create a tiny mask the size of the foot hitbox.
    # This is used to detect if the player's FEET are touching a layer.
    foot_mask = pygame.Mask(character.hitbox.size, fill=True)

    # Convert foot hitbox position into the layer's coordinate space.
    offset = (
        character.hitbox.left - layer.rect.left,
        character.hitbox.top - layer.rect.top
    )

    # Returns True if the foot mask overlaps solid pixels in the layer.
    return layer.mask.overlap(foot_mask, offset) is not None


def body_collision(character, layer, rect=None):
    # Choose which rectangle to test (body_rect by default).
    target_rect = rect if rect else character.body_rect

    # Convert body rectangle position into the layer's coordinate space.
    offset = (
        target_rect.left - layer.rect.left,
        target_rect.top - layer.rect.top
    )

    # Returns True if the player's BODY overlaps solid pixels in the layer.
    return layer.mask.overlap(character.body_mask, offset) is not None


def get_support_layer(character, layers):
    # Finds the layer the player is currently STANDING on.
    # Only layers at the same Z-height can support the player.
    for layer in layers:
        if layer.z == character.z:
            if foot_collision(character, layer):
                return layer
    return None


def get_blocking_layers(character, layers, old_body_rect=None):
    blocking = []

    for layer in layers:
        # Layers BELOW or EQUAL to the player's Z cannot block movement.
        # This prevents the player from colliding with the layer they stand on.
        if layer.z <= character.z:
            continue

        # Layers ABOVE the player can block movement.
        # If the player's BODY overlaps a higher layer, it's a wall.
        if body_collision(character, layer):
            blocking.append(layer)

    return blocking


def check_collision(character, layers, old_body_rect=None):
    # Returns True if ANY higher layer is blocking the player's movement.
    return len(get_blocking_layers(character, layers, old_body_rect)) > 0

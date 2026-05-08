import pygame


def body_collision(character, layer, rect=None):
    # Only collidable layers should be tested for body overlap.
    if not getattr(layer, 'collidable', False):
        return False

    target_rect = rect if rect else character.body_rect
    offset = (
        target_rect.left - layer.rect.left,
        target_rect.top - layer.rect.top
    )
    return layer.mask.overlap(character.body_mask, offset) is not None


def check_collision(character, layers, old_body_rect=None):
    # Return True if any layer is blocking the player's movement.
    for layer in layers:
        if body_collision(character, layer):
            return True
    return False

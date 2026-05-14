import pygame


def _character_mask_and_offset(character):
    """Return (mask, (left, top)) for the character in world coordinates.

    Uses the rendered `character.image` surface so transparent pixels are
    respected. The returned (left, top) is the top-left of the mask within
    world space.
    """
    # Prefer a `get_collision_mask` helper if provided by the character
    if hasattr(character, 'get_collision_mask'):
        mask = character.get_collision_mask()
    else:
        mask = pygame.mask.from_surface(character.image)
    w, h = mask.get_size()
    left = int(character.world_x - w // 2)
    top = int(character.world_y - h // 2)
    return mask, (left, top)


def body_collision(character, layer):
    """Return True if the character overlaps non-transparent pixels in `layer`.

    Only layers with `collidable=True` are considered. The layer's mask is
    expected to represent the entire world image (world coordinates).
    """
    if not getattr(layer, 'collidable', False):
        return False
    if not getattr(layer, 'mask', None):
        return False

    char_mask, _ = _character_mask_and_offset(character)
    w, h = char_mask.get_size()

    # Use layer's collision conversion if available (parallax/world offsets).
    if hasattr(layer, 'get_collision_point'):
        cx, cy = layer.get_collision_point(character.world_x, character.world_y)
    else:
        cx, cy = int(character.world_x), int(character.world_y)

    left = int(cx - w // 2)
    top = int(cy - h // 2)

    # Quick-out if completely outside
    if left + w <= 0 or top + h <= 0:
        return False
    if left >= layer.image_size[0] or top >= layer.image_size[1]:
        return False

    return layer.mask.overlap(char_mask, (left, top)) is not None


def check_collision(character, layers):
    """Return True if the character collides with any collidable wall layer."""
    for layer in layers:
        if body_collision(character, layer):
            return True
    return False


def colliding_layers(character, layers):
    """Return list of (layer, overlap_point) where character overlaps a layer.

    Useful for debugging. `overlap_point` is the point returned by Mask.overlap
    (coordinates relative to the layer mask).
    """
    hits = []
    for layer in layers:
        if not getattr(layer, 'collidable', False):
            continue
        if not getattr(layer, 'mask', None):
            continue
        char_mask, (left, top) = _character_mask_and_offset(character)
        if left + char_mask.get_size()[0] <= 0 or top + char_mask.get_size()[1] <= 0:
            continue
        if left >= layer.image_size[0] or top >= layer.image_size[1]:
            continue
        p = layer.mask.overlap(char_mask, (left, top))
        if p:
            hits.append((layer, p))
    return hits

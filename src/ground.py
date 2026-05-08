import pygame
import os


class BaseLayer:
    # Base class for drawable layers in the world.
    def __init__(self, image_path=None, rect=None, z=0, collidable=False, draw_order=0):
        if image_path and os.path.exists(image_path):
            self.image = pygame.image.load(image_path).convert_alpha()
            if rect is None:
                self.rect = self.image.get_rect(topleft=(0, 0))
            else:
                self.rect = rect
        else:
            # Fallback: create a surface if no image or image missing
            if rect is None:
                self.rect = pygame.Rect(0, 0, 360, 240)  # Default size
            else:
                self.rect = rect
            self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            # Optional: fill with a placeholder color
            self.image.fill((50, 50, 50, 100))  # Semi-transparent gray
        self.z = z
        self.collidable = collidable
        self.draw_order = draw_order
        self.mask = pygame.mask.from_surface(self.image, 1) if collidable else None

    def scroll(self, dx, dy):
        # Move the layer when the world scrolls.
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        # Render the layer onto the target surface.
        surface.blit(self.image, self.rect)


class GroundLayer(BaseLayer):
    # Ground is under the player and has no collision. Loads from PNG.
    def __init__(self, image_path, rect=None, z=0):
        super().__init__(image_path=image_path, rect=rect, z=z, collidable=False, draw_order=0)


class WallLayer(BaseLayer):
    # Wall uses per-pixel collision from PNG; transparent areas do not collide.
    def __init__(self, image_path, rect=None, z=0):
        super().__init__(image_path=image_path, rect=rect, z=z, collidable=True, draw_order=1)


class MiscLayer(BaseLayer):
    # Misc is a decorative layer drawn above the player and does not collide. Loads from PNG.
    def __init__(self, image_path, rect=None, z=0):
        super().__init__(image_path=image_path, rect=rect, z=z, collidable=False, draw_order=2)


class SkyBoxLayer(BaseLayer):
    # Sky box is a top overlay that appears above the player. Uses color if no image.
    def __init__(self, rect, z=0, color=(100, 180, 255, 140)):
        super().__init__(image_path=None, rect=rect, z=z, collidable=False, draw_order=3)
        self.image.fill(color)

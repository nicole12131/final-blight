import pygame

class GroundLayer:
    def __init__(self, image_path, z):
        # Load the ground image (this layer's visual appearance).
        self.image = pygame.image.load(image_path).convert_alpha()

        # The layer's position on screen.
        # Starts at (0,0) and moves when the world scrolls.
        self.rect = self.image.get_rect(topleft=(0, 0))

        # Pixel-perfect collision mask for this layer.
        # Every non-transparent pixel becomes "solid".
        self.mask = pygame.mask.from_surface(self.image, 1)

        # The height (Z-level) of this layer.
        # Higher Z = higher elevation in the world.
        self.z = z

    def scroll(self, dx, dy):
        # Move the layer on screen.
        # This simulates the player moving through the world.
        self.rect.x += dx
        self.rect.y += dy

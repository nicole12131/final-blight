import pygame
import os


class BaseLayer:
    # Base class for drawable layers in the world.
    # Supports large images (16k) with viewport-based rendering.
    def __init__(self, image_path=None, rect=None, z=0, collidable=False, draw_order=0, parallax_factor=1.0):
        self.original_image = None
        self.parallax_factor = parallax_factor
        self.world_offset_x = 0  # Track world position for large images
        self.world_offset_y = 0
        
        if image_path and os.path.exists(image_path):
            try:
                self.original_image = pygame.image.load(image_path).convert_alpha()
                # For large images, we store the full image and render via viewport
                self.image_size = self.original_image.get_size()
                if rect is None:
                    self.rect = pygame.Rect(0, 0, self.image_size[0], self.image_size[1])
                else:
                    self.rect = rect
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")
                self._create_fallback(rect)
        else:
            # Fallback: create a surface if no image or image missing
            self._create_fallback(rect)
        
        self.z = z
        self.collidable = collidable
        self.draw_order = draw_order
        # Create mask from the original image for collision detection
        # Use a high threshold so only fully opaque pixels count as solid.
        # `threshold=254` means only alpha==255 will be considered opaque.
        self.mask = pygame.mask.from_surface(self.original_image, 254) if (self.collidable and self.original_image) else None

    def _create_fallback(self, rect):
        #Create a fallback surface.
        if rect is None:
            rect = pygame.Rect(0, 0, 360, 240)
        self.rect = rect
        self.original_image = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        self.original_image.fill((50, 50, 50, 100))
        self.image_size = (rect.width, rect.height)

    def scroll(self, dx, dy):
        # Update world position for viewport rendering
        self.world_offset_x += dx * self.parallax_factor
        self.world_offset_y += dy * self.parallax_factor
        # Clamp to world bounds to prevent infinite scrolling
        self.world_offset_x = max(0, min(self.world_offset_x, max(0, self.image_size[0] - 360)))
        self.world_offset_y = max(0, min(self.world_offset_y, max(0, self.image_size[1] - 240)))

    def get_collision_point(self, world_x, world_y):
        
        #Get the pixel coordinates in the layer's mask for collision detection.
        #Converts world coordinates to layer image coordinates.
        #For collision detection, we use world coordinates directly since the image represents the entire world.
        
        # For collision detection, use world coordinates directly (no viewport offset)
        layer_x = int(world_x)
        layer_y = int(world_y)
        return layer_x, layer_y

    def draw(self, surface):
        # Render the visible portion of the layer to the viewport
        if not self.original_image:
            return
        
        viewport_width, viewport_height = surface.get_size()
        
        # Calculate source rectangle from the original image
        src_rect = pygame.Rect(
            int(self.world_offset_x),
            int(self.world_offset_y),
            viewport_width,
            viewport_height
        )
        
        # Clamp source rectangle to image bounds
        src_rect.x = max(0, min(src_rect.x, self.image_size[0] - 1))
        src_rect.y = max(0, min(src_rect.y, self.image_size[1] - 1))
        src_rect.width = min(src_rect.width, self.image_size[0] - src_rect.x)
        src_rect.height = min(src_rect.height, self.image_size[1] - src_rect.y)
        
        # Draw the cropped portion to the target surface
        surface.blit(self.original_image, (0, 0), src_rect)


class GroundLayer(BaseLayer):
    # Ground is under the player and all other layers. No collision. Draws first.
    def __init__(self, image_path, rect=None, z=0, parallax_factor=1.0):
        super().__init__(image_path=image_path, rect=rect, z=z, collidable=False, draw_order=0, parallax_factor=parallax_factor)


class WallLayer(BaseLayer):
    # Wall is main collision layer. Uses per-pixel collision from PNG; transparent areas do not collide.
    # Draws above ground, below player and misc.
    def __init__(self, image_path, rect=None, z=0, parallax_factor=1.0):
        super().__init__(image_path=image_path, rect=rect, z=z, collidable=True, draw_order=1, parallax_factor=parallax_factor)


class MiscLayer(BaseLayer):
    # Misc is drawn above player (e.g., bushes, foliage). High draw_order ensures it draws after player.
    # Does not collide. Draws on top of everything except sky.
    def __init__(self, image_path, rect=None, z=0, parallax_factor=1.0):
        super().__init__(image_path=image_path, rect=rect, z=z, collidable=False, draw_order=10, parallax_factor=parallax_factor)


class SkyBoxLayer(BaseLayer):
    # Sky box is a top overlay that appears above the player. Uses color if no image.
    def __init__(self, rect, z=0, color=(100, 180, 255, 140), parallax_factor=1.0):
        super().__init__(image_path=None, rect=rect, z=z, collidable=False, draw_order=3, parallax_factor=parallax_factor)
        if self.original_image:
            self.original_image.fill(color)
        else:
            # Create a solid color surface
            self.original_image = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            self.original_image.fill(color)
            self.image_size = (rect.width, rect.height)

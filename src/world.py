# World manages the scrolling of layers in the scene.
class World:
    def __init__(self, layers, world_width=16384, world_height=16384, viewport_width=360, viewport_height=240):
        self.layers = layers
        self.world_width = world_width
        self.world_height = world_height
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        
        # Camera position tracks the top-left corner of the viewport
        self.camera_x = 0
        self.camera_y = 0

    # Scroll every layer to simulate player movement.
    def scroll(self, dx, dy):
        # Update camera position based on player movement
        new_camera_x = max(0, min(self.camera_x + dx, self.world_width - self.viewport_width))
        new_camera_y = max(0, min(self.camera_y + dy, self.world_height - self.viewport_height))
        
        actual_dx = new_camera_x - self.camera_x
        actual_dy = new_camera_y - self.camera_y
        
        self.camera_x = new_camera_x
        self.camera_y = new_camera_y
        
        # Scroll all layers with the actual movement
        for layer in self.layers:
            layer.scroll(actual_dx, actual_dy)
    
    def get_camera_position(self):
        """Get current camera position."""
        return self.camera_x, self.camera_y
    
    def set_camera_position(self, x, y):
        """Set camera position directly."""
        self.camera_x = max(0, min(x, self.world_width - self.viewport_width))
        self.camera_y = max(0, min(y, self.world_height - self.viewport_height))


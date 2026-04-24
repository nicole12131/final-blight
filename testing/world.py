class World:
    def __init__(self, layers):
        # Store all ground layers (floors, platforms, walls).
        self.layers = layers

    def scroll(self, dx, dy):
        # Move every layer by the same amount.
        # This creates the illusion that the player is moving.
        for layer in self.layers:
            layer.scroll(dx, dy)

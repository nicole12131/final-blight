# World manages the scrolling of layers in the scene.
class World:
    def __init__(self, layers):
        self.layers = layers

    # Scroll every layer to simulate player movement.
    def scroll(self, dx, dy):
        for layer in self.layers:
            layer.scroll(dx, dy)

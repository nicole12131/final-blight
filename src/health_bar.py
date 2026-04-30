import pygame

class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.health = max_health

    def update(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height))

        health_ratio = self.health / self.max_health
        pygame.draw.rect(
            surface,
            (0, 255, 0),
            (self.x, self.y, self.width * health_ratio, self.height)
        )
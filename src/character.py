import pygame
from datetime import datetime
try:
    from .collision import check_collision
except ImportError:
    from collision import check_collision


# GameCharacter controls movement and collision interactions in an open world.
class GameCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y, width=32, height=48, color=(0, 140, 255)):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

        self.world_x = x
        self.world_y = y

        self.body_rect = pygame.Rect(0, 0, 24, 24)
        self.body_mask = pygame.Mask(self.body_rect.size, fill=True)

        self.speed = 4

        self.update_hitbox()

    # Keep the body hitbox aligned to the sprite.
    def update_hitbox(self):
        self.body_rect.centerx = self.rect.centerx
        self.body_rect.centery = self.rect.centery

    # Try moving the player while rolling back on collision.
    def try_move(self, dx, dy, world, layers):
        if dx == 0 and dy == 0:
            return

        old_positions = [(layer.rect.x, layer.rect.y) for layer in world.layers]
        old_world_x, old_world_y = self.world_x, self.world_y

        world.scroll(-dx, -dy)
        self.world_x += dx
        self.world_y += dy
        self.update_hitbox()

        if check_collision(self, layers):
            for layer, (old_x, old_y) in zip(world.layers, old_positions):
                layer.rect.x, layer.rect.y = old_x, old_y
            self.world_x, self.world_y = old_world_x, old_world_y
            self.update_hitbox()

    # Update movement each frame.
    def update(self, keys, world, layers):
        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * self.speed
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * self.speed

        self.try_move(dx, 0, world, layers)
        self.try_move(0, dy, world, layers)


# Simple data structures for persisted characters.
class Character:
    def __init__(self, name, race, char_class, level=1, attributes=None, skills=None):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.level = level
        self.attributes = attributes or {}
        self.skills = set(skills or [])
        self.created_date = datetime.now()

    def get_total_stats(self):
        return sum(self.attributes.values())


class CharacterRoster:
    def __init__(self):
        self.characters = []

    def add_character(self, character):
        self.characters.append(character)

    def __iter__(self):
        return iter(self.characters)

    def __len__(self):
        return len(self.characters)

    def get_rows(self):
        rows = []
        for character in self.characters:
            row = {
                'Name': character.name,
                'Race': character.race,
                'Class': character.char_class,
                'Level': character.level,
                'skills_count': len(character.skills)
            }
            row.update(character.attributes)
            rows.append(row)
        return rows

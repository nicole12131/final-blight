import pygame
from datetime import datetime
try:
    from .collision import check_collision
except ImportError:
    from collision import check_collision


# GameCharacter controls movement and collision interactions in an open world.
class GameCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y, width=10, height=10, color=(0, 140, 255)):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

        self.world_x = x
        self.world_y = y

        self.body_rect = pygame.Rect(0, 0, width, height)

        self.speed = 4

        self.update_hitbox()

    # Keep the body hitbox aligned to the sprite.
    def update_hitbox(self):
        self.body_rect.centerx = self.rect.centerx
        self.body_rect.centery = self.rect.centery

    def get_collision_mask(self):
        #Return a mask generated from the character surface (respecting alpha).
        return pygame.mask.from_surface(self.image)

    # Try moving the player while rolling back on collision.
    def try_move(self, dx, dy, world, layers, collision_enabled=True):
        if dx == 0 and dy == 0:
            return

        # Save layer world offsets (for viewport-based rendering)
        old_offsets = [(layer.world_offset_x, layer.world_offset_y) for layer in world.layers]
        old_world_x, old_world_y = self.world_x, self.world_y

        world.scroll(-dx, -dy)
        self.world_x += dx
        self.world_y += dy
        self.update_hitbox()

        if collision_enabled and check_collision(self, layers):
            # Debug: print collision info
            print(f"COLLISION DETECTED at ({self.world_x}, {self.world_y})")
            for i, layer in enumerate(layers):
                if hasattr(layer, 'collidable') and layer.collidable and layer.mask:
                    world_x = int(self.world_x)
                    world_y = int(self.world_y)
                    if 0 <= world_x < layer.image_size[0] and 0 <= world_y < layer.image_size[1]:
                        try:
                            pixel_value = layer.mask.get_at((world_x, world_y))
                            print(f"  Layer {i}: ({world_x}, {world_y}) = {pixel_value}")
                        except:
                            print(f"  Layer {i}: Error reading pixel")
            
            # Collision detected - restore previous state
            for layer, (old_x, old_y) in zip(world.layers, old_offsets):
                layer.world_offset_x, layer.world_offset_y = old_x, old_y
            self.world_x, self.world_y = old_world_x, old_world_y
            self.update_hitbox()

    # Update movement each frame.
    def update(self, keys, world, layers, collision_enabled=True):
        dx = (keys[pygame.K_a] - keys[pygame.K_d]) * self.speed
        dy = (keys[pygame.K_w] - keys[pygame.K_s]) * self.speed

        self.try_move(dx, 0, world, layers, collision_enabled)
        self.try_move(0, dy, world, layers, collision_enabled)


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

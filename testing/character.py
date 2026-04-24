import pygame
from collision import check_collision, get_support_layer, foot_collision

class Character(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()

        # Load sprite and place it centered on screen.
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(400, 300))

        # World-space position (logical position, not screen position).
        self.world_x = x
        self.world_y = y

        # FEET hitbox: small rectangle used for standing and landing detection.
        self.hitbox = pygame.Rect(0, 0, 16, 4)

        # BODY hitbox: used for detecting walls above the player.
        self.body_rect = pygame.Rect(0, 0, 24, 24)
        self.body_mask = pygame.Mask(self.body_rect.size, fill=True)

        # Vertical (Z) movement system.
        self.z = 0
        self.jump_power = 12
        self.vertical_speed = 0
        self.gravity = 1
        self.is_jumping = False
        self.jump_pressed = False

        # Horizontal movement speed.
        self.speed = 5

        # Sync hitboxes to sprite position.
        self.update_hitbox()

    def update_hitbox(self):
        # Align hitboxes to the sprite's screen position.
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom

        # Body hitbox sits slightly above the feet.
        self.body_rect.centerx = self.rect.centerx
        self.body_rect.bottom = self.rect.bottom - 2

    def find_landing_layer(self, layers, old_z):
        # Finds the highest layer the player can land on while falling.
        candidates = [
            l for l in layers
            if foot_collision(self, l)
            and l.z < old_z
            and l.z >= self.z
        ]
        return max(candidates, key=lambda l: l.z) if candidates else None

    def apply_gravity(self, layers):
        # Check if player is standing on a layer at their current Z.
        support = get_support_layer(self, layers)

        # If not jumping and above ground with no support, start falling.
        if not self.is_jumping and self.z > 0 and support is None:
            self.is_jumping = True
            self.vertical_speed = -2  # Begin falling.

        if self.is_jumping:
            old_z = self.z

            # Apply vertical movement.
            self.z += self.vertical_speed
            self.vertical_speed -= self.gravity

            # If falling downward, check for landing.
            if self.vertical_speed < 0:
                landing = self.find_landing_layer(layers, old_z)
                if landing:
                    # Snap to landing layer height.
                    self.z = landing.z
                    self.is_jumping = False
                    self.vertical_speed = 0
                    return

            # If we hit ground level, stop falling.
            if self.z <= 0:
                self.z = 0
                self.is_jumping = False
                self.vertical_speed = 0

    def try_move(self, dx, dy, world, layers):
        # Skip if no movement.
        if dx == 0 and dy == 0:
            return

        # Save world positions for rollback.
        old_pos = [(l.rect.x, l.rect.y) for l in world.layers]
        old_world_x, old_world_y = self.world_x, self.world_y

        # Scroll world opposite to movement.
        world.scroll(-dx, -dy)

        # Update logical world position.
        self.world_x += dx
        self.world_y += dy

        # Sync hitboxes.
        self.update_hitbox()

        # If movement hits a wall, rollback.
        if check_collision(self, layers):
            for l, (ox, oy) in zip(world.layers, old_pos):
                l.rect.x, l.rect.y = ox, oy

            self.world_x, self.world_y = old_world_x, old_world_y
            self.update_hitbox()

    def update(self, keys, world, layers):
        # Handle jump input (single press).
        if keys[pygame.K_SPACE] and not self.jump_pressed:
            if not self.is_jumping:
                self.is_jumping = True
                self.vertical_speed = self.jump_power
            self.jump_pressed = True

        if not keys[pygame.K_SPACE]:
            self.jump_pressed = False

        # Apply gravity and landing logic.
        self.apply_gravity(layers)

        # Horizontal movement input.
        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * self.speed
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * self.speed

        # Move horizontally and vertically with collision rollback.
        self.try_move(dx, 0, world, layers)
        self.try_move(0, dy, world, layers)

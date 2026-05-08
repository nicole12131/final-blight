import pygame


# Dodge helper class for hitbox overlap checks only.
class DodgePlayer:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, 50, 50)

    # Compare two rectangles and report whether the hitboxes overlap.
    def check_overlap(self, attacker_rect, target_rect, attacker_name='Player', target_name='Enemy'):
        hitbox = pygame.Rect(attacker_rect.right, attacker_rect.y, 40, attacker_rect.height)

        if hitbox.colliderect(target_rect):
            print(f"{attacker_name} hit {target_name}! Attack box overlapped.")
            return True
        print(f"{attacker_name} missed {target_name}'s attack box.")
        return False

    # Check if either side missed when comparing both hitboxes.
    def check_miss(self, player_rect, enemy_rect):
        player_hit = self.check_overlap(player_rect, enemy_rect, 'Player', 'Enemy')
        enemy_hit = self.check_overlap(enemy_rect, player_rect, 'Enemy', 'Player')
        return not (player_hit or enemy_hit)

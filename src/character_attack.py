import pygame


# Simple attack helper class for the player.
class AttackPlayer:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, 50, 50)
        self.combo_step = 0
        self.last_attack_time = 0
        self.combo_timeout = 500
        self.is_attacking = False
        self.attack_duration = 200
        self.attack_timer = 0

    # Perform a hitbox-based attack toward the enemy.
    def attack(self, attacker_rect, enemy_rect):
        now = pygame.time.get_ticks()

        if now - self.last_attack_time > self.combo_timeout:
            self.combo_step = 0

        self.is_attacking = True
        self.attack_timer = now
        self.last_attack_time = now

        hitbox = pygame.Rect(attacker_rect.right, attacker_rect.y, 40, attacker_rect.height)

        if self.combo_step == 0:
            print("Attack 1: Light Strike")
            self.check_hit(hitbox, enemy_rect, damage=10)
            self.combo_step = 1
        elif self.combo_step == 1:
            print("Attack 2: Mid Strike")
            self.check_hit(hitbox, enemy_rect, damage=15)
            self.combo_step = 2
        elif self.combo_step == 2:
            print("Attack 3: Heavy Finisher!")
            self.check_hit(hitbox, enemy_rect, damage=30)
            self.combo_step = 0

    # Check whether the attack hit the enemy rectangle.
    def check_hit(self, hitbox, enemy_rect, damage):
        if hitbox.colliderect(enemy_rect):
            print(f"STRIKE Dealt {damage} damage.")
        else:
            print("Missed the target.")


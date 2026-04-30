import pygame

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, 50, 50)
        self.combo_step = 0
        self.last_attack_time = 0
        self.combo_timeout = 500  # Milliseconds to hit Z again for next combo
        self.is_attacking = False
        self.attack_duration = 200 # How long the hitbox stays active
        self.attack_timer = 0

    def attack(self, enemy_rect):
        now = pygame.get_ticks()
        
        # Check if we are starting a new combo or continuing one
        if now - self.last_attack_time > self.combo_timeout:
            self.combo_step = 0 # Reset if too much time passed
        
        self.is_attacking = True
        self.attack_timer = now
        self.last_attack_time = now

        # Define hitbox based on combo step
        # Offset the hitbox in front of the player
        hitbox = pygame.Rect(self.rect.right, self.rect.y, 40, 50)
        
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
            self.combo_step = 0 # Reset after finisher

    def check_hit(self, hitbox, enemy_rect, damage):
        if hitbox.colliderect(enemy_rect):
            print(f"STRICK Dealt {damage} damage.")
        else:
            print("wow you need to aim buddy ")


pygame.init()
player = Player()
enemy_rect = pygame.Rect(140, 100, 50, 50) # Positioned near the player
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Trigger attack on KEYDOWN
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                player.attack(enemy_rect)

    # Simple logic to end the "attack state" visually
    if player.is_attacking and pygame.get_ticks() - player.attack_timer > player.attack_duration:
        player.is_attacking = False

    clock.tick(60)
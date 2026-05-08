import os
import pygame

try:
    from .character import GameCharacter
    from .ground import GroundLayer, WallLayer, MiscLayer, SkyBoxLayer
    from .health_bar import HealthBar
    from .music import load_music, stop_music, sfx
    from .world import World
    from .character_attack import AttackPlayer
    from .dodge import DodgePlayer
    from .skill_stat_manager import get_stats_for_class
    from .data_manager import DataManager
except ImportError:
    from character import GameCharacter
    from ground import GroundLayer, WallLayer, MiscLayer, SkyBoxLayer
    from health_bar import HealthBar
    from music import load_music, stop_music, sfx
    from world import World
    from character_attack import AttackPlayer
    from dodge import DodgePlayer
    from skill_stat_manager import get_stats_for_class
    from data_manager import DataManager

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'assets'))
MUSIC_FILE = os.path.join(ASSETS_DIR, 'music', 'Hero_theme_loop.mp3')
SFX_FILE = os.path.join(ASSETS_DIR, 'music', 'Hero_theme_loop.mp3')

WIDTH, HEIGHT = 360, 240
WHITE = (240, 240, 240)
ENEMY_COLOR = (180, 50, 50)
PLAYER_COLOR = (0, 140, 255)


def load_game_audio():
    # Start looping game music if the asset exists.
    if os.path.exists(MUSIC_FILE):
        load_music(MUSIC_FILE)
    else:
        print(f"Music not found: {MUSIC_FILE}")


def create_game():
    # Initialize Pygame and create the game objects.
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Final Blight Demo')
    font = pygame.font.SysFont(None, 20)

    # Placeholder PNG paths - replace with your actual layer images
    ground_png = os.path.join(ASSETS_DIR, 'layers', 'ground.png')
    wall_png = os.path.join(ASSETS_DIR, 'layers', 'wall.png')
    misc_png = os.path.join(ASSETS_DIR, 'layers', 'misc.png')

    sky_layer = SkyBoxLayer(pygame.Rect(0, 0, WIDTH, 80), z=100, color=(100, 180, 255, 160))

    world_layers = [
        GroundLayer(ground_png, rect=pygame.Rect(0, 0, WIDTH, HEIGHT)),
        WallLayer(wall_png, rect=pygame.Rect(120, 0, 120, HEIGHT)),
        MiscLayer(misc_png, rect=pygame.Rect(50, 50, 100, 50)),
    ]

    world = World(world_layers)
    player = GameCharacter(WIDTH // 2, HEIGHT // 2, width=18, height=28, color=PLAYER_COLOR)
    health_bar = HealthBar(8, 8, 120, 16, max_health=100)
    enemy_rect = pygame.Rect(WIDTH - 60, HEIGHT - 60, 24, 40)

    attack_demo = AttackPlayer()
    dodge_demo = DodgePlayer()
    stats = get_stats_for_class('Zan', 1)
    _ = DataManager(data_dir=os.path.join(BASE_DIR, 'game_data'))

    return screen, font, world, player, health_bar, enemy_rect, attack_demo, dodge_demo, stats, sky_layer


def main():
    screen, font, world, player, health_bar, enemy_rect, attack_demo, dodge_demo, stats, sky_layer = create_game()
    load_game_audio()

    clock = pygame.time.Clock()
    running = True

    while running:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    attack_demo.attack(player.rect, enemy_rect)
                    if player.rect.colliderect(enemy_rect):
                        health_bar.update(10)
                elif event.key == pygame.K_f:
                    if os.path.exists(SFX_FILE):
                        sfx(SFX_FILE)

        player.update(keys, world, world.layers)

        screen.fill((18, 18, 38))
        for layer in sorted(world.layers, key=lambda l: l.draw_order):
            layer.draw(screen)

        screen.blit(player.image, player.rect)
        sky_layer.draw(screen)
        pygame.draw.rect(screen, ENEMY_COLOR, enemy_rect)
        health_bar.draw(screen)

        info_text = [
            'Move: WASD',
            'Attack: Z',
            'Play SFX: F',
            f"Enemy hits taken: {100 - health_bar.health}",
            f"Zan HP @ level 1: {stats.get('HP', 0)}",
        ]

        for idx, line in enumerate(info_text):
            surface = font.render(line, True, WHITE)
            screen.blit(surface, (8, 36 + idx * 18))

        if health_bar.health == 0:
            game_over = font.render('Game Over - press ESC to quit', True, (255, 50, 50))
            screen.blit(game_over, (20, HEIGHT // 2 - 10))

        if keys[pygame.K_ESCAPE]:
            running = False

        pygame.display.flip()
        clock.tick(60)

    stop_music()
    pygame.quit()


if __name__ == '__main__':
    main()

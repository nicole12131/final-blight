import os
import pygame
#implement font
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
    from .spawn_config import SpawnConfig
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
    from spawn_config import SpawnConfig

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'assets'))
MUSIC_FILE = os.path.join(ASSETS_DIR, 'music', 'Hero_theme_loop.mp3')
SFX_FILE = os.path.join(ASSETS_DIR, 'music', 'Hero_theme_loop.mp3')

WIDTH, HEIGHT = 360, 240
WHITE = (240, 240, 240)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
ENEMY_COLOR = (180, 50, 50)
PLAYER_COLOR = (0, 140, 255)

count = 0

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

    # Load spawn configuration
    spawn_config = SpawnConfig(os.path.join(BASE_DIR, 'spawn_config.json'))
    player_spawn_x, player_spawn_y = spawn_config.get_player_spawn()
    world_width, world_height = spawn_config.get_world_size()

    # Layer PNG paths - now supports 16k images
    ground_png = os.path.join(ASSETS_DIR, 'layers', 'ground.png')
    wall_png = os.path.join(ASSETS_DIR, 'layers', 'wall.png')
    misc_png = os.path.join(ASSETS_DIR, 'layers', 'misc.png')

    # Create layers with parallax factors from config
    ground_config = spawn_config.get_layer_config('ground')
    wall_config = spawn_config.get_layer_config('wall')
    misc_config = spawn_config.get_layer_config('misc')
    sky_config = spawn_config.get_layer_config('skybox')

    sky_layer = SkyBoxLayer(pygame.Rect(0, 0, WIDTH, 80), z=100, 
                           color=(100, 180, 255, 160),
                           parallax_factor=sky_config.get('parallax_factor', 1.0))

    world_layers = []
    
    # Ground layer (16k image, 1:1 parallax)
    if ground_config.get('enabled', True):
        world_layers.append(GroundLayer(ground_png, z=0, parallax_factor=ground_config.get('parallax_factor', 1.0)))
    
    # Wall layer (16k image, 1:1 parallax, collidable)
    if wall_config.get('enabled', True):
        wall_layer = WallLayer(wall_png, z=1, parallax_factor=wall_config.get('parallax_factor', 1.0))
        world_layers.append(wall_layer)
        print(f"Wall layer loaded: size={wall_layer.image_size}, has_mask={wall_layer.mask is not None}")
    
    # Misc layer (16k image, slightly slower parallax for depth)
    if misc_config.get('enabled', True):
        world_layers.append(MiscLayer(misc_png, z=2, parallax_factor=misc_config.get('parallax_factor', 1.0)))

    # Create world with 16k dimensions and viewport size
    world = World(world_layers, world_width=world_width, world_height=world_height, 
                  viewport_width=WIDTH, viewport_height=HEIGHT)
    
    # Create player at configured spawn point
    player = GameCharacter(WIDTH // 2, HEIGHT // 2, width=18, height=28, color=PLAYER_COLOR)
    player.world_x = player_spawn_x
    player.world_y = player_spawn_y
    
    health_bar = HealthBar(8, 8, 120, 16, max_health=100)
    enemy_rect = pygame.Rect(WIDTH - 60, HEIGHT - 60, 24, 40)

    attack_demo = AttackPlayer()
    dodge_demo = DodgePlayer()
    stats = get_stats_for_class('Zan', 1)
    _ = DataManager(data_dir=os.path.join(BASE_DIR, 'game_data'))

    return screen, font, world, player, health_bar, enemy_rect, attack_demo, dodge_demo, stats, sky_layer, spawn_config


def main():
    global collision_enabled
    screen, font, world, player, health_bar, enemy_rect, attack_demo, dodge_demo, stats, sky_layer, spawn_config = create_game()
    load_game_audio()

    clock = pygame.time.Clock()
    running = True
    collision_enabled = False  # Toggle for debugging

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
                elif event.key == pygame.K_p:
                    # Press P to print current spawn point and world position
                    print(f"Current player world position: ({player.world_x}, {player.world_y})")
                    print(f"Camera position: {world.get_camera_position()}")
                    print(f"Config spawn point: {spawn_config.get_player_spawn()}")
                elif event.key == pygame.K_o:
                    # Press O to save current position as new spawn point
                    spawn_config.set_player_spawn(int(player.world_x), int(player.world_y))
                    print(f"Spawn point updated to: ({int(player.world_x)}, {int(player.world_y)})")
                elif event.key == pygame.K_c:
                    # Press C to debug collision info
                    print(f"Player world pos: ({player.world_x}, {player.world_y})")
                    print(f"Player screen pos: ({player.rect.centerx}, {player.rect.centery})")
                    for i, layer in enumerate(world.layers):
                        if hasattr(layer, 'collidable') and layer.collidable:
                            world_x = int(player.world_x)
                            world_y = int(player.world_y)
                            print(f"Layer {i} ({type(layer).__name__}) collision point: ({world_x}, {world_y})")
                            if layer.mask and 0 <= world_x < layer.image_size[0] and 0 <= world_y < layer.image_size[1]:
                                center_value = layer.mask.get_at((world_x, world_y))
                                print(f"  Mask value at center: {center_value}")
                                print(f"  Image size: {layer.image_size}")
                            else:
                                print("  Out of bounds or no mask")
                        elif hasattr(layer, 'collidable'):
                            print(f"Layer {i} ({type(layer).__name__}) - not collidable")
                elif event.key == pygame.K_v:
                    # Press V to check if wall.png has any collision pixels
                    wall_layer = None
                    for layer in world.layers:
                        if isinstance(layer, WallLayer):
                            wall_layer = layer
                            break
                    
                    if wall_layer and wall_layer.mask:
                        print("Checking wall.png for collision pixels...")
                        print(f"Wall image size: {wall_layer.image_size}")
                        
                        # Check spawn point
                        spawn_x, spawn_y = spawn_config.get_player_spawn()
                        spawn_world_x, spawn_world_y = int(spawn_x), int(spawn_y)
                        if 0 <= spawn_world_x < wall_layer.image_size[0] and 0 <= spawn_world_y < wall_layer.image_size[1]:
                            spawn_value = wall_layer.mask.get_at((spawn_world_x, spawn_world_y))
                            print(f"Spawn point ({spawn_x}, {spawn_y}) -> world ({spawn_world_x}, {spawn_world_y}): {spawn_value}")
                        
                        # Check current player position
                        player_world_x, player_world_y = int(player.world_x), int(player.world_y)
                        if 0 <= player_world_x < wall_layer.image_size[0] and 0 <= player_world_y < wall_layer.image_size[1]:
                            player_value = wall_layer.mask.get_at((player_world_x, player_world_y))
                            print(f"Player pos ({player.world_x}, {player.world_y}) -> world ({player_world_x}, {player_world_y}): {player_value}")
                        
                        # Scan edges for collision
                        print("Scanning edges for collision...")
                        edges = [
                            ("Top", [(x, 0) for x in range(0, wall_layer.image_size[0], 500)]),
                            ("Bottom", [(x, wall_layer.image_size[1]-1) for x in range(0, wall_layer.image_size[0], 500)]),
                            ("Left", [(0, y) for y in range(0, wall_layer.image_size[1], 500)]),
                            ("Right", [(wall_layer.image_size[0]-1, y) for y in range(0, wall_layer.image_size[1], 500)]),
                        ]
                        
                        for edge_name, points in edges:
                            collision_count = 0
                            for x, y in points:
                                value = wall_layer.mask.get_at((x, y))
                                if value > 0:
                                    collision_count += 1
                            print(f"  {edge_name} edge: {collision_count}/{len(points)} collision pixels")
                    else:
                        print("Wall layer not found or no mask")
                elif event.key == pygame.K_x:
                    # Press X to teleport to left edge (should cause collision)
                    print("Teleporting to left edge...")
                    player.world_x = 50  # Near the left edge where collision was found
                    player.world_y = player.world_y  # Keep same Y
                    player.update_hitbox()
                    print(f"Teleported to ({player.world_x}, {player.world_y})")
                elif event.key == pygame.K_b:
                    # Press B to toggle collision on/off
                    collision_enabled = not collision_enabled
                    print(f"Collision {'ENABLED' if collision_enabled else 'DISABLED'}")

        # Update player movement
        player.update(keys, world, world.layers, collision_enabled)

        screen.fill((18, 18, 38))
        
        # Draw background layers (ground and wall - under player)
        for layer in sorted([l for l in world.layers if l.draw_order < 10], key=lambda l: l.draw_order):
            layer.draw(screen)

        screen.blit(player.image, player.rect)
        
        # Draw foreground layers (misc/bushes - above player)
        for layer in sorted([l for l in world.layers if l.draw_order >= 10], key=lambda l: l.draw_order):
            layer.draw(screen)

        sky_layer.draw(screen)
        pygame.draw.rect(screen, ENEMY_COLOR, enemy_rect)
        health_bar.draw(screen)

        # Debug: Show collision points if C is held
        if keys[pygame.K_c]:
            for layer in world.layers:
                if hasattr(layer, 'collidable') and layer.collidable and layer.mask:
                    # Use world coordinates directly for collision point
                    world_x, world_y = int(player.world_x), int(player.world_y)
                    # Convert to screen coordinates (relative to viewport)
                    screen_x = world_x - layer.world_offset_x
                    screen_y = world_y - layer.world_offset_y
                    
                    # Draw collision point (just center since we simplified to single point)
                    pygame.draw.circle(screen, (255, 0, 0), (int(screen_x), int(screen_y)), 3)  # Center

        info_text = [
            'Move: WASD',
            'Attack: Z',
            'Play SFX: F',
            'Print spawn: P',
            'Save spawn: O',
            'Debug collision: C',
            'Check wall pixels: V',
            'Test collision: X',
            f"Enemy hits taken: {100 - health_bar.health}",
            f"Zan HP @ level 1: {stats.get('HP', 0)}",
            'Press E to win ',
        ]

        for idx, line in enumerate(info_text):
            surface = font.render(line, True, WHITE)
            screen.blit(surface, (8, 36 + idx * 18))

        if health_bar.health == 0:
            game_over = font.render('Game Over - press ESC to quit', True, (255, 50, 50))
            screen.blit(game_over, (20, HEIGHT // 2 - 10))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            pygame.quit()

        if count >= 100:
            print("You Won! Ending game...")
            pygame.time.delay(2000)
            pygame.quit()

        if keys[pygame.K_ESCAPE]:
            running = False

        pygame.display.flip()
        clock.tick(60)

    stop_music()
    pygame.quit()


if __name__ == '__main__':
    main()

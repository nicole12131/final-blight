#!/usr/bin/env python3
#Comprehensive collision debugging script

import pygame
import os
import sys

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((360, 240))

# Import game modules
from src.character import GameCharacter
from src.ground import WallLayer
from src.world import World
from src.collision import check_collision, body_collision
from src.spawn_config import SpawnConfig

print("=" * 60)
print("COLLISION DIAGNOSTIC")
print("=" * 60)

# Load spawn config
spawn_config = SpawnConfig()
spawn_x, spawn_y = spawn_config.get_player_spawn()
print(f"\n1. SPAWN CONFIGURATION")
print(f"   Spawn point: ({spawn_x}, {spawn_y})")

# Create character
character = GameCharacter(spawn_x, spawn_y)
print(f"\n2. CHARACTER INITIALIZATION")
print(f"   World position: ({character.world_x}, {character.world_y})")
print(f"   Screen rect: {character.rect}")

# Load wall layer
wall_png = os.path.join(os.path.dirname(__file__), 'assets', 'layers', 'wall.png')
wall_layer = WallLayer(wall_png, z=1, parallax_factor=1.0)
wall_layer.collidable = True

print(f"\n3. WALL LAYER")
print(f"   Image path: {wall_png}")
print(f"   Image size: {wall_layer.image_size}")
print(f"   Has mask: {wall_layer.mask is not None}")
print(f"   Collidable: {wall_layer.collidable}")

# Test collision at spawn point
print(f"\n4. SPAWN POINT COLLISION TEST")
print(f"   Testing collision at spawn ({spawn_x}, {spawn_y})...")
collision = body_collision(character, wall_layer)
print(f"   Collision: {collision}")

# Check the pixel at spawn point
world_x = int(character.world_x)
world_y = int(character.world_y)
if 0 <= world_x < wall_layer.image_size[0] and 0 <= world_y < wall_layer.image_size[1]:
    pixel_value = wall_layer.mask.get_at((world_x, world_y))
    print(f"   Pixel value at ({world_x}, {world_y}): {pixel_value}")

# Test movement and collision
print(f"\n5. MOVEMENT TEST")
test_moves = [
    (4, 0, "Right"),
    (-4, 0, "Left"),
    (0, 4, "Down"),
    (0, -4, "Up"),
]

for dx, dy, direction in test_moves:
    old_x, old_y = character.world_x, character.world_y
    character.world_x += dx
    character.world_y += dy
    character.update_hitbox()
    
    collision = body_collision(character, wall_layer)
    world_x = int(character.world_x)
    world_y = int(character.world_y)
    if 0 <= world_x < wall_layer.image_size[0] and 0 <= world_y < wall_layer.image_size[1]:
        pixel_value = wall_layer.mask.get_at((world_x, world_y))
    else:
        pixel_value = "OOB"
    
    print(f"   Move {direction:6} to ({character.world_x:7.1f}, {character.world_y:7.1f}): collision={collision}, pixel={pixel_value}")
    
    # Reset
    character.world_x = old_x
    character.world_y = old_y
    character.update_hitbox()

# Check wall content - find collision areas
print(f"\n6. WALL CONTENT ANALYSIS")
print(f"   Scanning for collision areas...")

# Check different regions
regions = [
    ("Top-left corner", 0, 100, 0, 100),
    ("Top-center", wall_layer.image_size[0]//2 - 100, wall_layer.image_size[0]//2 + 100, 0, 100),
    ("Center region", wall_layer.image_size[0]//2 - 100, wall_layer.image_size[0]//2 + 100, 
     wall_layer.image_size[1]//2 - 100, wall_layer.image_size[1]//2 + 100),
    ("Bottom-right corner", wall_layer.image_size[0] - 100, wall_layer.image_size[0], 
     wall_layer.image_size[1] - 100, wall_layer.image_size[1]),
]

for region_name, x_start, x_end, y_start, y_end in regions:
    collision_count = 0
    for x in range(x_start, min(x_end, wall_layer.image_size[0]), 10):
        for y in range(y_start, min(y_end, wall_layer.image_size[1]), 10):
            value = wall_layer.mask.get_at((x, y))
            if value > 0:
                collision_count += 1
    
    total_pixels = ((x_end - x_start) // 10) * ((y_end - y_start) // 10)
    if total_pixels > 0:
        percentage = (collision_count / total_pixels) * 100
        print(f"   {region_name:25} - {collision_count:3}/{total_pixels:3} collision pixels ({percentage:5.1f}%)")

print("\n" + "=" * 60)

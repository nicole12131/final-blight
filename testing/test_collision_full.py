#!/usr/bin/env python3
"""
Comprehensive collision integration test.
Validates that collision mask matches wall.png visibility.
"""
import pygame
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.character import GameCharacter
from src.ground import WallLayer
from src.collision import check_collision, colliding_layers
from src.world import World

pygame.init()
pygame.display.set_mode((1,1))

# Load all layers like the game does
ground_png = 'assets/layers/ground.png'
wall_png = 'assets/layers/wall.png'
misc_png = 'assets/layers/misc.png'

from src.ground import GroundLayer, MiscLayer

ground = GroundLayer(ground_png, z=0, parallax_factor=1.0)
wall = WallLayer(wall_png, z=1, parallax_factor=1.0)
misc = MiscLayer(misc_png, z=2, parallax_factor=1.0)

world = World([ground, wall, misc], world_width=15360, world_height=8640, viewport_width=360, viewport_height=240)

# Test cases: position, expected_collision
tests = [
    ((50, 120), True, "Left edge wall"),
    ((180, 120), False, "Spawn area"),
    ((10, 50), True, "Top-left wall"),
    ((7680, 4320), False, "Center area (likely transparent)"),
    ((0, 0), True, "Far top-left"),
]

print("=" * 60)
print("COLLISION INTEGRATION TEST")
print("=" * 60)

all_pass = True
for (x, y), expected, label in tests:
    player = GameCharacter(x, y, width=18, height=28)
    got = check_collision(player, world.layers)
    status = "PASS" if got == expected else "FAIL"
    all_pass = all_pass and (got == expected)
    hits = colliding_layers(player, world.layers)
    hit_info = f" (hit: {hits[0][0].__class__.__name__})" if hits else ""
    print(f"[{status}] ({x:5d}, {y:5d}) {label:30s} | expected={expected} got={got}{hit_info}")

print("=" * 60)
if all_pass:
    print("All tests PASSED")
else:
    print("Some tests FAILED - check above")
print("=" * 60)

pygame.quit()

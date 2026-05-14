#!/usr/bin/env python3
import pygame
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

pygame.init()
pygame.display.set_mode((1,1))

print("Importing modules...")
from src.character import GameCharacter
from src.ground import WallLayer
from src.collision import check_collision

print("Loading wall layer...")
wall = WallLayer('assets/layers/wall.png', z=1, parallax_factor=1.0)
print(f"Wall collidable: {wall.collidable}, has mask: {wall.mask is not None}")

tests = [
    ((50, 120), True, "Left edge wall"),
    ((180, 120), False, "Spawn area"),
]

print("\nRunning collision tests:")
for (x, y), expected, label in tests:
    player = GameCharacter(x, y, width=18, height=28)
    got = check_collision(player, [wall])
    status = "✓" if got == expected else "✗"
    print(f"{status} ({x},{y}) {label:20s} exp={expected} got={got}")

pygame.quit()
print("Done.")

import pygame
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.character import GameCharacter
from src.ground import WallLayer
from src.collision import check_collision

pygame.init()
pygame.display.set_mode((1,1))

wall = WallLayer('assets/layers/wall.png', z=1, parallax_factor=1.0)
wall.collidable = True

cases = [
    (50, 120, True),
    (180, 120, False)
]

for x,y,expected in cases:
    p = GameCharacter(x, y, width=18, height=28)
    got = check_collision(p, [wall])
    print(f"pos=({x},{y}) expected={expected} got={got}")

pygame.quit()

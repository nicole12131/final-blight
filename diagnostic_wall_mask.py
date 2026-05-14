import pygame
import os

pygame.init()
pygame.display.set_mode((1,1))

wall_path = 'assets/layers/wall.png'
wall_img = pygame.image.load(wall_path).convert_alpha()
w, h = wall_img.get_size()

# Create mask with same threshold as in ground.py
mask_254 = pygame.mask.from_surface(wall_img, 254)  # alpha >= 254
mask_1 = pygame.mask.from_surface(wall_img, 1)      # any non-zero alpha

print(f"Wall image: {w}x{h}")
print(f"Checking opaque pixels at sample positions...")
print()

# Sample positions
test_pts = [
    (50, 120, "left edge (known wall)"),
    (180, 120, "spawn"),
    (0, 0, "top-left corner"),
    (100, 100, "middle area"),
]

for x, y, label in test_pts:
    if 0 <= x < w and 0 <= y < h:
        px = wall_img.get_at((x, y))
        mask_254_val = mask_254.get_at((x, y))
        mask_1_val = mask_1.get_at((x, y))
        print(f"({x:4d}, {y:4d}) {label:30s} | pixel={px} | mask(254)={mask_254_val} | mask(1)={mask_1_val}")
    else:
        print(f"({x:4d}, {y:4d}) {label:30s} | OUT OF BOUNDS")

# Compare mask contents
mask_254_count = mask_254.count()
mask_1_count = mask_1.count()
total_pixels = w * h

print()
print(f"Mask(254) opaque pixels: {mask_254_count} / {total_pixels} ({100*mask_254_count/total_pixels:.1f}%)")
print(f"Mask(1)   opaque pixels: {mask_1_count} / {total_pixels} ({100*mask_1_count/total_pixels:.1f}%)")
print()

# Sample the image at known wall positions to see alpha values
print("Alpha values at left edge (should be 255 for opaque):")
for y in range(100, 130, 5):
    px = wall_img.get_at((0, y))
    print(f"  (0, {y}): {px}")

pygame.quit()

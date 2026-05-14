
#Quick test script to check wall.png collision pixels

import pygame
import os

# Initialize pygame
pygame.init()
pygame.display.set_mode((1, 1))  # Minimal display for image loading

# Path to wall.png
wall_path = os.path.join(os.path.dirname(__file__), 'assets', 'layers', 'wall.png')

print(f"Checking wall.png at: {wall_path}")
print(f"File exists: {os.path.exists(wall_path)}")

if os.path.exists(wall_path):
    try:
        # Load the image
        wall_image = pygame.image.load(wall_path).convert_alpha()
        wall_size = wall_image.get_size()
        print(f"Wall image size: {wall_size}")

        # Create mask
        wall_mask = pygame.mask.from_surface(wall_image)
        print(f"Wall mask created: {wall_mask is not None}")

        # Check some sample pixels
        sample_points = [
            (100, 100),
            (500, 500),
            (1000, 1000),
            (2000, 2000),
            (wall_size[0]//2, wall_size[1]//2),  # Center
            (wall_size[0]-100, wall_size[1]-100),  # Bottom-right
        ]

        collision_pixels = 0
        for x, y in sample_points:
            if 0 <= x < wall_size[0] and 0 <= y < wall_size[1]:
                value = wall_mask.get_at((x, y))
                print(f"  Pixel ({x}, {y}): {value}")
                if value > 0:
                    collision_pixels += 1

        print(f"Found {collision_pixels} collision pixels out of {len(sample_points)} samples")

        # Do a more thorough scan of the image
        print("Scanning for any collision pixels...")
        scan_step = 100  # Check every 100th pixel
        total_collision = 0
        total_checked = 0
        
        for x in range(0, wall_size[0], scan_step):
            for y in range(0, wall_size[1], scan_step):
                value = wall_mask.get_at((x, y))
                total_checked += 1
                if value > 0:
                    total_collision += 1
                    print(f"  Found collision at ({x}, {y}): {value}")
                    if total_collision >= 5:  # Show first 5 collision pixels
                        break
            if total_collision >= 5:
                break
        
        print(f"Scan complete: {total_collision} collision pixels found out of {total_checked} checked")
        
        # Check if image has any alpha channel
        has_alpha = wall_image.get_alpha() is not None
        print(f"Image has alpha channel: {has_alpha}")

    except Exception as e:
        print(f"Error loading wall.png: {e}")
else:
    print("wall.png not found!")

pygame.quit()
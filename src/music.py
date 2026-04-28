import pygame

pygame.init()
pygame.mixer.init()

def load_music(intro, loop):
    pygame.mixer.music.load(intro)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)
    pygame.mixer.music.load(loop)
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()

def sfx(path):
    sound = pygame.mixer.Sound(path)
    sound.play()


load_music('assets\music\Hero_theme_intro.mp3', 'assets\music\Hero_theme_loop.mp3')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
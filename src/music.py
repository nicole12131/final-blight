import pygame

# Initialize the mixer lazily so this module can be imported without forcing audio start.
def init_audio():
    if not pygame.mixer.get_init():
        pygame.mixer.init()


# Start looping background music from the given file.
def load_music(loop_path, volume=0.4):
    init_audio()
    try:
        pygame.mixer.music.load(loop_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print(f"Warning: unable to load music '{loop_path}'")


# Stop the currently playing music if audio is initialized.
def stop_music():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()


# Play one-shot sound effects.
def sfx(path, volume=0.6):
    init_audio()
    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        sound.play()
    except pygame.error:
        print(f"Warning: unable to play sound '{path}'")

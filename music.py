import pygame

music = True
current_music = "placeholder"

def play_music_for_screen(active_screen):
    global current_music
    music_files = {
        "start": "Resources/music/MenuMusic.mp3",
        "levels": "Resources/music/MenuMusic.mp3", 
        "paused": "Resources/music/MenuMusic.mp3", 
        "help": "Resources/music/MenuMusic.mp3", 
        "credits": "Resources/music/MenuMusic.mp3",
        "gaming": "Resources/music/GameMusic.mp3",
    }

    if current_music != music_files[active_screen]:
        pygame.mixer.music.load(music_files[active_screen])
        pygame.mixer.music.play(-1)  # Loop indefinitely
        current_music = music_files[active_screen]

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

icons = [pygame.transform.scale_by(pygame.image.load(f"Resources/minimenu/{i}.png"), 3) for i in ["restart", "pause", "music"]]
for icon in icons:
    icon.set_colorkey((131, 206, 82, 255))
rects = []
continue_button_surf = pygame.image.load("Resources/minimenu/pressed_pause_button.png")
continue_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 209 // 2, SCREEN_HEIGHT // 2 - 7, 209, 54)
back_menu_button_surf = pygame.image.load("Resources/minimenu/pressed_back_menu_button.png")
back_menu_button_rect = pygame.Rect(296, 365, 228, 54)

buttons = {
    continue_button_surf: (continue_button_rect, True),
    back_menu_button_surf: (back_menu_button_rect, True)
}

play_button_surf = pygame.image.load("Resources/menu/pressed_play_button.png")
play_button_rect = pygame.Rect(496, 129, 281, 105)

help_button_surf = pygame.image.load("Resources/menu/pressed_help_button.png")
help_button_rect = pygame.Rect(494, 265, 281, 105)

credits_button_surf = pygame.image.load("Resources/menu/pressed_credits_button.png")
credits_button_rect = pygame.Rect(494, 396, 281, 105)

buttons.update({
    play_button_surf: (play_button_rect, True),
    help_button_surf: (help_button_rect, True),
    credits_button_surf: (credits_button_rect, True)
})

lv1_button_surf = pygame.image.load("Resources/levels_interface/pressed_lvl1_button.png")
lv1_button_rect = pygame.Rect(269, 101, 91, 89)
lv2_button_surf = pygame.image.load("Resources/levels_interface/pressed_lvl2_button.png")
lv2_button_rect = pygame.Rect(268 + 92, 101, 92, 89)
lv3_button_surf = pygame.image.load("Resources/levels_interface/pressed_lvl3_button.png")
lv3_button_rect = pygame.Rect(268 + 93 * 2 - 1, 101, 93, 89)
back_button_surf = pygame.image.load("Resources/levels_interface/pressed_back_button.png")
back_button_rect = pygame.Rect(301, 509, 211, 101)

lv_access = {
    0: (lv1_button_rect, True, lv1_button_surf),
    1: (lv2_button_rect, False, lv2_button_surf),
    2: (lv3_button_rect, False, lv3_button_surf)
}

buttons.update({
    back_button_surf: (back_button_rect, True)
})

menu_button_surf = pygame.image.load("Resources/help/pressed_back_menu_button.png")
menu_button_rect = pygame.Rect(288, 483, 228, 54)

buttons.update({
    menu_button_surf: (menu_button_rect, True)
})


paused_interface = pygame.image.load("Resources/minimenu/Paused.webp").convert_alpha()
paused_rect = paused_interface.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2))

start_interface = pygame.image.load("Resources/menu/start.png").convert_alpha()
start_rect = start_interface.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2))

levels_interface = pygame.image.load("Resources/levels_interface/levels.png").convert_alpha()
levels_rect = levels_interface.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2))

help_interface = pygame.image.load("Resources/help/background.png").convert_alpha()
help_rect = help_interface.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2))

credits_interface = pygame.image.load("Resources/credits/background.png").convert_alpha()
credits_rect = credits_interface.get_rect(center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2))

# Scores images
digit_names = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
scores = {"p": pygame.transform.scale_by(pygame.image.load("Resources/score/player1.png"), 2)}
scores["p"].set_colorkey((131, 206, 82, 255))
for i, name in enumerate(digit_names):
    img = pygame.transform.scale_by(pygame.image.load(f"Resources/score/{name}.png"), 2.5)
    img.set_colorkey((131, 206, 82, 255))
    scores[i] = img

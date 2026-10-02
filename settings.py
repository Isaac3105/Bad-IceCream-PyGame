import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 820, 622
WALL_SIZE = 50
ICE_WIDTH, ICE_HEIGHT = 40, 58

pygame.init()
try:
    pygame.mixer.init()
except:
    pass
# Create a hidden or main surface so .convert_alpha() works during imports
pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

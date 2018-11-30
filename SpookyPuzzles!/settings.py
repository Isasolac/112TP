#settings framework borrowed from Chris Bradfield
import pygame
pygame.font.init()

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (148,0,241)
ICE = (173,216,230)
BROWN = (205,175,149)
ORANGE = (255,165,0)
SEAGREEN = (46,139,87)
FONT = pygame.font.SysFont("Times New Roman, Arial",10)
BIGFONT = pygame.font.SysFont("Times New Roman, Arial",30)

# game settings
WIDTH = 576   # 7 * 64 
HEIGHT = 576  # 8 * 64
FPS = 60
BGCOLOR = WHITE

#tile settings
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
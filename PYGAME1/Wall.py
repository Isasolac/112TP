import pygame
from settings import *

#This is the Wall class! I will probably include some "subclasses" here perhaps
#most of this structure is taken from Chris Bradfield
class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        #calls super
        super(Wall,self).__init__()
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
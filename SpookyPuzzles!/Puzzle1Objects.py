import pygame
from Wall import Wall
from settings import *


class Spot(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        #calls super
        super(Spot,self).__init__()
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.mapX = x
        self.mapY = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
    def update(self):
        self.scrollX,self.scrollY = self.game.getPlayerPosition()
        
    def reDraw(self,screen):
        midX,midY=3,3
        self.drawX=self.mapX+midX-self.scrollX
        self.drawY=self.mapY+midY-self.scrollY
        screen.blit(self.image,pygame.Rect(self.drawX*TILESIZE, self.drawY*TILESIZE, TILESIZE,
        TILESIZE))
        
class EndSpot(Spot):
    def __init__(self,game,x,y):
        #calls super
        super(EndSpot,self).__init__(game, x, y)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.mapX = x
        self.mapY = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class StartSpot(Spot):
    def __init__(self,game,x,y):
        #calls super
        super(StartSpot,self).__init__(game, x, y)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.mapX = x
        self.mapY = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
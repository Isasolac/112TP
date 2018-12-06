import pygame
from Wall import Wall
from settings import *
from Spot import Spot


        
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
        
    
        
class Gate(Spot):
    def __init__(self,game,x,y):
        #calls super
        super(Gate,self).__init__(game, x, y)
        self.imageOpen = pygame.transform.scale(pygame.image.load("environment/grass.png").convert_alpha(),(TILESIZE,TILESIZE))
        self.image = self.imageOpen
        self.imageClosed = pygame.transform.scale(pygame.image.load("environment/closedGate.png").convert_alpha(),(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        self.mapX = x
        self.mapY = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.isClosed=False
        
    def update(self):
        self.scrollX,self.scrollY = self.game.getPlayerPosition()
        if self.isClosed:
            self.image=self.imageClosed
        else:
            self.image = self.imageOpen

#technically i'll be using this for all 3 puzzles
class Key(Spot):
    def __init__(self,game,x,y):
        #calls up
        super(Key,self).__init__(game,x,y)
        self.image=pygame.transform.scale(pygame.image.load("environment/key.png").convert_alpha(),(TILESIZE,TILESIZE))
        self.x,self.y=x,y
        self.mapX = x
        self.mapY = y
    
    def update(self):
        self.scrollX,self.scrollY=self.game.getPlayerPosition()
        if self.scrollX==self.x and self.scrollY==self.y:
            self.kill()
            self.game.drawSnowflake=True
            self.game.player.keys+=1
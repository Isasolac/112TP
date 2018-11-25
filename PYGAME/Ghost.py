import pygame
from settings import *

class Ghost(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(Ghost, self)
        self.game = game
        self.imageForward = pygame.transform.scale(pygame.image.load("ghostSprite/ghostForwardMid.png").convert_alpha(),(TILESIZE,TILESIZE))
        self.image=self.imageForward
        self.imageLeft=pygame.transform.scale(pygame.image.load("ghostSprite/ghostLeftMid.png").convert_alpha(),(TILESIZE,TILESIZE))
        self.imageRight=pygame.transform.scale(pygame.image.load("ghostSprite/ghostRightMid.png").convert_alpha(),(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        
    def update(self, dt, keysDown, screenWidth, screenHeight):
        #initialize dx and dy values
        dx=0
        dy=0
        if keysDown(pygame.K_RIGHT):
            dx=1
            self.image=self.imageRight
        elif keysDown(pygame.K_LEFT):
            dx=-1
            self.image=self.imageLeft
        elif keysDown(pygame.K_UP):
            dy=-1
            self.image=self.imageForward
        elif keysDown(pygame.K_DOWN):
            dy=1
            self.image=self.imageForward
        if not self.collideWithWalls(dx,dy):
            self.x += dx
            self.y += dy
            
    #this function (having to do with the walls) is from Chris Bradfield as well!
    def collideWithWalls(self,dx=0,dy=0):
        for wall in self.game.walls:
            if wall.x==self.x+dx and wall.y==self.y+dy:
                return True
        return False
        
    def draw(self,screen):
        #draws ghost at certain tile
        screen.blit(self.image,pygame.Rect(self.x*TILESIZE, self.y*TILESIZE, TILESIZE,
        TILESIZE))
        
class Reflection(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(Reflection, self)
        self.game = game
        self.imageForward = pygame.transform.scale(pygame.image.load("ghostSprite/ghostForwardMid.png").convert_alpha(),(TILESIZE,TILESIZE))
        self.image=self.imageForward
        self.imageLeft=pygame.transform.scale(pygame.image.load("ghostSprite/ghostLeftMid.png").convert_alpha(),(TILESIZE,TILESIZE))
        self.imageRight=pygame.transform.scale(pygame.image.load("ghostSprite/ghostRightMid.png").convert_alpha(),(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        
    def update(self, dt, keysDown, screenWidth, screenHeight):
        #initialize dx and dy values
        dx=0
        dy=0
        if keysDown(pygame.K_RIGHT):
            dx=-1
            self.image=self.imageLeft
        elif keysDown(pygame.K_LEFT):
            dx=1
            self.image=self.imageRight
        elif keysDown(pygame.K_UP):
            dy=1
            self.image=self.imageForward
        elif keysDown(pygame.K_DOWN):
            dy=-1
            self.image=self.imageForward
        if not self.collideWithWalls(dx,dy):
            self.x += dx
            self.y += dy
         
    
    def collideWithWalls(self,dx=0,dy=0):
        for wall in self.game.walls:
            if wall.x==self.x+dx and wall.y==self.y+dy:
                return True
        return False
        
    def draw(self,screen):
        #draws ghost at certain tile
        screen.blit(self.image,pygame.Rect(self.x*TILESIZE, self.y*TILESIZE, TILESIZE,
        TILESIZE))
    
        

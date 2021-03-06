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
        #for puzzle3, sets if player is charged
        self.isCharged = False
        
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
            if dx!=0 or dy!=0:
                print("updating!")
            self.x += dx
            self.y += dy
            
    #this function (having to do with the walls) is from Chris Bradfield as well!
    def collideWithWalls(self,dx=0,dy=0):
        for wall in self.game.walls:
            if wall.x==self.x+dx and wall.y==self.y+dy:
                print("collided!")
                return True
        return False
        
    def draw(self,screen):
        #draws ghost at certain tile (topleft midpoint, 4x4)
        screen.blit(self.image,pygame.Rect(3*TILESIZE, 3*TILESIZE, TILESIZE,
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
        self.drawX = 0
        
    def update(self, dt, keysDown, screenWidth, screenHeight):
        self.scrollX,self.scrollY = self.game.getPlayerPosition()
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
        midX,midY=3,3
        self.drawX=self.x+midX-self.scrollX
        self.drawY=self.y+midY-self.scrollY
        #draws ghost at certain tile
        screen.blit(self.image,pygame.Rect(self.drawX*TILESIZE, self.drawY*TILESIZE, TILESIZE,
        TILESIZE))
    
        

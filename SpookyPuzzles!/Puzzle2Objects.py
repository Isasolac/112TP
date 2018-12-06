import pygame
from Wall import Wall
from settings import *
import time


#this class extends wall! it's for the second puzzle : )
class SlidingBlock(Wall):
    def __init__(self,game,x,y):
        #calls super (extends the Wall class so it's "solid" to the player)
        super(SlidingBlock,self).__init__(game,x,y)
        self.image = pygame.transform.scale(pygame.image.load("environment/block.png").convert_alpha(),(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.mapX = x
        self.mapY = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.isPushed=False
        self.direction = (0,0)
    
    def collideWithPoints(self,dx=0,dy=0):
        for point in self.game.points:
            if point.x==self.x+dx and point.y==self.y+dy:
                print("collided!")
                return True
        return False
    
    def collideWithBlocks(self,dx=0,dy=0):
        for block in self.game.blocks:
            if block.x==self.x+dx and block.y==self.y+dy:
                print("collided!")
                return True
        return False
        
    def push(self,direction):
        dx,dy=direction
        print("pushes!")
        #checks if it's next to a point or block
        #if it collides, it stops being pushed! BASE CASE
        if self.collideWithPoints(dx,dy) or \
           self.collideWithBlocks(dx,dy):
            self.isPushed=False
            self.mapX,self.mapY=self.x,self.y
        #the block will keep being pushed (sliding) until it collides
        else:
            self.x+= dx
            self.y+= dy
            self.mapX,self.mapY=self.x,self.y
    
    def onSwitch(self):
        for block in self.game.blocks:
            #if block is on the switch and is not sliding
            if block.x==self.game.switch.x and block.y==self.game.switch.y and \
            block.isPushed==False:
                return True
        return False
            
    
#switch for puzzle 2!
class Switch(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        super(Switch,self).__init__()
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
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
 

class PushPoint(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        super(PushPoint,self).__init__()
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
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
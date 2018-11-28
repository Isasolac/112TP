import pygame
from settings import *


#colored tiles for puzzle three!
class Tile(pygame.sprite.Sprite):
    def __init__(self,game,x,y,num):
        #calls up
        super(Tile,self).__init__()
        self.num=num
        self.game=game
        self.scrollX,self.scrollY = self.game.getPlayerPosition()
        self.image = pygame.Surface((TILESIZE,TILESIZE))
        #choose color based on number
        if num=="1": self.image.fill(PURPLE)
        elif num=="2":self.image.fill(BROWN)
        elif num=="3":self.image.fill(YELLOW)
        elif num=="4":self.image.fill(RED)
        elif num=="5":self.image.fill(ORANGE)
        elif num=="6":self.image.fill(ICE)
        elif num=="7":self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.mapX = x
        self.mapY = y
        self.rect.x = x*TILESIZE
        self.rect.y = y*TILESIZE
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
 
#this class extends wall! it's for the second puzzle : )
class SlidingBlock(Wall):
    def __init__(self,game,x,y):
        #calls super (extends the Wall class so it's "solid" to the player)
        super(SlidingBlock,self).__init__(game,x,y)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(SEAGREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.mapX = x
        self.mapY = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.isPushed=False
    
    def collideWithPoints(self,dx=0,dy=0):
        for point in self.game.points:
            if point.x==self.x+dx and point.y==self.y+dy:
                print("collided!")
                return True
        return False
        
    def push(self,direction):
        dx,dy=direction
        #checks if it's next to a point
        #if it collides, it stops being pushed! BASE CASE
        if self.collideWithPoints(self,dx,dy):
            self.isPushed=False
        #the block will keep being pushed (sliding) until it collides
        else:
            self.x+=dx
            self.y+=dy
            #RECURSION until it collides hehehe
            self.push(direction)
            
    
    
        
        
        

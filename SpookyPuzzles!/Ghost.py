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
        self.imageBack=pygame.transform.scale(pygame.image.load("ghostSprite/ghostBackMid.png").convert_alpha(),(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #for puzzle 1 and puzzle 3, for reverse tiles and ect
        self.reversed=False
        #for puzzle3, sets if player is charged
        self.isCharged = False
        #for puzzle 3, sets is player is being "moved" by a tile
        self.isSliding=False
        self.keys = 0
        self.freeze=False
        self.canMove=True
        
    def update(self, dt, keysDown, screenWidth, screenHeight):
        #if the player stops sliding, they can't be reversed anymore
        if self.reversed:
            self.reversed=False
        if not self.reversed:
            if self.isSliding:
                pygame.time.wait(250)
                self.canMove=False
            #initialize dx and dy values
            dx,dy=0,0
            if keysDown(pygame.K_RIGHT):
                dx=1
                self.image=self.imageRight
            elif keysDown(pygame.K_LEFT):
                dx=-1
                self.image=self.imageLeft
            elif keysDown(pygame.K_UP):
                dy=-1
                self.image=self.imageBack
            elif keysDown(pygame.K_DOWN):
                dy=1
                self.image=self.imageForward
        else:
            #initialize dx and dy values
            dx,dy=0,0
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
            
    #update for sliding player
    def slideUpdate(self,dt,keysDown,screenWidth,screenHeight):
        if not self.reversed:
            #initialize dx and dy values
            dx,dy=0,0
            if keysDown(pygame.K_RIGHT):
                dx=1
                self.image=self.imageRight
            elif keysDown(pygame.K_LEFT):
                dx=-1
                self.image=self.imageLeft
            elif keysDown(pygame.K_UP):
                dy=-1
                self.image=self.imageBack
            elif keysDown(pygame.K_DOWN):
                dy=1
                self.image=self.imageForward
        else:
            #initialize dx and dy values
            dx,dy=0,0
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
                
    #this function (having to do with the walls) is from Chris Bradfield as well!
    def collideWithWalls(self,dx=0,dy=0):
        for wall in self.game.walls:
            if wall.x==self.x+dx and wall.y==self.y+dy:
                print("collided with wall!")
                return True
        #add something for closed gate
        for gate in self.game.gates:
            if gate.isClosed:
                if gate.x==self.x+dx and gate.y==self.y+dy:
                    return True
        return False
    
    #if the player is on the puzzle1 startspot
    def onSpotOne(self):
        spot = self.game.startSpot
        if spot.x==self.x and spot.y==self.y:
            return True
        return False
    
    def onEndSpot(self):
        for spot in self.game.endSpots:
            if spot.x==self.x and spot.y==self.y:
                return True
        
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
        self.canMove=False
        
    def update(self, dt, keysDown, screenWidth, screenHeight):
        self.scrollX,self.scrollY = self.game.getPlayerPosition()
        if self.game.puzzleOneEnded:
            print('KILLLLLL')
            self.kill()
        if self.canMove:
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
    
    def onEndSpot(self):
        for spot in self.game.endSpots:
            if spot.x==self.x and spot.y==self.y:
                return True
    
    def reDraw(self,screen):
        midX,midY=3,3
        self.drawX=self.x+midX-self.scrollX
        self.drawY=self.y+midY-self.scrollY
        #draws ghost at certain tile
        screen.blit(self.image,pygame.Rect(self.drawX*TILESIZE, self.drawY*TILESIZE, TILESIZE,
        TILESIZE))
    
        

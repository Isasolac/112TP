import pygame
from pygamegame import PygameGame
from Ghost import *
from Wall import *
from settings import *
from Map import *
from os import path
import time
import string




###################################################
#PLAYING THE GAME/SETTING THE RULES
###################################################

class Puzzle2(PygameGame):
    def init(self):
        self.timer=0
        #initializes the pause function
        self.isPaused=False
        #initializes the game 
        self.gameOver = False
        #initializes screen
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        #initializes player
        self.player=Ghost(self,0,0)
        #BACKGROUND COLOR
        self.bgColor=WHITE
        #INITIALIZES WALL GROUP
        self.walls = pygame.sprite.Group()
        #INITIALIZES GROUP OF POINTS ON THE SIDE
        self.points = pygame.sprite.Group()
        #INITIALIZES BLOCK GROUP
        self.blocks = pygame.sprite.Group()
        #BUILDS MAP AND PUTS PLAYER ON MAP
        self.map = Map("puzzle2.txt")
        for row,tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                #initializes the walls
                if tile == 'x':
                    newWall = Wall(self, col, row)
                    self.walls.add(newWall)
                #initializes the player
                if tile == 'p':
                    self.player.x,self.player.y = col, row
                    self.playerStart = (col, row)
                #initializes the points! hehehe
                if tile == 'D':
                    newPoint = PushPoint(self,col,row)
                    self.points.add(newPoint)
                if tile == 'b':
                    newBlock = SlidingBlock(self,col,row)
                    self.blocks.add(newBlock)
                    self.walls.add(newBlock)
                    
    def getPlayerPosition(self):
        return (self.player.x,self.player.y)
                    
    
    def drawGrid(self):
        for x in range(0,WIDTH,TILESIZE):
            pygame.draw.line(self.screen,LIGHTGREY,(x,0),(x,HEIGHT))
        for y in range(0,HEIGHT,TILESIZE):
            pygame.draw.line(self.screen,LIGHTGREY,(0,y),(WIDTH,y))

    
        
    def timerFired(self,dt):
        #starts the clock
        self.timer+=1
        if not self.isPaused:
            #the player's actual position
            preCol,preRow=self.getPlayerPosition()
            #makes the move with the key
            self.player.update(dt,self.isKeyPressed,self.width, self.height)
            self.walls.update()
            self.blocks.update()
            self.points.update()
        return self.timer
        
    def redrawAll(self,screen):
        self.screen.fill(BGCOLOR)
        self.drawGrid()
        for block in self.blocks:
            block.reDraw(screen)
        for point in self.points:
            point.reDraw(screen)
        self.player.draw(screen)
        for wall in self.walls:
            wall.reDraw(screen)
        if self.gameOver==True:
            pygame.draw.rect(self.screen,RED,pygame.Rect(0,3*TILESIZE,WIDTH, 2*TILESIZE))
            screen.blit(self.gameOverImage,pygame.Rect(2*TILESIZE, 2.5*TILESIZE, 3*TILESIZE,
            3*TILESIZE))
    
Puzzle2(600,600).run()
import pygame
from pygamegame import PygameGame
from Map import *
from Wall import *
from Ghost import Ghost
from os import path




class Main(PygameGame):
    def init(self):
        self.player=Ghost(self,0,0)
        self.gameOver=False
        self.bgColor = (0,0,0)
        #loads into map data
        self.map=Map("practiceMap1.txt")
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        #initializes groups of walls and paths
        self.walls = pygame.sprite.Group()
        self.paths = pygame.sprite.Group()
        #initializes list of ending positions (there are two)
        self.endSpots = []
        #initializes map
        for row,tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'x':
                    newWall = Wall(self, col, row)
                    self.walls.add(newWall)
                if tile == 'p':
                    self.player.x,self.player.y = col, row
                    self.playerStart = (col, row)
        
    
    #draws the main "tiles" in the background
    def drawGrid(self):
        for x in range(0,WIDTH,TILESIZE):
            pygame.draw.line(self.screen,LIGHTGREY,(x,0),(x,HEIGHT))
        for y in range(0,HEIGHT,TILESIZE):
            pygame.draw.line(self.screen,LIGHTGREY,(0,y),(WIDTH,y))
    
    def getPlayerPosition(self):
        return (self.player.x,self.player.y)
            
    def timerFired(self,dt):
        if self.gameOver==False:
            self.player.update(dt,self.isKeyPressed,self.width, self.height)
            self.walls.update()
    
    def keyPressed(self,keyCode,modifier):
        #reset button for this puzzle
        if self.isKeyPressed(pygame.K_r):
            self.gameOver=False
            self.player.x,self.player.y=self.playerStart
            self.reflection.x,self.reflection.y=self.reflStart
            
            
    def redrawAll(self,screen):
        self.screen.fill(BGCOLOR)
        self.drawGrid()
        self.player.draw(screen)
        for wall in self.walls:
            wall.reDraw(screen)
        if self.gameOver==True:
            pygame.draw.rect(self.screen,RED,pygame.Rect(0,3*TILESIZE,WIDTH, 2*TILESIZE))
            screen.blit(self.gameOverImage,pygame.Rect(2*TILESIZE, 2.5*TILESIZE, 3*TILESIZE,
            3*TILESIZE))
            
        
        
        
Main(600,600).run()
import pygame
from pygamegame import PygameGame
from Map import *
from Wall import *
from Ghost import Ghost
from os import path


class Main(PygameGame):
    def init(self):
        self.gameOver=False
        self.bgColor = (0,0,0)
        #loads into map data
        self.map=Map("rPuzzleMap1.txt")
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
                elif tile == 'p':
                    self.player = Ghost(self, col, row)
                    self.playerGroup=pygame.sprite.GroupSingle(self.player)
                    self.playerStart = (col, row)
                    
        self.camera = Camera(self.map.width,self.map.height)
        
    def timerFired(self,dt):
        self.camera.update(self.player)
                    
    #draws the main "tiles" in the background
    def drawGrid(self):
        for x in range(0,WIDTH,TILESIZE):
            pygame.draw.line(self.screen,LIGHTGREY,(x,0),(x,HEIGHT))
        for y in range(0,HEIGHT,TILESIZE):
            pygame.draw.line(self.screen,LIGHTGREY,(0,y),(WIDTH,y))
            
    def redrawAll(self,screen):
        self.screen.fill(BGCOLOR)
        self.drawGrid()
        for wall in self.walls:
            self.screen.blit(wall.image,self.camera.apply(wall))
        self.screen.blit(self.player.image,self.camera.apply(self.player))
        
        
Main(600,600).run()
import pygame
from pygamegame import PygameGame
from Ghost import *
from Wall import *
from settings import *
from Map import *
from os import path

'''Although this file is currently the "main" game, later I will most likely import
this code as being merely the "reflection puzzle minigame" portion of the larger
game.'''
'''NOTE HOW TO PLAY: use the arrow keys to move your character around! your character
is the character that starts at the bottom. the other character will reflect all
your moves and so basically move the opposite direction. move your character so
both characters end up on the green squares!'''


class Game(PygameGame):
    def init(self):
        self.player=Ghost(self,0,0)
        self.gameOver=False
        self.gameOverImage=pygame.transform.scale(pygame.image.load("gameOver.png").convert_alpha(),(TILESIZE*3,TILESIZE*3))
        self.bgColor = (0,0,0)
        self.map = Map("rPuzzleMap1.txt")
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        #initializes player/player starting position
        self.walls = pygame.sprite.Group()
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
                if tile == 'r':
                    self.reflection = Reflection(self,col,row)
                    self.reflStart = (col,row)
                if tile == 'e':
                    self.endSpots.append((row,col))
        
    
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
            self.reflection.update(dt,self.isKeyPressed,self.width, self.height)
        #minigame puzzle reflection gameover state
        if (self.player.y,self.player.x)==self.endSpots[0] and \
            (self.reflection.y,self.reflection.x)==self.endSpots[1] or \
            (self.player.y,self.player.x)==self.endSpots[1] and \
            (self.reflection.y,self.reflection.x)==self.endSpots[0]:
            self.gameOver=True
    
    def keyPressed(self,keyCode,modifier):
        #reset button for this puzzle
        if self.isKeyPressed(pygame.K_r):
            self.gameOver=False
            self.player.x,self.player.y=self.playerStart
            self.reflection.x,self.reflection.y=self.reflStart
            
            
    def redrawAll(self,screen):
        self.screen.fill(BGCOLOR)
        self.drawGrid()
        for spot in self.endSpots:
            y,x=spot
            pygame.draw.rect(self.screen,GREEN,pygame.Rect(x*TILESIZE,y*TILESIZE,TILESIZE,TILESIZE))
        self.player.draw(screen)
        self.reflection.draw(screen)
        for wall in self.walls:
            wall.reDraw(screen)
        if self.gameOver==True:
            pygame.draw.rect(self.screen,RED,pygame.Rect(0,3*TILESIZE,WIDTH, 2*TILESIZE))
            screen.blit(self.gameOverImage,pygame.Rect(2*TILESIZE, 2.5*TILESIZE, 3*TILESIZE,
            3*TILESIZE))
            
        
        
        
Game(600,600).run()
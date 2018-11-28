import pygame
from pygamegame import PygameGame
from Ghost import *
from Wall import *
from settings import *
from Map import *
from os import path
import time
import string



"""The code for the puzzle board is as follows:
1-purple tiles (normal unless player is "charged"
2-brown tiles (normal!)
3-yellow tiles (normal, but charges the player)
4-red (walls! but red so thus puzzleWalls ;))
5-orange (bounces the player back to the square they were just in after a time
delay)
6-ice (slides the player to the next tile in the direction they were walking!)
7-green (puts the player to sleep for 3 seconds) """

#############################################
#INITIALIZING THE BOARD
#############################################
def board3():
    board = [[1,6,5,4],
            [7,2,3,6],
            [4,5,2,4],
            [3,6,2,7],
            [2,6,1,5],
            [4,1,2,2],
            [5,7,6,3],
            [7,4,5,2],
            [4,2,6,1],
            [4,2,3,1],
            [5,4,6,4],
            [3,4,7,3],
            [2,4,5,2],
            [1,5,2,7],
            [4,2,2,3]]
    return board


#writeFile is from the class website!
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
        
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
#wrapper function for writeFile
#returns a string of the new map text
def boardText(board):
    #initializes string
    result = "xxxooooxx\n"
    for row in board:
        #this is going to be the string version of the row
        strRow="xxx"
        for col in row:
            strRow+=str(col)
        #makes a newline after the end of the row
        strRow+="xx\n"
        result+=strRow
    result+="xxxoopoxx"
    return result

#writes the file with the board!!! AHHHH IT WORKED WOWEE
writeFile("puzzle3.txt",boardText(board3()))
print(readFile("puzzle3.txt"))

def isLegal(player,board,row,col):
    print("row: "+str(row)+" col: "+str(col))
    #check if it's a red square (basically a wall)
    if board[row][col]==4:
        return False
    #check if players are charged+purple tile
    #is the player on a purple tile?
    elif board[row][col]==1:
        #is the player charged?
        if player.isCharged:
            #then the player can't be on that tile...
            print("charged!")
            return False
    return True

###################################################
#PLAYING THE GAME/SETTING THE RULES
###################################################

class Puzzle3(PygameGame):
    def init(self):
        self.timer=0
        #initializes the pause function
        self.isPaused=False
        #initializes the BOARD
        self.board=board3()
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
        #INITIALIZES COLORED TILE GROUP
        self.tiles = pygame.sprite.Group()
        #BUILDS MAP AND PUTS PLAYER ON MAP
        self.map = Map("puzzle3.txt")
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
                #initializes the tiles! hehehe
                if tile.isdigit():
                    newTile = Tile(self,col,row,tile)
                    self.tiles.add(newTile)
                    
    def getPlayerPosition(self):
        return (self.player.x,self.player.y)
                    
    def getPlayerBoardPos(self):
        #these numbers will depend on the where the puzzle is on the map
        #I will have to change/calculate these by hand when I change maps
        marginX,marginY=3,1
        x,y=self.getPlayerPosition()
        return (x-marginX,y-marginY)
    
    def drawGrid(self):
        for x in range(0,WIDTH,TILESIZE):
            pygame.draw.line(self.screen,LIGHTGREY,(x,0),(x,HEIGHT))
        for y in range(0,HEIGHT,TILESIZE):
            pygame.draw.line(self.screen,LIGHTGREY,(0,y),(WIDTH,y))

    
    #updates the player's position
    def applyTile(self,player,board,keysDown,dt):
        #gets where the player is on the board
        col,row=self.getPlayerBoardPos()
        #which type of tile is the player on?
        tile=board[row][col]
        #if it's a yellow tile (3), charges the player!
        if tile==3: self.player.isCharged=True
        #if it's an ice tile (6), slides the player once more in their direction
        if tile==6: 
            #discharges the player!
            self.player.isCharged=False
            #pauses the game for half a second to allow "sliding" effect
            #i haven't figured this out yet...:(
            timePaused=12
            self.timer=0
            self.isPaused=True
            while self.timer<=12:
                self.isPaused=self.pauseFunction()
                self.timer=self.timerFired(dt)
            self.isPaused=False
            print(self.isPaused)
            #we have to also check the following tile
            #the player's actual position
            preCol,preRow=self.getPlayerPosition()
            #makes the move with the key
            self.player.update(dt,keysDown,self.width, self.height)
            postCol,postRow=self.getPlayerBoardPos()
            #CHECKS IF PLAYER IS ON THE BOARD
            if self.getPlayerBoardPos()[0]>=0 and self.getPlayerBoardPos()[0]<4 and\
            self.getPlayerBoardPos()[1]>=0 and self.getPlayerBoardPos()[1]<15:
                #if the player is illegal, doesn't let player pass
                if isLegal(self.player,self.board,postRow,postCol)==False:
                    self.player.x,self.player.y=preCol,preRow
                else:
                    self.applyTile(self.player,self.board,self.isKeyPressed,dt)
        #if it is an orange tile (5) it bounces the player back after a moment..
        if tile==5:
            #pauses the game for half a second to allow "bouncing" effect
            #i haven't figured this out yet...:(
            timePaused=12
            self.timer=0
            self.isPaused=True
            while self.timer<=12:
                self.isPaused=self.pauseFunction()
                self.timer=self.timerFired(dt)
            self.isPaused=False
            print(self.isPaused)
            #we have to also check the following tile
            #the player's actual position
            preCol,preRow=self.getPlayerPosition()
            #reverses the keysDown
            '''if keysDown(pygame.K_RIGHT):
                keysDown(pygame.K_RIGHT),keysDown(pygame.K_LEFT)=False,True
            elif keysDown(pygame.K_LEFT):
                keysDown(pygame.K_RIGHT),keysDown(pygame.K_LEFT)=True,False
            elif keysDown(pygame.K_UP):
                keysDown(pygame.K_UP),keysDown(pygame.K_DOWN)=False,True
            elif keysDown(pygame.K_DOWN):
                keysDown(pygame.K_UP),keysDown(pygame.K_DOWN)=True,False'''
            #makes the move with the key
            self.player.update(dt,keysDown,self.width, self.height)
            postCol,postRow=self.getPlayerBoardPos()
            #CHECKS IF PLAYER IS ON THE BOARD
            if self.getPlayerBoardPos()[0]>=0 and self.getPlayerBoardPos()[0]<4 and\
            self.getPlayerBoardPos()[1]>=0 and self.getPlayerBoardPos()[1]<15:
                #if the player is illegal, doesn't let player pass
                if isLegal(self.player,self.board,postRow,postCol)==False:
                    self.player.x,self.player.y=preCol,preRow
                else:
                    self.applyTile(self.player,self.board,self.isKeyPressed,dt)
        #if it's a green tile(7) it should pause the player
        if tile==7:
            #however as we've established i can't get this to work! >:'(
            pass
        
    #this function keeps the program busy while it's paused
    def pauseFunction(self):
        return True
        
        
    def timerFired(self,dt):
        #starts the clock
        self.timer+=1
        print(self.timer)
        if not self.isPaused:
            #the player's actual position
            preCol,preRow=self.getPlayerPosition()
            #the player's board position
            preBCol,preBRow=self.getPlayerBoardPos()
            #makes the move with the key
            self.player.update(dt,self.isKeyPressed,self.width, self.height)
            postCol,postRow=self.getPlayerBoardPos()
            #CHECKS IF PLAYER IS ON THE BOARD
            if self.getPlayerBoardPos()[0]>=0 and self.getPlayerBoardPos()[0]<4 and\
            self.getPlayerBoardPos()[1]>=0 and self.getPlayerBoardPos()[1]<15:
                #if the player is illegal, doesn't let player pass
                if isLegal(self.player,self.board,postRow,postCol)==False:
                    self.player.x,self.player.y=preCol,preRow
                else:
                    self.applyTile(self.player,self.board,self.isKeyPressed,dt)
            self.walls.update()
            self.tiles.update()
            print(self.getPlayerBoardPos())
        return self.timer
        
    def redrawAll(self,screen):
        self.screen.fill(BGCOLOR)
        self.drawGrid()
        for tile in self.tiles:
            tile.reDraw(screen)
        self.player.draw(screen)
        for wall in self.walls:
            wall.reDraw(screen)
        if self.gameOver==True:
            pygame.draw.rect(self.screen,RED,pygame.Rect(0,3*TILESIZE,WIDTH, 2*TILESIZE))
            screen.blit(self.gameOverImage,pygame.Rect(2*TILESIZE, 2.5*TILESIZE, 3*TILESIZE,
            3*TILESIZE))
    
Puzzle3(600,600).run()
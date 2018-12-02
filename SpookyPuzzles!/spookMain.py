import pygame
from pygamegame import PygameGame
from Map import *
from Wall import *
from Ghost import Ghost
from os import path
from Puzzle3 import *
from KakuroSquare import *
from Puzzle2Objects import *




class Main(PygameGame):
    def init(self):
        self.timer=0
        #initializes the pause function
        self.isPaused=False
        #initializes the game 
        self.gameOver = False
        self.gameOverImage=pygame.transform.scale(pygame.image.load("gameOver.png").convert_alpha(),(TILESIZE*3,TILESIZE*3))
        #INITIALIZES WALL GROUP
        self.walls = pygame.sprite.Group()
        #initializes screen
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        #initializes player
        self.player=Ghost(self,0,0)
        #BACKGROUND COLOR
        self.bgColor=WHITE
        ######### PUZZLE 1 INIT
        #initializes list of ending positions (there are two)
        self.endSpots = []
        ######### PUZZLE 2 INIT
        #INITIALIZES GROUP OF POINTS ON THE SIDE
        self.points = pygame.sprite.Group()
        #INITIALIZES BLOCK GROUP
        self.blocks = pygame.sprite.Group()
        #initializes switch
        self.switch=Switch(self,0,0)
        ######### PUZZLE 3 INIT
        #initializes the BOARD
        self.board=board3()
        #INITIALIZES COLORED TILE GROUP
        self.tiles = pygame.sprite.Group()
        ############## MAP STUFF
        #loads into map data
        self.map=Map("mainMap.txt")
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        #initializes grouppaths
        self.paths = pygame.sprite.Group()
        ########### PUZZLE 4 INIT
        #initializes Kakuro squares for puzzle 4!
        #kvalues are all the list items from self.kBoard
        kValues=[]
        #dictionary: keys are x,y; values are botleft,topright numbers!
        self.kSquares=dict()
        self.kSquaresFinal=pygame.sprite.Group()
        #counter counts the number ksquare that's being added from the board
        kCount=0
        #initializes the kBoard and adds everything to kValues!
        self.kBoard=KakuroBoard(self,kakuroBoard1())
        self.kBoard.makeDicts()
        for item in self.kBoard.board:
            for value in item:
                if isinstance(value,list):
                    kValues.append(value)
        print(kValues)
        #initialize kakuro changing tiles
        self.kTiles=pygame.sprite.Group()
        #initializes map
        for row,tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'x':
                    newWall = Wall(self, col, row)
                    self.walls.add(newWall)
                if tile == 'P':
                    self.player.x,self.player.y = col, row
                    self.playerStart = (col, row)
                #initializes the tiles! hehehe
                if tile.isdigit():
                    newTile = Tile(self,col,row,tile)
                    self.tiles.add(newTile)
                #initializes the points! hehehe
                if tile == 'D':
                    newPoint = PushPoint(self,col,row)
                    self.points.add(newPoint)
                if tile == 'b':
                    newBlock = SlidingBlock(self,col,row)
                    self.blocks.add(newBlock)
                    self.walls.add(newBlock)
                if tile == 'S':
                    self.switch.x,self.switch.y=col,row
                    self.switch.mapX,self.switch.mapY=col,row
                if tile == 'K':
                    self.kSquares[(col,row)]=kValues[kCount]
                    kCount+=1
                if tile == 0:
                    newTile=KTile(self,(row,col))
                    self.kTiles.add(newTile)
        #makes kakuro squares for puzzle 4
        for location in self.kSquares:
            square=KakuroSquare(self,location,self.kSquares[location])
            self.kSquaresFinal.add(square)
        print(self.kTiles)
        
    #draws the main "tiles" in the background
    def drawGrid(self):
        for x in range(0,WIDTH,TILESIZE):
            pygame.draw.line(self.screen,LIGHTGREY,(x,0),(x,HEIGHT))
        for y in range(0,HEIGHT,TILESIZE):
            pygame.draw.line(self.screen,LIGHTGREY,(0,y),(WIDTH,y))
    
    def getPlayerPosition(self):
        return (self.player.x,self.player.y)
    
    #FOR PUZZLE 4 KAKURO BOARD
    def getPlayerKBoardPos(self):
        marginX,marginY=10,1
        x,y=self.getPlayerPosition()
        return (x-marginX,y-marginY)
    
    def getPlayerBoardPos(self):
        #these numbers will depend on the where the puzzle is on the map
        #I will have to change/calculate these by hand when I change maps
        marginX,marginY=12,18
        x,y=self.getPlayerPosition()
        return (x-marginX,y-marginY)
    
    
        
   
            
    def timerFired(self,dt):
        self.timer+=1
        if not self.isPaused:
            ################PUZZLE 3
            #the player's actual position
            preCol,preRow=self.getPlayerPosition()
            if not self.player.isSliding:
                #makes the move with the key
                self.player.update(dt,self.isKeyPressed,self.width, self.height)
                postCol,postRow=self.getPlayerBoardPos()
                #CHECKS IF PLAYER IS ON THE BOARD
                if self.getPlayerBoardPos()[0]>=0 and self.getPlayerBoardPos()[0]<4 and\
                self.getPlayerBoardPos()[1]>=0 and self.getPlayerBoardPos()[1]<15:
                    print("player on puzzle3!")
                    #if the player is illegal, doesn't let player pass
                    if isLegal(self.player,self.board,postRow,postCol)==False:
                        self.player.x,self.player.y=preCol,preRow
                    else:
                        applyTile(self, self.player,self.board,self.isKeyPressed,dt)
                        if self.player.freeze:
                            pygame.time.wait(1000)
                            self.player.freeze=False
            else:
                #pauses for a sec
                #pygame.time.wait(250)
                #makes the move with the key
                self.player.update(dt,self.player.key,self.width, self.height)
                postCol,postRow=self.getPlayerBoardPos()
                #CHECKS IF PLAYER IS ON THE BOARD
                if self.getPlayerBoardPos()[0]>=0 and self.getPlayerBoardPos()[0]<4 and\
                self.getPlayerBoardPos()[1]>=0 and self.getPlayerBoardPos()[1]<15:
                    print("player on puzzle3!")
                    #if the player is illegal, doesn't let player pass
                    if isLegal(self.player,self.board,postRow,postCol)==False:
                        self.player.x,self.player.y=preCol,preRow
                    else:
                        applyTile(self, self.player,self.board,self.player.key,dt)
            self.tiles.update()
            ##################PUZZLE 2
            self.blocks.update()
            self.switch.update()
            for block in self.blocks:
                #the block will keep being pushed (sliding) until it collides
                if block.isPushed:
                    #this creates the illusion of sliding, because it pauses 
                    pygame.time.wait(250)
                    block.push(block.direction)
                if block.onSwitch():
                    self.gameOver=True
            self.points.update()
            self.walls.update()
            self.kSquaresFinal.update()
        return self.timer
    
    #THIS FUNCTION IS ALSO FOR PUZZLE 2 (BLOCKS)
    #returns None if block not in range, returns direction of push if it is
    #x1,y1 should be player coordinates, x2,y2 should be block coordinates
    def direction(self,x1,y1,x2,y2):
        #checks if it's in range...
        if abs(x1-x2)==1 and y1==y2 or abs(y1-y2)==1 and x1==x2:
            #dy=1 if the player is above the block
            if (y2-y1)==1:
                return (0,1)
            #and vice versa
            elif (y2-y1)==-1:
                return (0,-1)
            #dx=1 if player is to the left of the block
            elif (x2-x1)==1:
                return (1,0)
            #and vice versa!
            elif (x2-x1)==-1:
                return (-1,0)
        #else return None!
        return None
    
    def keyPressed(self,keyCode,modifier):
        #checks if user presses the space key FOR PUZZLE 2
        if self.isKeyPressed(pygame.K_SPACE):
            #checks if user's player sprite is in range of a block (L,R,U,D)
            for block in self.blocks:
                direction=self.direction(self.player.x,self.player.y,block.x,block.y)
                if direction != None:
                    block.isPushed=True
                    block.direction = direction
        #reset button for this puzzle
        if self.isKeyPressed(pygame.K_r):
            self.gameOver=False
            self.player.x,self.player.y=self.playerStart
            self.reflection.x,self.reflection.y=self.reflStart
        #checks if player is on a kakuro tile
        for tile in self.kTiles:
            if self.getPlayerPosition()==(tile.x,tile.y):
                if self.isKeyPressed(pygame.K_1):self.kBoard.board[tile.y][tile.x]=1
                if self.isKeyPressed(pygame.K_2):self.kBoard.board[tile.y][tile.x]=2
                if self.isKeyPressed(pygame.K_3):self.kBoard.board[tile.y][tile.x]=3
                if self.isKeyPressed(pygame.K_4):self.kBoard.board[tile.y][tile.x]=4
                if self.isKeyPressed(pygame.K_5):self.kBoard.board[tile.y][tile.x]=5
                if self.isKeyPressed(pygame.K_6):self.kBoard.board[tile.y][tile.x]=6
                if self.isKeyPressed(pygame.K_7):self.kBoard.board[tile.y][tile.x]=7
                if self.isKeyPressed(pygame.K_8):self.kBoard.board[tile.y][tile.x]=8
                if self.isKeyPressed(pygame.K_9):self.kBoard.board[tile.y][tile.x]=9
            #LEGALITY CHECK
            if not self.kBoard.isLegal():
                self.kBoard.board[tile.y][tile.x]=0
            
            
    def redrawAll(self,screen):
        self.screen.fill(BGCOLOR)
        self.drawGrid()
        for block in self.blocks:
            block.reDraw(screen)
        for point in self.points:
            point.reDraw(screen)
        self.switch.reDraw(screen)
        for tile in self.tiles:
            tile.reDraw(screen)
        for square in self.kSquaresFinal:
            square.reDraw(screen)
        for tile in self.kTiles:
            tile.reDraw(screen)
        self.player.draw(screen)
        for wall in self.walls:
            wall.reDraw(screen)
        if self.gameOver==True:
            pygame.draw.rect(self.screen,RED,pygame.Rect(0,3*TILESIZE,WIDTH, 2*TILESIZE))
            screen.blit(self.gameOverImage,pygame.Rect(2*TILESIZE, 2.5*TILESIZE, 3*TILESIZE,
            3*TILESIZE))
            
        
        
        
Main(600,600).run()
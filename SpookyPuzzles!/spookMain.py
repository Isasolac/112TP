import pygame
from pygamegame import PygameGame
from Map import *
from Wall import *
from Ghost import Ghost
from os import path
from Puzzle3 import *
from KakuroSquare import *
from Puzzle2Objects import *
from Puzzle1Objects import *
from coolFractal import Snowflake

#ART CITATIONS
#GHOST SPRITE FROM FINAL FANTASY 6, SNOW FROM VECTOR.COM,
#WALL AND GATE FROM OPENGAMEART USER '.bee', KEY FROM LEGEND OF ZELDA




class Main(PygameGame):
    def init(self):
        self.gameBegun=False
        self.drawSnowflake=False
        self.snowflake = Snowflake(self)
        self.timer=0
        self.ghosts=pygame.sprite.Group()
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
        self.spots = pygame.sprite.Group()
        self.puzzleOneStarted=False
        self.puzzleOneEnded=False
        self.gates = pygame.sprite.Group()
        self.endSpots = pygame.sprite.Group()
        ######### PUZZLE 2 INIT
        self.puzzleTwoStarted=True
        self.puzzleTwoEnded=False
        #INITIALIZES GROUP OF POINTS ON THE SIDE
        self.points = pygame.sprite.Group()
        #INITIALIZES BLOCK GROUP
        self.blocks = pygame.sprite.Group()
        #initializes switch
        self.switch=Switch(self,0,0)
        self.gates2 = pygame.sprite.Group()
        ######### PUZZLE 3 INIT
        #initializes the BOARD
        self.puzzleThreeStarted=False
        self.puzzleThreeEnded=False
        self.puzzleThreeX=(12,16)
        self.puzzleThreeY=(18,33)
        self.board=board3()
        #INITIALIZES COLORED TILE GROUP
        self.tiles = pygame.sprite.Group()
        ############## MAP STUFF
        #loads into map data
        self.map=Map("mainMap.txt")
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        #initializes grouppaths
        self.paths = pygame.sprite.Group()
        #initializes keys
        self.keys = pygame.sprite.Group()
        ########### PUZZLE 4 INIT
        #initializes Puzzle4 game
        self.gates3=pygame.sprite.Group()
        self.puzzleFourStarted=False
        self.puzzleFourEnded=False
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
        #HINT BOARD
        self.kBoardSolved=self.kBoard.solvedBoard
        print(self.kBoardSolved)
        for item in self.kBoard.board:
            for value in item:
                if isinstance(value,list):
                    kValues.append(value)
        #initialize kakuro changing tiles
        self.kTiles=pygame.sprite.Group()
        #initializes map
        for row,tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'x':
                    newWall = Wall(self, col, row)
                    self.walls.add(newWall)
                if tile == 'k':
                    newKey = Key(self,col,row)
                    newPath = Path(self,col,row)
                    self.paths.add(newPath)
                    self.keys.add(newKey)
                if tile == 'p':
                    newPath = Path(self,col,row)
                    self.paths.add(newPath)
                if tile == 'P':
                    self.player.x,self.player.y = col, row
                    self.playerStart = (col, row)
                    newPath = Path(self,col,row)
                    self.paths.add(newPath)
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
                if tile == 'w':
                    newPath = Path(self,col,row)
                    self.paths.add(newPath)
                    newWall=clearWall(self,col,row)
                    self.walls.add(newWall)
                if tile == 'S':
                    self.switch.x,self.switch.y=col,row
                    self.switch.mapX,self.switch.mapY=col,row
                if tile == 'K':
                    self.kSquares[(col,row)]=kValues[kCount]
                    kCount+=1
                #GATES FOR WIN STATE OF PUZZLES 1,2 AND 4
                if tile == 'G':
                    newPath = Path(self,col,row)
                    self.paths.add(newPath)
                    newGate = Gate(self,col,row)
                    self.gates.add(newGate)
                if tile == 'o':
                    newPath = Path(self,col,row)
                    self.paths.add(newPath)
                    newGate = Gate(self,col,row)
                    newGate.isClosed=True
                    self.gates.add(newGate)
                if tile == 's':
                    newPath = Path(self,col,row)
                    self.paths.add(newPath)
                    newGate = Gate(self,col,row)
                    self.gates3.add(newGate)
                if tile == 'i':
                    self.startSpot = StartSpot(self,col,row)
                    self.spots.add(self.startSpot)
                if tile == 'r':
                    self.reflection = Reflection(self,col,row)
                    self.ghosts.add(self.reflection)
                    self.reflStart = (col,row)
                if tile == 'e':
                    spot=EndSpot(self,col,row)
                    self.endSpots.add(spot)
                    self.spots.add(spot)
                if tile == '0':
                    newTile=KTile(self,col,row)
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
        #THE PLAYER'S POSITION (FOR GENERAL USE)
        preCol,preRow=self.getPlayerPosition()
        if not self.puzzleThreeStarted:
            self.player.update(dt,self.isKeyPressed,self.width,self.height)
        if not self.isPaused:
            #################PUZZLE 1
            self.spots.update()
            self.gates.update()
            for ghost in self.ghosts:
                ghost.update(dt,self.isKeyPressed,self.width, self.height)
            if not self.puzzleOneEnded:
                if self.player.onSpotOne():
                    if not self.puzzleOneStarted:
                        self.puzzleOneStarted=True
                        self.reflection.canMove=True
                        for gate in self.gates:
                            gate.isClosed=True
                elif self.player.onEndSpot() and self.reflection.onEndSpot():
                    if self.player.x!=self.reflection.x or \
                        self.player.y !=self.reflection.y:
                            self.puzzleOneEnded=True
                            ############ OPENS THE GATES
                            for gate in self.gates:
                                gate.isClosed=False
            
            ################PUZZLE 3
            #CHECKS IF PLAYER IS ON THE BOARD
            if preCol>=self.puzzleThreeX[0] and preCol<self.puzzleThreeX[1] and \
               preRow>=self.puzzleThreeY[0] and preRow<self.puzzleThreeY[1]:
                   self.puzzleThreeStarted=True
            #else makes sure the player is not sliding
            else:
                self.puzzleThreeStarted=False
                self.player.isSliding=False
            #ONLY RUNS PUZZLE 3 IF PLAYER IS ON THE BOARD
            self.tiles.update()
            ##################PUZZLE 4
            #only evaluates all the puzzle 4 stuff if the player is in range
            if preRow<15:
                self.puzzleFourStarted=True
            else:
                self.puzzleFourStarted=False
            if self.kBoard.gameOver():
                print("gameover!")
                self.puzzleFourEnded=True
                self.gameOver=True
            ##################PUZZLE 2
            self.blocks.update()
            self.switch.update()
            self.kTiles.update()
            if not self.puzzleTwoEnded:
                for gate in self.gates2:
                    gate.isClosed=True
            for block in self.blocks:
                #the block will keep being pushed (sliding) until it collides
                if block.isPushed:
                    #this creates the illusion of sliding, because it pauses 
                    pygame.time.wait(250)
                    block.push(block.direction)
                if block.onSwitch():
                    self.puzzleTwoEnded=True
                    for gate in self.gates2:
                        gate.isClosed=False
            self.points.update()
            self.walls.update()
            self.paths.update()
            self.keys.update()
            self.kSquaresFinal.update()
            if self.player.keys==3:
                for gate in self.gates3:
                    gate.isClosed=False
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
            self.drawSnowflake=False
            self.gameBegun=True
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
        #######PUZZLE 3
        if self.puzzleThreeStarted:
            #use the arrow keys to navigate!
            if self.isKeyPressed(pygame.K_RIGHT):
                dx=1
                self.player.keyUpdate(dx)
                self.player.image=self.player.imageRight
                applyTile(self, self.player,self.board)
            elif self.isKeyPressed(pygame.K_LEFT):
                dx=-1
                self.player.keyUpdate(dx)
                self.player.image=self.player.imageLeft
                applyTile(self, self.player,self.board)
            elif self.isKeyPressed(pygame.K_UP):
                dy=-1
                self.player.keyUpdate(0,dy)
                self.player.image=self.player.imageBack
                applyTile(self, self.player,self.board)
            elif self.isKeyPressed(pygame.K_DOWN):
                dy=1
                self.player.keyUpdate(0,dy)
                self.player.image=self.player.imageForward
                applyTile(self, self.player,self.board)
        if self.puzzleFourStarted:
            #checks if player is on a kakuro tile
            for tile in self.kTiles:
                x,y=self.getPlayerKBoardPos()
                if self.getPlayerPosition()==(tile.x,tile.y):
                    if self.isKeyPressed(pygame.K_h):
                        self.kBoard.hint(y,x,tile)
                    elif self.isKeyPressed(pygame.K_1):
                        self.kBoard.board[y][x]=1
                        tile.value='1'
                        tile.updateText()
                    elif self.isKeyPressed(pygame.K_2):
                        self.kBoard.board[y][x]=2
                        tile.value='2'
                        tile.updateText()
                    elif self.isKeyPressed(pygame.K_3):
                        self.kBoard.board[y][x]=3
                        tile.value='3'
                        tile.updateText()
                    elif self.isKeyPressed(pygame.K_4):
                        self.kBoard.board[y][x]=4
                        tile.value='4'
                        tile.updateText()
                    elif self.isKeyPressed(pygame.K_5):
                        self.kBoard.board[y][x]=5
                        tile.value='5'
                        tile.updateText()
                    elif self.isKeyPressed(pygame.K_6):
                        self.kBoard.board[y][x]=6
                        tile.value='6'
                        tile.updateText()
                    elif self.isKeyPressed(pygame.K_7):
                        self.kBoard.board[y][x]=7
                        tile.value='7'
                        tile.updateText()
                    elif self.isKeyPressed(pygame.K_8):
                        self.kBoard.board[y][x]=8
                        tile.value='8'
                        tile.updateText()
                    elif self.isKeyPressed(pygame.K_9):
                        self.kBoard.board[y][x]=9
                        tile.value='9'
                        tile.updateText()
                    
                #LEGALITY CHECK
                if not self.kBoard.isLegal():
                    self.kBoard.board[y][x]=0
                    tile.value='0'
                    tile.updateText()
            
            
    def redrawAll(self,screen):
        self.screen.fill(BGCOLOR)
        self.drawGrid()
        for path in self.paths:
            path.reDraw(screen)
        for tile in self.kTiles:
            tile.reDraw(screen)
        for spot in self.spots:
            spot.reDraw(screen)
        for block in self.blocks:
            block.reDraw(screen)
        for key in self.keys:
            key.reDraw(screen)
        for point in self.points:
            point.reDraw(screen)
        self.switch.reDraw(screen)
        for tile in self.tiles:
            tile.reDraw(screen)
        for square in self.kSquaresFinal:
            square.reDraw(screen)
        for tile in self.kTiles:
            tile.reDraw(screen)
        for ghost in self.ghosts:
            ghost.reDraw(screen)
        for wall in self.walls:
            wall.reDraw(screen)
        for gate in self.gates:
            gate.reDraw(screen)
        self.player.draw(screen)
        if self.player.isSliding:
            print("slides!")
            pygame.time.wait(300)
        if self.drawSnowflake==True:
            self.snowflake.reDraw(screen)
        if not self.gameBegun:
            text = TITLEFONT.render(('SPOOKY PUZZLES'),True,BLACK)
            screen.blit(text,pygame.Rect(2*TILESIZE, 2*TILESIZE, 5*TILESIZE,
            5*TILESIZE))
            text2= BIGFONT.render(("PRESS SPACE TO START"),True,BLACK)
            screen.blit(text2,pygame.Rect(3*TILESIZE, 5*TILESIZE, 3*TILESIZE,
            3*TILESIZE))
        if self.puzzleFourStarted:
            text3= BIGFONT.render(("PRESS H ON SQUARE FOR HINT"),True,BLACK)
            screen.blit(text3,pygame.Rect(1*TILESIZE, 1*TILESIZE, 5*TILESIZE,
            3*TILESIZE))
        if self.gameOver==True:
            pygame.draw.rect(self.screen,RED,pygame.Rect(0,3*TILESIZE,WIDTH, 2*TILESIZE))
            screen.blit(self.gameOverImage,pygame.Rect(2*TILESIZE, 2.5*TILESIZE, 3*TILESIZE,
            3*TILESIZE))
            
        
        
        
Main(600,600).run()
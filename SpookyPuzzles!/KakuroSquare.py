import pygame
from settings import *
from Puzzle1Objects import Spot
import random
import copy
pygame.font.init()



#HINT SECTION: SOLVES BOARD
def solveBoard(kBoard,board,allVals):
    #base case
    if len(allVals)==0:
        return board
    else:
        #tests a number between 1-9
        for num in range(1,10):
            #takes off the end of the list and stores it
            loc=allVals.pop()
            row,col=loc
            #sets the location to a number 1-9 (makes move)
            board[row][col]=num
            #checks legality
            if kBoard.isLegal():
                tmpSolution=solveBoard(kBoard,board,allVals)
                if tmpSolution!=None:
                    return tmpSolution
            #undos the move
            board[row][col]=0
            allVals.append((row,col))
        return None

#class of Kakuro Square we will be using!
class KakuroSquare(pygame.sprite.Sprite):
    def __init__(self,game,location, values):
        #calls up
        super(KakuroSquare,self).__init__()
        self.game=game
        self.scrollX,self.scrollY = self.game.getPlayerPosition()
        self.image = pygame.Surface((TILESIZE,TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x,self.y = location
        self.mapX,self.mapY = location
        self.botLeft,self.topRight=values
        #sets text stuff!
        self.text=[FONT.render(str(values[0]),True,BLACK),
        FONT.render(str(values[1]),True,BLACK)]
        
        
    def update(self):
        self.scrollX,self.scrollY = self.game.getPlayerPosition()
        
    def reDraw(self,screen):
        midX,midY=3,3
        self.drawX=self.mapX+midX-self.scrollX
        self.drawY=self.mapY+midY-self.scrollY
        screen.blit(self.image,pygame.Rect(self.drawX*TILESIZE, self.drawY*TILESIZE, TILESIZE,
        TILESIZE))
        pygame.draw.aaline(screen,BLACK,[self.drawX*TILESIZE, self.drawY*TILESIZE],
        [self.drawX*TILESIZE+TILESIZE, self.drawY*TILESIZE+TILESIZE],True)
        if self.text[0]!="None":
            screen.blit(self.text[0],(self.drawX*TILESIZE,self.drawY*TILESIZE+TILESIZE-10))
        if self.text[1]!="None":
            screen.blit(self.text[1],(self.drawX*TILESIZE+TILESIZE-10,self.drawY*TILESIZE))

class KakuroBoard(object):
    def __init__(self,game,board):
        self.board=board
        self.game=game
        self.values=[]
        self.colLocs=dict()
        self.rowLocs=dict()
        #key is location, value is value
        self.rowHeadValues=dict()
        self.colHeadValues=dict()
        self.rows=[]
        self.cols=[]
        #set for solving the board
        self.allVals=[]
        #not solved yet!
        self.solvedBoard=copy.deepcopy(board)
        self.tempBoard=copy.deepcopy(board)
        for item in self.board:
            for value in item:
                if isinstance(value,list):
                    self.values.append(value)
        
    def makeDicts(self):
        #if dict[key].sum==key it's complete!
        #if in dict[key] it's illegal!
        board=self.board
        rowLst,colLst=[],[]
        for row in range(len(board)):
            for col in range(len(board)):
                item=board[row][col]
                #checks if the item is a list (then it has row/col info)
                if isinstance(item,list):
                    rowVal,colVal=board[row][col][1],board[row][col][0]
                    if rowVal!=None:
                        rowLst.append((row,col,rowVal))
                        #adds the row locations to a list of row value locations
                        self.rows.append((row,col))
                        #location maps to a row value
                        self.rowHeadValues[(row,col)]=rowVal
                    if colVal!=None:
                        colLst.append((row,col,colVal))
                        #adds the col locations to a list of row value locations
                        self.cols.append((row,col))
                        #location maps to a col value
                        self.colHeadValues[(row,col)]=colVal
                #list of everywhere there are changeable values
                elif item==0:
                    self.allVals.append((row,col))
                        
        
        #make rows
        for item in rowLst:
            row,col,value=item
            #self.rowValues[(row,col)]=value
            for i in range(1,len(board)):
                if col+i>=len(board):
                    break
                num=board[row][col+i]
                location=(row,col)
                if type(num)!=list and num!='x':
                    if location not in self.rowLocs:
                        self.rowLocs[location]=[(row,col+i)]
                    else:
                        self.rowLocs[location].append((row,col+i))
                else:
                    break
                    
        for item in colLst:
            row,col,value=item
            #self.colValues[(row,col)]=value
            for i in range(1,len(board)):
                if row+i>=len(board):
                    break
                num=board[row+i][col]
                location=(row,col)
                if type(num)!=list and num!='x':
                    if location not in self.colLocs:
                        self.colLocs[location]=[(row+i,col)]
                    else:
                        self.colLocs[location].append((row+i,col))
                else:
                    break
                    
        #solves the board now that allVals is made!
        self.solvedBoard=solveBoard(self,self.board,self.allVals)
        self.board=self.tempBoard
    
    
    def checkRows(self):
        for location in self.rows:
            #gets location and value at that location from dictionary
            row,col=location
            value=self.rowHeadValues[location]
            valueLst=[]
            #for each place on the board that the colLocation maps to...
            for loc in self.rowLocs[location]:
                #gets the value at that location
                valRow,valCol=loc
                newValue=self.board[valRow][valCol]
                #doesn't allow repeats unless zero
                if newValue!=0 and newValue in valueLst:
                    return False
                valueLst.append(newValue)
            amount=sum(valueLst)
            if amount>value:
                return False
            elif 0 not in valueLst and amount!=value:
                return False
        return True
        
    def checkCols(self):
        for location in self.cols:
            row,col=location
            value=self.colHeadValues[location]
            valueLst=[]
            #for each place on the board that the colLocation maps to...
            for loc in self.colLocs[location]:
                #gets the value at that location
                valRow,valCol=loc
                newValue=self.board[valRow][valCol]
                #doesn't allow repeats unless zero
                if newValue!=0 and newValue in valueLst:
                    return False
                valueLst.append(newValue)
            amount=sum(valueLst)
            if amount>value:
                return False
            elif 0 not in valueLst and amount!=value:
                return False
        return True
    
    
    #checks each affected location on the locLst of kakuroSquares
    def isLegal(self):
        #for each location
        if self.checkCols() and self.checkRows():
            return True
        else:
            return False
    
    #move it to other area
    def hint(self,row,col,tile):
        hintVal=self.solvedBoard[row][col]
        #changes the actual board value
        self.board[row][col]=hintVal
        #changes the display tile value and updates the display
        tile.value=str(hintVal)
        tile.updateText()
            
                
            
        

#creates the board!
def kakuroBoard1():
    board = [['x','x',[4,None],[10,None],'x','x','x'],
             ['x',[None,4],0,0,'x',[3,None],[4,None]],
             ['x',[None,3],0,0,[11,4],0,0],
             ['x',[3,None],[4,10],0,0,0,0],
             [[None,11],0,0,0,0,[4,None],'x'],
             [[None,4],0,0,[None,4],0,0,'x'],
             ['x','x','x',[None,3],0,0,'x']]
    return board
    

    
class KTile(Spot):
    def __init__(self,game,x,y):
        #calls up
        super(KTile,self).__init__(game,x,y)
        self.game=game
        self.scrollX,self.scrollY = self.game.getPlayerPosition()
        self.image = pygame.Surface((TILESIZE,TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x,self.y = x,y
        self.mapX,self.mapY = x,y
        self.value=str(self.game.kBoard.board[self.y-1][self.x-10])
        #sets text stuff!
        self.text=BIGFONT.render((self.value),True,WHITE)
     
    #CHANGETEXT
    def updateText(self):
        self.text=BIGFONT.render((self.value),True,WHITE)
        
        
    def reDraw(self,screen):
        midX,midY=3,3
        self.drawX=self.mapX+midX-self.scrollX
        self.drawY=self.mapY+midY-self.scrollY
        screen.blit(self.image,pygame.Rect(self.drawX*TILESIZE, self.drawY*TILESIZE, TILESIZE,
        TILESIZE))
        screen.blit(self.text,(self.drawX*TILESIZE,self.drawY*TILESIZE))
        

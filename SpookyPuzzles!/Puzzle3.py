import pygame
from pygamegame import PygameGame
from Ghost import *
from Wall import *
from settings import *
from Map import *
from os import path
import time
import string


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


#FOR PUZZLE 3
#updates the player's position
def applyTile(game,player,board):
    #gets where the player is on the board
    col,row=game.getPlayerBoardPos()
    #legal undoes move
    if not isLegal(player,board,row,col):
        player.x-=player.dx
        player.y-=player.dy
    #which type of tile is the player on?
    print("row: "+str(row)+" col: "+str(col))
    tile=board[row][col]
    #where was the player going?
    dx,dy=player.dx,player.dy
    #this tile is plain unless the player is charged,
    if tile==1:
        player.isSliding=False
        player.key = None
        player.reversed=False
        player.dx,player.dy=0,0
    #if it's a plain tile (2), does nothing! (but removes reversed effect)
    if tile==2:
        player.isSliding=False
        player.key = None
        player.reversed=False
        player.dx,player.dy=0,0
    #if it's a yellow tile (3), charges the player!
    if tile==3: 
        player.isSliding=False
        player.key = None
        player.reversed=False
        player.isCharged=True
        player.dx,player.dy=0,0
    #if it's an ice tile (6), slides the player once more in their direction
    elif tile==6: 
        #discharges the player!
        player.isCharged=False
        #pauses the game for a quarter second to allow "sliding" effect
        player.isSliding=True
        #we have to also check the following tile
        #the player's actual position
        preCol,preRow=game.getPlayerPosition()
        postCol,postRow=game.getPlayerBoardPos()
        #CHECKS IF PLAYER IS ON THE BOARD
        '''if game.getPlayerBoardPos()[0]>=0 and game.getPlayerBoardPos()[0]<4 and\
        game.getPlayerBoardPos()[1]>=0 and game.getPlayerBoardPos()[1]<15:
            #if the player is illegal, doesn't let player pass
            if isLegal(player,board,postRow,postCol)==False:
                player.x,player.y=preCol,preRow
            else:
                applyTile(game,player,board,game.isKeyPressed,dt)'''
        #waits for a second
        game.redrawAll(game.screen)
        pygame.time.wait(300)
        player.keyUpdate(player.dx,player.dy)
        applyTile(game,player,board)
    #if it is an orange tile (5) it bounces the player back after a moment..
    elif tile==5:
        #pauses the game for half a second to allow "bouncing" effect
        #i haven't figured this out yet...:(
        player.reversed=True
        player.dx*=-1
        player.dy*=-1
        player.isSliding=True
        pygame.time.wait(300)
        player.keyUpdate(player.dx,player.dy)
        applyTile(game,player,board)
    #if it's a green tile(7) it should pause the player
    elif tile==7:
        player.isSliding=False
        player.key = None
        player.reversed=False#wait 2 seconds
        player.dx,player.dy=0,0


def isLegal(player,board,row,col):
    #check if it's a red square (basically a wall)
    if board[row][col]==4:
        player.isSliding=False
        return False
    #check if players are charged+purple tile
    #is the player on a purple tile?
    elif board[row][col]==1:
        #is the player charged?
        if player.isCharged:
            player.isSliding=False
            #then the player can't be on that tile...
            print("charged!")
            return False
    return True
    
def isValid(board,isCharged,row,col):
    #check if it's a red square (basically a wall)
    #backtrack if out of bounds
    try:
        if board[row][col]==4:
            return False
    except:
        return False
    if board[row][col]==4:
        return False
    #check if players are charged+purple tile
    #is the player on a purple tile?
    elif board[row][col]==1:
        #is the player charged?
        if isCharged:
            #then the player can't be on that tile...
            print("charged!")
            return False
    return True



def solve(board, isCharged, row, col, visited):
    # base cases
    if row == len(board)-1 and col == len(board[0])-1:
        return visited
    # recursive case
    for direction in [(0,1),(0,-1),(1,0),(-1,0)]:
        drow, dcol = direction
        if (row+drow, col+dcol) not in visited and \
            (row+drow)>=0 and (col+dcol)>=0 and \
            (row+drow)<len(board) and (col+dcol)<len(board) and \
            isValid(board,isCharged, row, col):
            visited.add((row+drow,col+dcol))
            if board[row][col]==3:
                isCharged=True
            if board[row][col]==6:
                isCharged=False
            tmpSolution = solve(board, isCharged, row+drow, col+dcol, visited)
            if tmpSolution != None:
                return tmpSolution
            visited.remove((row+drow,col+dcol))
    return None

def solveBoard(board):
    visited = set()
    visited.add((0, 0))
    isCharged=False
    return solve(board, isCharged, 0, 0, visited)

#print(solveBoard(board3()))
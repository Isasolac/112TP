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
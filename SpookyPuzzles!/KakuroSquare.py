import pygame
from settings import *



#class of Kakuro Square we will be using!
class KakuroSquare(pygame.sprite.Sprite):
    def __init__(self,game,location, values):
        #calls up
        super(KakuroSquare,self).__init__()
        self.game=game
        self.scrollX,self.scrollY = self.game.getPlayerPosition()
        self.image = pygame.Surface((TILESIZE,TILESIZE))
        #choose color based on number
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x,self.y = location
        self.mapX,self.mapY = location
        self.botLeft,self.topRight=values
        
    def update(self):
        self.scrollX,self.scrollY = self.game.getPlayerPosition()
        
    def reDraw(self,screen):
        print("here?")
        midX,midY=3,3
        self.drawX=self.mapX+midX-self.scrollX
        self.drawY=self.mapY+midY-self.scrollY
        screen.blit(self.image,pygame.Rect(self.drawX*TILESIZE, self.drawY*TILESIZE, TILESIZE,
        TILESIZE))
        pygame.draw.aaline(screen,BLACK,[self.drawX*TILESIZE, self.drawY*TILESIZE],
        [self.drawX*TILESIZE+TILESIZE, self.drawY*TILESIZE+TILESIZE],True)
        

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
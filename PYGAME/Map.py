import pygame
from settings import *

#this section of code will load a map
#Using it to load the large "megamap" that is the "backdrop" of the game
#code of the classes is mostly an edited version of Chris Bradfield's code for
#pygame sidescrolling, however all the comments are mine

class Map(object):
    def __init__(self,filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line)
        
        #this basically sets up how large the "larger" image is
        #it counts the number of "tiles" in one line of the textfile
        self.tilewidth=len(self.data[0])
        #and then counts the number of rows of tiles
        self.tileheight=len(self.data)
        #then sets the final dimensions using the tilesize in settings
        self.width=self.tilewidth*TILESIZE
        self.height=self.tileheight*TILESIZE
  
  
#this section of code tells the main game what portion of the map to draw
class Camera(object):
    def __init__(self,width,height):
        #sets where the camera will be with the game window dimensions
        self.camera=pygame.Rect(0,0,width,height)
        self.width=width
        self.height=height
        
    #the "entity" is the player's sprite
    #the entity's actions affect the coordinates of the camera rectangle's
    #top left coordinates
    def apply(self,entity):
        return entity.rect.move(self.camera.topleft)
      
    #the "target" is basically the camera's new location, in the form of a 
    #rectangle
    def update(self, target):
        #calculates the target's "topLeft" location
        x=-target.rect.x+int(WIDTH/2)
        y=-target.rect.y+int(HEIGHT/2)
        #changes the camera to match the target
        self.camera=pygame.Rect(x,y,self.width,self.height)
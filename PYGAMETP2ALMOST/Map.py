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
  
  

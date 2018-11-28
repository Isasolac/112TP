#CURRENTLY THIS IS DEAD CODE
#An initial draft of the player's "ghost" sprite...it was very confusing/buggy 
#So I decided to rebuild it so it could be more organized
#however I'm still keeping it as a past draft in case I decide to reuse parts

import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    #initializes the sprite's basic properties (loads the image)
    @staticmethod
    def init():
        ghostSprite.ghostImage = pygame.transform.scale(pygame.image.load("ghostSprite/ghostForwardMid.png").convert_alpha(),(TILESIZE,TILESIZE))
        
    
    def __init__(self,game,x,y):
        super(Player, self).__init__()
        #walk cycles/standing
        self.standing = [pygame.transform.scale(pygame.image.load("ghostSprite/ghostForwardMid.png").convert_alpha(),(TILESIZE,TILESIZE)),
        pygame.image.load("ghostSprite/ghostForwardLeft.png"),
        pygame.image.load("ghostSprite/ghostForwardMid.png"),
        pygame.image.load("ghostSprite/ghostForwardRight.png")]
        self.walkingRight = [pygame.image.load("ghostSprite/ghostRightMid.png"),
        pygame.image.load("ghostSprite/ghostRightFar.png")]
        self.walkingLeft = ["ghostSprite/ghostLeftMid.png","ghostSprite/ghostLeftFar.png"]
        #initial image
        self.image=self.standing[0]
        #walking counter/standing counter
        self.walkCount=0
        self.standCount=0
        self.standing=True
        #object center
        self.x, self.y, self.image, self.radius = x, y, image, radius
        #just in case I need to rotate...initialize image so it doesnt "grow"
        self.baseImage = image.copy()
        w, h = image.get_size()
        self.speed=5
        #more initializations later!
        
    
 
        
    def update(self, dt, keysDown, screenWidth, screenHeight):
        #moves the player horizontally
        if keysDown(pygame.K_RIGHT):
            self.x+=1
        elif keysDown(pygame.K_LEFT):
            self.x-=1
        #moves the player "forward and back" (vertically)
        elif keysDown(pygame.K_UP):
            self.y-=1
        elif keysDown(pygame.K_DOWN):
            self.y+=1
            

            
    
        
#settings framework borrowed from Chris Bradfield
import pygame
pygame.font.init()

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (148,0,241)
ICE = (173,216,230)
BROWN = (205,175,149)
ORANGE = (255,165,0)
SEAGREEN = (46,139,87)
FONT = pygame.font.SysFont("Times New Roman, Arial",15)
BIGFONT = pygame.font.SysFont("Times New Roman, Arial",30)

# game settings
WIDTH = 576   # 7 * 64 
HEIGHT = 576  # 8 * 64
FPS = 60
BGCOLOR = WHITE

#tile settings
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
'''
        else:
            #recursive case
            pygame.draw.polygon(screen,BLACK,triPoints,1)
            print(triPoints)
            #distance from center
            dFC=r-(length/(6*math.sqrt(3)))
            for point in triPoints:
                angle=pointMap[point]
                newCX,newCY=(cX+dFC*math.sin(angle)),(cY-dFC*math.cos(angle))
                xPoints[point]=newCX
                yPoints[point]=newCY
            #points
            p1,p2,p3=triPoints[0],triPoints[1],triPoints[2]
            #angles
            a1,a2,a3=pointMap[p1],pointMap[p2],pointMap[p3]
            #centerlocations
            cx1,cx2,cx3=xPoints[p1],xPoints[p2],xPoints[p3]
            cy1,cy2,cy3=yPoints[p1],yPoints[p2],yPoints[p3]
            newR=r-dFC
            self.drawKochSnowflake(screen,cx1,cy1,a1,newR,length,level-1)
            self.drawKochSnowflake(screen,cx2,cy2,a2,newR,length,level-1)
            self.drawKochSnowflake(screen,cx3,cy3,a3,newR,length,level-1)
            #self.drawKochSnowflake(screen,cX,cY,offsetAngle+math.pi/3,r,length,level)'''
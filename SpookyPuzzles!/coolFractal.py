import pygame
from settings import *
import math


class Snowflake(pygame.sprite.Sprite):
    def __init__(self,game):
        self.game=game
        self.mid=game.width/2
        #changes every time draw is called 10 times!
        self.level=3
        print(self.mid)
       
    def drawKochSnowflake(self,screen,cX,cY,offsetAngle,r,length,level):
        pointMap=dict()
        #draws itself at a center
        dA=2*math.pi/3
        triPoints=[]
        topPoint=(cX,cY-r)
        for n in range(3):
            angle=n*dA+offsetAngle
            x2,y2=(cX+r*math.sin(angle)),(cY-r*math.cos(angle))
            triPoints.append((x2,y2))
            #maps each new point to a relative angle
            pointMap[(x2,y2)]=angle
        if level==0:
            pygame.draw.polygon(screen,SEAGREEN,triPoints,3)
            print("level0!")
        else:
            #recursive case
            for point in triPoints:
                pAngle=pointMap[point]
                #distance from center
                dFC=r-(length/(6*math.sqrt(3)))
                newR=r-dFC
                newCX,newCY=(cX+dFC*math.sin(pAngle)),(cY-dFC*math.cos(pAngle))
                self.drawTriangle(screen,newCX,newCY,pAngle+math.pi/3,newR)
                self.drawKochSnowflake(screen,newCX,newCY,pAngle+math.pi/3,newR,length,level-1)
            
    
    def drawTriangle(self,screen,cX,cY,offsetAngle,r):
        #draws itself at a center
        dA=2*math.pi/3
        triPoints=[]
        topPoint=(cX,cY-r)
        for n in range(3):
            angle=n*dA+offsetAngle
            x2,y2=(cX+r*math.sin(angle)),(cY-r*math.cos(angle))
            triPoints.append((x2,y2))
        pygame.draw.polygon(screen,WHITE,triPoints,3)
        
    def reDraw(self,screen):
        pointMap=dict()
        cX,cY=self.mid,self.mid
        #draws itself at a center
        dA=2*math.pi/3
        r=150
        triPoints=[]
        topPoint=(cX,cY-r)
        length=r*2*math.sqrt(3)
        for n in range(3):
            angle=n*dA
            x2,y2=(cX+r*math.sin(angle)),(cY-r*math.cos(angle))
            triPoints.append((x2,y2))
            pointMap[(x2,y2)]=angle
        pygame.draw.polygon(screen,WHITE,triPoints,1)
        for point in triPoints:
            pAngle=pointMap[point]
            #distance from center
            dFC=r-(length/(6*math.sqrt(3)))
            newR=r-dFC
            newCX,newCY=(cX+dFC*math.sin(pAngle)),(cY-dFC*math.cos(pAngle))
            self.drawTriangle(screen,newCX,newCY,pAngle+math.pi/3,newR)
            self.drawKochSnowflake(screen,newCX,newCY,pAngle+math.pi/3,newR,length,2)
        self.drawKochSnowflake(screen,cX,cY,math.pi/3,r,length,3)
        

# koch-snowflake.py

'''import turtle

def kochSide(length, n):
    if (n == 1):
        turtle.forward(length)
    else:
        kochSide(length/3.0, n-1)
        turtle.left(60)
        kochSide(length/3.0, n-1)
        turtle.right(120)
        kochSide(length/3.0, n-1)
        turtle.left(60)
        kochSide(length/3.0, n-1)

def kochSnowflake(length, n):
    for step in range(3):
        kochSide(length, n)
        turtle.right(120)

turtle.delay(0)
turtle.speed(0)
turtle.penup()
turtle.goto(-300,100)
turtle.pendown()

turtle.pencolor("black")
kochSide(300, 4) # same as k4(300)

turtle.pencolor("blue")
kochSnowflake(300, 4)

turtle.penup()
turtle.goto(-250,50)
turtle.pendown()
turtle.pencolor("red")
kochSnowflake(200, 5)
turtle.done()'''
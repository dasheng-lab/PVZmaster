import pygame
import random
import sys
import time
import copy
from Event import *

screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

class Obstacle(EntityLike,pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        self.image=pygame.Surface((width,height))
        self.image.fill((255,255,255))
        self.image.set_alpha(0)
        self.rect=pygame.Rect(x,y,width,height)
    def draw(self,camera):
        screen.blit(self.image, pygame.Rect(self.rect.x-camera[0],self.rect.y-camera[1],self.rect.width,self.rect.height))
    def collide(self,other,x=0,y=0):
        new_rect=other.rect.copy()
        new_rect.move_ip(x * 10, y * 10)
        if new_rect.colliderect(self.rect):
            return 0
        else:
            return 1
    
obstacle_list0=[]
obstacle1=Obstacle(-1180,150,1250,450)
obstacle2=Obstacle(-2600,0,4000,150)
obstacle3=Obstacle(-2800,0,200,700)
obstacle4=Obstacle(-2600,700,4000,200)
obstacle5=Obstacle(1400,0,200,700)

obstacle_list0.append(obstacle1)
obstacle_list0.append(obstacle2)
obstacle_list0.append(obstacle3)
obstacle_list0.append(obstacle4)
obstacle_list0.append(obstacle5)

obstacle_list1=[]
obstacl6=Obstacle(-1000,-100,2000,130)
obstacl7=Obstacle(-1000,1270,2000,200)
obstacl8=Obstacle(-1200,0,230,1300)
obstacl9=Obstacle(970,0,200,1300)

obstacle10=Obstacle(-1000,430,750,30)
obstacle11=Obstacle(-820,920,1000,30)
obstacle12=Obstacle(-820,920,30,700)
obstacle13=Obstacle(380,920,270,30)
obstacle14=Obstacle(650,920,30,300)
obstacle15=Obstacle(-300,430,30,300)
obstacle16=Obstacle(-260,290,30,170)
obstacle17=Obstacle(-145,280,350,30)
obstacle18=Obstacle(-300,840,30,80)
obstacle19=Obstacle(-350,700,300,30)
obstacle20=Obstacle(160,0,30,280)
obstacle21=Obstacle(650,1200,130,30)
obstacle22=Obstacle(750,570,60,350)
obstacle23=Obstacle(800,820,200,30)
obstacle24=Obstacle(-465,280,30,230)
obstacle25=Obstacle(-880,850,100,70)

obstacle_list1.append(obstacl6)
obstacle_list1.append(obstacl7)
obstacle_list1.append(obstacl8)
obstacle_list1.append(obstacl9)
obstacle_list1.append(obstacle10)
obstacle_list1.append(obstacle11)
obstacle_list1.append(obstacle12)
obstacle_list1.append(obstacle13)
obstacle_list1.append(obstacle14)
obstacle_list1.append(obstacle15)
obstacle_list1.append(obstacle16)
obstacle_list1.append(obstacle17)
obstacle_list1.append(obstacle18)
obstacle_list1.append(obstacle19)
obstacle_list1.append(obstacle20)
obstacle_list1.append(obstacle21)
obstacle_list1.append(obstacle22)
obstacle_list1.append(obstacle23)
obstacle_list1.append(obstacle24)
obstacle_list1.append(obstacle25)

obstacl_class=[obstacle_list0,obstacle_list1]
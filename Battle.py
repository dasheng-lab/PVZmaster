import pygame
import random
import sys
import time
import copy
from Creature import *
from Event import *

moneyimage=pygame.image.load("images/钱数.png")
moneyimage=pygame.transform.scale(moneyimage,(150,50))
moneybox=Button(700,350,75,75,"images/钱袋.png")
sunflower_image=pygame.image.load("images/向日葵卡.png")
sunflower_image=pygame.transform.scale(sunflower_image,(55,80))
nut_image=pygame.image.load("images/坚果卡.png")
nut_image=pygame.transform.scale(nut_image,(55,80))
melon_image=pygame.image.load("images/窝瓜卡.png")
melon_image=pygame.transform.scale(melon_image,(55,80))

sunflower_coldimage=pygame.image.load("images/向日葵冷却.png")
sunflower_coldimage=pygame.transform.scale(sunflower_coldimage,(55,80))
nut_coldimage=pygame.image.load("images/坚果冷却.png")
nut_coldimage=pygame.transform.scale(nut_coldimage,(55,80))
melon_coldimage=pygame.image.load("images/窝瓜冷却.png")
melon_coldimage=pygame.transform.scale(melon_coldimage,(55,80))

add_hp=Button(100,0,50,50,"images/加号.png")

pygame.font.init()
font = pygame.font.Font(f"word/pop.ttf", 30)
font1 = pygame.font.Font(f"word/pop.ttf", 20)
jindut0=pygame.image.load("images/进度条0.png")
jindut0=pygame.transform.scale(jindut0,(150,25))
jindut1=pygame.image.load("images/进度条1.png")
jindut1=pygame.transform.scale(jindut1,(150,25))
jindut2=pygame.image.load("images/进度条2.png")
jindut2=pygame.transform.scale(jindut2,(150,25))

sunflowerfunc_frame=[]
for i in range(1,7):
    picture=pygame.image.load(f"images/向日葵头亮/图层-{i}.png").convert_alpha()
    sunflowerfunc_frame.append(picture)

sunflower_frame=[sunflowernor_frame,sunflowerfunc_frame]

nuthurt1_frame=[]
for i in range(1,9):
    picture=pygame.image.load(f"images/坚果1/图层-{i}.png").convert_alpha()
    nuthurt1_frame.append(picture)
nuthurt2_frame=[]
for i in range(1,9):
    picture=pygame.image.load(f"images/坚果2/图层-{i}.png").convert_alpha()
    nuthurt2_frame.append(picture)
nut_set=[nut_frame,nuthurt1_frame,nuthurt2_frame]

melonjump_frame=[]
for i in range(1,5):
    for j in range(1,3):
        picture=pygame.image.load(f"images/窝瓜跳跃/图层-{i}.png").convert_alpha()
        melonjump_frame.append(picture)

cold_dict={"1":[sunflower_coldimage,50],"3":[nut_coldimage,50],"4":[melon_coldimage,50]}
place_dict={"1":280,"3":335,"4":390}


class Level(Listener):
    def __init__(self):
        self.level=1
        self.count=0
        self.win_count=0
        self.hp=0
    def level_start(self):
        if self.count>400 and self.win_count<=self.level*5+10:
            self.count=0
            emg.AIput(player.rect.x,player.rect.y)
            self.win_count+=1
        else:
            self.count+=1
        if self.win_count>=self.level*5+10:
            for zombie in emg.zombie_list:
                if zombie.HP>=0:
                    self.hp+=zombie.HP
            if self.hp<=0:
                moneybox.draw()
            else:
                self.hp=0
        if moneybox.is_clicked():
            self.win_count=0
            self.level+=1
            global lawn_avaible
            for lawn in lawn_avaible.keys():
                lawn_avaible[lawn]=True
            player_money.add_money(100+20*self.level+int(0.1*card_box.sunshine))
            self.post(Event(Event_kind.CHANGE_BAKEGROUND,
            {"background":2,"x":-2600,"y":0}))
        if self.level>=6:
            self.post(Event(Event_kind.GAMEOVER))


class Money():
    def __init__(self):
        self.money=0
        self.image=moneyimage
    def add_money(self,num):
        self.money+=num
    def reduce_money(self,num):
        self.money-=num
    def draw(self):
        screen.blit(self.image,(0,650))
        text1=font.render(f"{self.money}",True,(127,255,127))
        screen.blit(text1,(58,665))

the_level=Level()
player_money=Money()
lawn_avaible={}

class Card():
    def __init__(self):
        self.plant=[False,True,False,True,True]#1向日葵，3坚果，4窝瓜
        self.plant_cold=[0,200,0,0,0]
        self.image=self.dialog_surface = pygame.image.load("images/卡槽.png")
        self.rect=pygame.Rect(200,0,1000,200)
        self.clicked=0
        self.sunshine=50
        self.active=0
        self.suncount=0
    def draw(self):
        self.suncount+=1
        if self.suncount>=500:
            self.suncount=0
            self.sunshine+=25
        self.plant_cold[1]=min(self.plant_cold[1]+1,200)
        self.plant_cold[3]=min(self.plant_cold[3]+1,1200)
        self.plant_cold[4]=min(self.plant_cold[4]+1,2000)
        text1=font1.render(f"{self.sunshine}",True,(0,0,0))
        screen.blit(self.image,self.rect)
        screen.blit(text1,(210,65))
        if self.plant[1]:
            if self.plant_cold[1]>=200 and self.sunshine>=50:
                screen.blit(sunflower_image,(280,0,55,80))
            else:
                screen.blit(sunflower_coldimage,(280,0,55,80))
        if self.plant[3]:
            if self.plant_cold[3]>=1200 and self.sunshine>=50:
                screen.blit(nut_image,(335,0,55,80))
            else:
                screen.blit(nut_coldimage,(335,0,55,80))
        if self.plant[4]:
            if self.plant_cold[4]>=2000 and self.sunshine>=50:
                screen.blit(melon_image,(390,0,55,80))
            else:
                screen.blit(melon_coldimage,(390,0,55,80))
        if self.active!=0:
            screen.blit(cold_dict[f"{self.active}"][0],
            (place_dict[f"{self.active}"],0,55,80))
        if the_level.win_count<=the_level.level*2+10:
            screen.blit(jindut0,(800,660))
        if (the_level.win_count>the_level.level*2+10 
            and the_level.win_count<=the_level.level*3+10):
            screen.blit(jindut1,(800,660))
        if the_level.win_count>the_level.level*3+10:
            screen.blit(jindut2,(800,660))
    def is_clicked(self):
        mouse_pos=pygame.mouse.get_pos()
        mouse_buttons=pygame.mouse.get_pressed()
        if self.active==0:
            if (self.plant[1]
                and self.clicked>=20 
                and pygame.Rect(280,0,55,80).collidepoint(mouse_pos)
                and mouse_buttons[0]
                and self.sunshine>=50
                and self.plant_cold[1]>=200):
                self.active=1
                self.clicked=0
            if (self.plant[3]
                and self.clicked>=20 
                and pygame.Rect(335,0,55,80).collidepoint(mouse_pos)
                and mouse_buttons[0]
                and self.sunshine>=50
                and self.plant_cold[3]>=1200):
                self.active=3
                self.clicked=0
            if (self.plant[4]
                and self.clicked>=20 
                and pygame.Rect(390,0,55,80).collidepoint(mouse_pos)
                and mouse_buttons[0]
                and self.sunshine>=50
                and self.plant_cold[4]>=2000):
                self.active=4
                self.clicked=0
            else:
                self.clicked+=1
            if add_hp.is_clicked():
                if player.hp<player.besthp:
                    if self.sunshine>=(player.besthp-player.hp)*5:
                        self.sunshine-=(player.besthp-player.hp)*5
                        player.hp=player.besthp
                    else:
                        player.hp+=self.sunshine//5
                        self.sunshine=self.sunshine%5
    def grow(self):
        mouse_pos=pygame.mouse.get_pos()
        mouse_buttons=pygame.mouse.get_pressed()
        global plant_list
        for lawn in lawn_dict.keys():
            if (lawn_dict[lawn].rect.collidepoint(mouse_pos) 
            and mouse_buttons[0]):
                if self.active==1:
                    if lawn_avaible[lawn]:
                        self.sunshine-=50
                        self.plant_cold[1]=0
                        self.active=0
                        plant_list.append(Sunflower(lawn_dict[lawn].x,lawn_dict[lawn].y))
                        lawn_avaible[lawn]=False
                    else:
                        self.active=0
                if self.active==3:
                    if lawn_avaible[lawn]:
                        self.sunshine-=50
                        self.plant_cold[3]=0
                        self.active=0
                        plant_list.append(Nut(lawn_dict[lawn].x,lawn_dict[lawn].y))
                        lawn_avaible[lawn]=False
                    else:
                        self.active=0
                if self.active==4:
                    if lawn_avaible[lawn]:
                        self.sunshine-=50
                        self.plant_cold[4]=0
                        self.active=0
                        plant_list.append(Melon(lawn_dict[lawn].x,
                        lawn_dict[lawn].y))
                        lawn_avaible[lawn]=False
                    else:
                        self.active=0
card_box=Card()

plant_list=[]
lawn_dict={}

class Rect1():
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.rect=pygame.Rect(x,y,width,height)
        self.width=width
        self.height=height
    def update(self,camera):
        self.rect.x=self.x-camera[0]
        self.rect.y=self.y-camera[1]


for i in range(9):
    for j in range(5):
        lawn_dict["lawn_rect"+str(i)+str(j)]=Rect1(162+i*84.5,
                                                   184+j*98,86.5,98)
        lawn_avaible["lawn_rect"+str(i)+str(j)]=True


class Sunflower():
    def __init__(self,x,y):
        self.hp=800
        self.x=x
        self.y=y
        self.pic_diex=0
        self.kind=0
        self.funccount=0
        self.stacount=0
        self.blight=0
    def draw(self,camera):
        self.pic_diex+=0.2
        plant_blit=int(self.pic_diex%len(NPC_list[1]))
        self.image=NPC_list[1][plant_blit]
        self.rect=self.image.get_rect()
        self.rect.x=self.x-camera[0]+20
        self.rect.y=self.y-camera[1]+10
        if self.blight==0:
            screen.blit(self.image,pygame.Rect(self.rect.x-camera[0],
            self.rect.y-camera[1]-(self.rect.width-65),self.rect.width,self.rect.height))
        elif self.blight<=3:
            self.blight+=1
            story=copy.copy(self.image)
            screen.blit(changecolor(story,1.5,1.5,1.5),pygame.Rect(self.rect.x-camera[0],
            self.rect.y-camera[1]-(self.rect.width-65),self.rect.width,self.rect.height))
        else:
            self.blight=0
            screen.blit(self.image,pygame.Rect(self.rect.x-camera[0],
            self.rect.y-camera[1]-(self.rect.width-65),self.rect.width,self.rect.height))
        
        if self.kind==1:
            self.pic_diex+=0.2
            plant_blit=int(self.pic_diex%len(sunflowerfunc_frame))
            self.image=sunflowerfunc_frame[plant_blit]
            self.rect=self.image.get_rect()
            self.rect.x=self.x-camera[0]+20
            self.rect.y=self.y-camera[1]+10
            screen.blit(self.image,self.rect)
    def func(self,camera):
        self.funccount+=1
        if self.funccount>=500:
            card_box.sunshine+=25
            self.funccount=0
            self.kind=1
        if self.kind==1:
            self.stacount+=1
        if self.stacount>=30:
            self.stacount=0
            self.kind=0
    def is_eaten(self,camera):
        for zombie in emg.zombie_list:
            if (pygame.Rect(self.rect.x-camera[0],self.rect.y-camera[1]-(self.rect.width-65),
                           self.rect.width,self.rect.height).colliderect(pygame.
                            Rect(zombie.rect.x-camera[0]+10,
                                 zombie.rect.y-camera[1]+20,
                            zombie.rect.width/3,zombie.rect.height/3) )
                            and zombie.style!=8 and zombie.style!=9 and zombie.HP>70):
                zombie.style=10
                self.hp-=8
                self.blight=1
        if self.hp<=0:
            plant_list.remove(self)
            for lawn in lawn_dict.keys():
                if lawn_dict[lawn].x==self.x and lawn_dict[lawn].y==self.y:
                    lawn_avaible[lawn]=True


class Nut():
    def __init__(self,x,y):
        self.hp=10000
        self.x=x
        self.y=y
        self.pic_diex=0
        self.kind=3
        self.blight=0
        self.status=0
    def draw(self,camera):
        self.pic_diex+=0.2
        plant_blit=int(self.pic_diex%len(nut_set[self.status]))
        self.image=nut_set[self.status][plant_blit]
        self.rect=self.image.get_rect()
        self.rect.x=self.x-camera[0]+20
        self.rect.y=self.y-camera[1]+10
        if self.blight==0:
            screen.blit(self.image,pygame.Rect(self.rect.x-camera[0],
            self.rect.y-camera[1]-(self.rect.width-65),self.rect.width,self.rect.height))
        elif self.blight<=3:
            self.blight+=1
            story=copy.copy(self.image)
            screen.blit(changecolor(story,1.5,1.5,1.5),pygame.Rect(self.rect.x-camera[0],
            self.rect.y-camera[1]-(self.rect.width-65),self.rect.width,self.rect.height))
        else:
            self.blight=0
            screen.blit(self.image,pygame.Rect(self.rect.x-camera[0],
            self.rect.y-camera[1]-(self.rect.width-65),self.rect.width,self.rect.height))
    def func(self,camera):
        if self.hp<=6000 and self.hp>=3000:
            self.status=1
        if self.hp<3000:
            self.status=2
    def is_eaten(self,camera):
        for zombie in emg.zombie_list:
            if (pygame.Rect(self.rect.x-camera[0],self.rect.y-camera[1]-(self.rect.width-65),
                           self.rect.width,self.rect.height).colliderect(pygame.
                            Rect(zombie.rect.x-camera[0]+10,
                                 zombie.rect.y-camera[1]+20,
                            zombie.rect.width/3,zombie.rect.height/3) )
                            and zombie.style!=8 and zombie.style!=9 and zombie.HP>70):
                zombie.style=10
                self.hp-=8
                self.blight=1
        if self.hp<=0:
            plant_list.remove(self)
            for lawn in lawn_dict.keys():
                if lawn_dict[lawn].x==self.x and lawn_dict[lawn].y==self.y:
                    lawn_avaible[lawn]=True
class Melon():
    def __init__(self,x,y):
        self.hp=800
        self.x=x
        self.y=y
        self.pic_diex=0
        self.pic_diex1=0
        self.kind=4
        self.blight=0
        self.countfunc=0
        self.funx=0
    def draw(self,camera):
        if self.funx==1:
            if self.countfunc<=40:
                self.pic_diex1+=0.2
                plant_blit1=int(self.pic_diex1%len(melonjump_frame))
                self.image=melonjump_frame[plant_blit1]
                screen.blit(self.image,pygame.Rect(self.rect.x-camera[0],
                self.rect.y-camera[1]-(self.rect.width-65)+self.pic_diex1*12,self.rect.width,self.rect.height))
                self.countfunc+=1
            else:
                self.countfunc=0
                plant_list.remove(self)
                for lawn in lawn_dict.keys():
                    if lawn_dict[lawn].x==self.x and lawn_dict[lawn].y==self.y:
                        lawn_avaible[lawn]=True
        else:
            self.pic_diex+=0.2
            plant_blit=int(self.pic_diex%len(NPC_list[self.kind]))
            self.image=NPC_list[self.kind][plant_blit]
            self.rect=self.image.get_rect()
            self.rect.x=self.x-camera[0]+20
            self.rect.y=self.y-camera[1]+10
            if self.blight==0:
                screen.blit(self.image,pygame.Rect(self.rect.x-camera[0],
                self.rect.y-camera[1]-(self.rect.width-65),self.rect.width,self.rect.height))
            elif self.blight<=3:
                self.blight+=1
                story=copy.copy(self.image)
                screen.blit(changecolor(story,1.5,1.5,1.5),pygame.Rect(self.rect.x-camera[0],
                self.rect.y-camera[1]-(self.rect.width-65),self.rect.width,self.rect.height))
            else:
                self.blight=0
                screen.blit(self.image,pygame.Rect(self.rect.x-camera[0],
                self.rect.y-camera[1]-(self.rect.width-65),self.rect.width,self.rect.height))
    def func(self,camera):
        if self.funx==0:
            for zombie in emg.zombie_list:
                if (pygame.Rect(self.rect.x-camera[0],self.rect.y-camera[1]-(self.rect.width-65),
                            self.rect.width,self.rect.height).colliderect(pygame.
                                Rect(zombie.rect.x-camera[0]-20,
                                    zombie.rect.y-camera[1]+20,
                                zombie.rect.width*2,zombie.rect.height/3) )
                                and zombie.style!=8 and zombie.style!=9 and zombie.HP>70):
                    self.funx=1
                    zombie.style=9
                    self.rect.x=zombie.rect.x
                    self.rect.y=zombie.rect.y
    
    def is_eaten(self,camera):
        for zombie in emg.zombie_list:
            if (pygame.Rect(self.rect.x-camera[0],self.rect.y-camera[1]-(self.rect.width-65),
                           self.rect.width,self.rect.height).colliderect(pygame.
                            Rect(zombie.rect.x-camera[0]+10,
                                 zombie.rect.y-camera[1]+20,
                            zombie.rect.width/3,zombie.rect.height/3) )
                            and zombie.style!=8 and zombie.style!=9 and zombie.HP>70):
                zombie.style=10
                self.hp-=8
                self.blight=1
        if self.hp<=0:
            plant_list.remove(self)
            for lawn in lawn_dict.keys():
                if lawn_dict[lawn].x==self.x and lawn_dict[lawn].y==self.y:
                    lawn_avaible[lawn]=True
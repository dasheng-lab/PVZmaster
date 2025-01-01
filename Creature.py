import pygame
import random
import sys
import time
import copy
from Event import *
from Obstacle import *
from Openai import *

pygame.font.init()
font2 = pygame.font.Font(f"word/pop.ttf", 25)


camera_lack=300
bulletlist_right=pygame.sprite.Group()
bulletlist_left=pygame.sprite.Group()
shooter_count=0
frame=[]
for i in range(1,19):
    fm_cjs=pygame.image.load(f"images/commonjs/cjs{i}.png").convert_alpha()
    frame.append(fm_cjs)

player_frame=[]
for i in range(1,14):
    picture=pygame.image.load(f"images/shootermove/图层 {i}.png").convert_alpha()
    player_frame.append(picture)
sunflowernor_frame=[]
for i in range(1,19):
    picture=pygame.image.load(f"images/player's wife/图层 {i}.png").convert_alpha()
    sunflowernor_frame.append(picture)
daifu_frame=[]
for i in range(1,16):
    picture=pygame.image.load(f"images/戴夫/图层-{i}.png").convert_alpha()
    picture=pygame.transform.scale(picture,(120,200))
    daifu_frame.append(picture)
nut_frame=[]
for i in range(1,9):
    picture=pygame.image.load(f"images/坚果/坚果图层-{i}.png").convert_alpha()
    nut_frame.append(picture)
melon_frame=[]
for i in range(1,18):
    picture=pygame.image.load(f"images/窝瓜/图层-{i}.png").convert_alpha()
    melon_frame.append(picture)

cjsdiewalk_frame=[]
for i in range(1,19):
    picture=pygame.image.load(f"images/cjsdiewalk/cjsdiewalk图层-{i}.png").convert_alpha()
    cjsdiewalk_frame.append(picture)
head_frame=[]
for i in range(1,13):
    picture=pygame.image.load(f"images/掉头/头图层-{i}.png").convert_alpha()
    head_frame.append(picture)
cjsfall_frame=[]
for i in range(1,11):
    picture=pygame.image.load(f"images/僵尸死/僵尸死图层-{i}.png").convert_alpha()
    cjsfall_frame.append(picture)
cjseat_frame=[]
for i in range(1,22):
    picture=pygame.image.load(f"images/cjseat/cjseat图层-{i}.png").convert_alpha()
    cjseat_frame.append(picture)
#pygame.font.init()
#font = [pygame.font.Font(pygame.font.get_default_font(),font_size) for font_size in [48, 36, 24]]

NPC_list=[]
NPC_list.append(daifu_frame)
NPC_list.append(sunflowernor_frame)
NPC_list.append(daifu_frame)
NPC_list.append(nut_frame)
NPC_list.append(melon_frame)

over=False
enter=False
fight=False
insert=False
Help=False
n=0
ji=0

class Player(EntityLike,pygame.sprite.Sprite):
    def __init__(self,x=200,y=200):
        self.image=pygame.image.load("images/shootermove/图层 1.png").convert_alpha()
        self.blood_image=pygame.image.load("images/血量.png").convert_alpha()
        self.blood_image=pygame.transform.scale(self.blood_image,(150,90))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.speed=5
        self.pic_diex=0
        self.hp=800
        self.besthp=800
        self.blight=0
        self.place=0
        self.beat=20
        self.shoot_speed=50
    def listen(self, event: Event):  # 玩家类所响应的事件
        if event.code == pygame.KEYDOWN:  # 键盘按下事件
            self.keydown()
        if event.code == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.code == Event_kind.CAN_MOVE:  # 响应场景发出的允许移动事件
            self.rect.x = event.body["POS"][0]
            self.rect.y = event.body["POS"][1]
        super().listen(event)  # 继承原有的响应事件内容，如对DRAW的响应

    def keydown(self):  # 键盘按下事件的响应
        keys=pygame.key.get_pressed()
        stay0__1obstacle=obstacl_class[self.place][0].collide(self,0,-1)
        stay0_1obstacle=obstacl_class[self.place][0].collide(self,0,1)
        stay1__0obstacle=obstacl_class[self.place][0].collide(self,-1,0)
        stay1_0obstacle=obstacl_class[self.place][0].collide(self,1,0)
        for obstale in obstacl_class[self.place][1:len(obstacl_class[self.place])]:
            stay0__1obstacle*=obstale.collide(self,0,-1)
            stay0_1obstacle*=obstale.collide(self,0,1)
            stay1__0obstacle*=obstale.collide(self,-1,0)
            stay1_0obstacle*=obstale.collide(self,1,0)
        if keys[pygame.K_w] and stay0__1obstacle==1:
            self.rect.y-=self.speed
        if keys[pygame.K_s] and stay0_1obstacle==1:
            self.rect.y+=self.speed
        if keys[pygame.K_a] and stay1__0obstacle==1:
            self.rect.x-=self.speed
        if keys[pygame.K_d] and stay1_0obstacle==1:
            self.rect.x+=self.speed
            self.post(Event(Event_kind.REQUEST_MOVE, {"POS": (self.rect.x, self.rect.y)}))

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        if keys[pygame.K_SPACE]:
            global shooter_count 
            shooter_count=min(shooter_count+1,self.shoot_speed)
            if shooter_count==self.shoot_speed:
                if self.rect.x>-1000:
                    bulletlist_right.add(Bullet(self))
                else:
                    bulletlist_left.add(Bullet(self))
                shooter_count=0
        
        if keys[pygame.K_1]:
            text0=f"beat={self.beat},shoot_speed={self.shoot_speed},besthp={self.besthp},speed={self.speed}"
            self.post(Event(Event_kind.WORDS,{"text":text0}))

    def draw(self,camera,style):
        self.pic_diex+=0.2
        player_blit=int(self.pic_diex%len(player_frame))
        player_image=player_frame[player_blit]
        player_rect=player_image.get_rect()
        if style==2 or style==6 :
            if camera[0]+500-self.rect.x>camera_lack and camera[0]>-2600:
                camera[0]=self.rect.x-500+camera_lack
            if -camera[0]-500+self.rect.x>camera_lack and camera[0]<400:
                camera[0]=self.rect.x-500-camera_lack
            if camera[0]<-1000:
                player_image=pygame.transform.flip(player_image,True,False)
        if style==7:
            if camera[0]+500-self.rect.x>camera_lack and camera[0]>-1000:
                camera[0]=self.rect.x-500+camera_lack
            if -camera[0]-500+self.rect.x>camera_lack and camera[0]<0:
                camera[0]=self.rect.x-500-camera_lack
            if camera[1]+350-self.rect.y>camera_lack and camera[1]>0:
                camera[1]=self.rect.y-350+camera_lack
            if -camera[1]-300+self.rect.y>camera_lack and camera[1]<600:
                camera[1]=self.rect.y-300-camera_lack
            
        #self.rect.x=self.x-camera[0]
        #self.rect.y=self.y-camera[1]-(player_rect.width-65)
        self.be_eaten(camera)
        if self.blight==0:
            screen.blit(player_image,pygame.Rect(self.rect.x-camera[0],self.rect.y-camera[1]-(player_rect.width-65),player_rect.width,player_rect.height))
        elif self.blight<=3:
            self.blight+=1
            story=copy.copy(player_image)
            screen.blit(changecolor(story,1.5,1.5,1.5),pygame.Rect(self.rect.x-camera[0],self.rect.y-camera[1]-(player_rect.width-65),player_rect.width,player_rect.height))
        else:
            self.blight=0
            screen.blit(player_image,pygame.Rect(self.rect.x-camera[0],
            self.rect.y-camera[1]-(player_rect.width-65),player_rect.width,player_rect.height))
        screen.blit(self.blood_image,(0,-20))
        text1=font2.render(f"{self.hp}",True,(0,0,0))
        screen.blit(text1,(50,16))
    def be_eaten(self,camera):
        for zombie in emg.zombie_list:
            if pygame.Rect(self.rect.x-camera[0],self.rect.y-camera[1]-(self.rect.width-65),
                           self.rect.width,self.rect.height).colliderect(pygame.Rect(zombie.rect.x-camera[0],zombie.rect.y-camera[1],
                            zombie.rect.width,zombie.rect.height) ) and zombie.style!=8 and zombie.style!=9 and zombie.HP>70:
                zombie.style=10
                self.hp-=8
                self.blight=1
                if self.hp<=0:
                    self.hp=300
                    self.post(Event(Event_kind.EATEN,{"objecct":player}))
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self,shooter):
        super().__init__()
        self.image=pygame.image.load("images/bullet.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(22,22))
        self.rect=self.image.get_rect()
        self.rect.x=shooter.rect.x+35
        self.rect.y=shooter.rect.y+5.5
        self.speed=5
        self.pic_diex=0
    def draw(self,camera):
        screen.blit(self.image, pygame.Rect(self.rect.x-camera[0],
        self.rect.y-camera[1],self.rect.width,self.rect.height)) 
    def move(self):
        #7 在屏幕范围内，实现往右移动
        if -1000<self.rect.x < 1000:
            self.rect.x += self.speed
        elif self.rect.x >= 1000:#8 子弹飞出屏幕，从精灵组删除
            self.kill()
        elif -2600<self.rect.x<=-1000:
            self.rect.x -= self.speed
        else:
            self.kill()
    def crash_zombie(self):
        for zombie in emg.zombie_list:
            if (self.rect.colliderect(zombie.rect)
                and zombie.style!=8
                and zombie.style!=9):
                zombie.HP-=player.beat
                zombie.style=3
                self.kill()

count_zombie=0

class ZombieManager(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.zombie_list=[]
        self.move_speed=0.5
        self.dealing=0
        self.count=0
    def gen_new_zombie(self,gen):
        #gen=random.choice([425,315,230,125,25])
        self.zombie_list.append(Zombie(1000,gen))
    def AIput(self,x,y):
        staystr=AI_decision(x,y)
        if "425" in staystr:
            self.gen_new_zombie(425)
        elif "315" in staystr:
            self.gen_new_zombie(315)
        elif "230" in staystr:
            self.gen_new_zombie(230)
        elif "125" in staystr:
            self.gen_new_zombie(125)
        elif "25" in staystr:
            self.gen_new_zombie(25)
        else:
            gen1=random.choice([425,315,230,125,25])
            self.gen_new_zombie(gen1)
        
    def move(self):
        for js in self.zombie_list:
            js.move()
    def draw(self,camera):
        for jsd in self.zombie_list:
            jsd.draw(camera)

player=Player()
emg=ZombieManager()

class Zombie(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.style=0
        self.x=x
        self.y=y
        self.HP=270
        self.move_speed=0.3
        self.cjsindex=0
        self.headindex=0
        self.fallindex=0
        self.eatindex=0
        self.image=pygame.image.load("images/commonjs/cjs1.png").convert_alpha()
        self.image2=pygame.image.load("images/cjsdiewalk/cjsdiewalk图层-1.png"
        ).convert_alpha()
        self.rect=self.image.get_rect()
        self.rect2=self.image2.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
        self.n=0
        self.dealing=0
    def draw(self,camera):
        if self.style==0 : #正常移动
            self.cjsindex+=0.1
            cjsblit=int(self.cjsindex%len(frame))
            self.rect.x=self.x
            self.rect.y=screen_height-(self.y+frame[cjsblit].get_height())
            screen.blit(frame[cjsblit],(self.rect.x-camera[0],self.rect.y-camera[1],
            self.rect.width,self.rect.height))
        elif self.style==3 : #被子弹击中
            if self.HP>70:
                self.cjsindex+=0.1
                cjsblit=int(self.cjsindex%len(frame))
                self.rect.x=self.x
                self.rect.y=screen_height-(self.y+frame[cjsblit].get_height())
                story=copy.copy(frame[cjsblit])
                if self.n<3:
                    self.n+=1
                    screen.blit(changecolor(story,1.6,1.6,1.6),(self.rect.x-camera[0],
                    self.rect.y-camera[1],self.rect.width,self.rect.height))
                if self.n==3:
                    self.n=0
                    self.style=0
            elif self.HP<=70 and self.HP>0:
                self.cjsindex+=0.1
                cjsblit=int(self.cjsindex%len(cjsdiewalk_frame))
                self.rect2.x=self.x
                self.rect2.y=screen_height-(self.y+cjsdiewalk_frame[cjsblit].get_height())
                story=copy.copy(cjsdiewalk_frame[cjsblit])
                if self.n<3:
                    self.n+=1
                    screen.blit(changecolor(story,1.6,1.6,1.6),(self.rect2.x-camera[0],
                    self.rect2.y-camera[1],self.rect.width,self.rect.height))
                if self.n==3:
                    self.n=0
                    self.style=7

        elif self.style==4 : #失败未进家
            self.rect.x=self.x
            self.rect.y=screen_height-(self.y+self.image.get_height())
            screen.blit(self.image,(self.rect.x-camera[0],self.rect.y-camera[1]))

        elif self.style==5 : #失败进家
            self.y=200
            self.rect.x=self.x
            self.cjsindex+=0.1
            cjsblit=int(self.cjsindex%len(frame))
            self.y=screen_height-(self.y+frame[cjsblit].get_height())
            screen.blit(frame[cjsblit],(self.x-camera[0],self.y-camera[1]))
            zombie_rect = fm_cjs.get_rect()
            zombie_rect.x = self.x
            zombie_rect.y = self.y
            self.image=frame[cjsblit]
        elif self.style==6 : #失败未进家但吃完脑子
            if self.dealing==0:
                self.image = changecolor(self.image, 0.5,0.5,0.5)
                self.dealing=1
            screen.blit(self.image,(self.rect.x-camera[0],self.rect.y-camera[1]))
        elif self.style==7 : #无头行走
            self.HP-=0.3
            self.cjsindex+=0.1
            cjsblit=int(self.cjsindex%len(cjsdiewalk_frame))
            self.rect2.x=self.x
            self.rect2.y=screen_height-(self.y+cjsdiewalk_frame[cjsblit].get_height())
            screen.blit(cjsdiewalk_frame[cjsblit],(self.rect2.x-camera[0],
            self.rect2.y-camera[1],self.rect.width,self.rect.height))
        elif self.style==8 : #尸体倒下
            self.fallindex+=0.1
            fallblit=int(self.fallindex)
            if fallblit<len(cjsfall_frame):
                rect=cjsfall_frame[fallblit].get_rect()
                screen.blit(cjsfall_frame[fallblit],
            (self.rect2.x-camera[0]-rect.width+self.rect.width-10,
             self.rect2.y-camera[1]-rect.height+self.rect.height-22,
             self.rect.width,self.rect.height))
            else:
                self.style=9 
        elif self.style==9 : #尸体倒下后消失
            self.kill()
        elif self.style==10 : #吃植物
            self.eatindex+=0.2
            eatblit=int(self.eatindex%len(cjseat_frame))
            #self.rect.x=self.x
            #self.rect.y=screen_height-(self.y+cjseat_frame[eatblit].get_height())
            screen.blit(cjseat_frame[eatblit],(self.rect.x-camera[0],self.rect.y-camera[1]))
            if not pygame.Rect(player.rect.x-camera[0]
                            ,player.rect.y-camera[1]-(player.rect.width-65),
                           player.rect.width,player.rect.height).colliderect(pygame.
                            Rect(self.rect.x-camera[0],
                            self.rect.y-camera[1],
                            self.rect.width,self.rect.height)):
                self.style=0
        if self.HP<=70 :
            if self.dealing<1:
                global temp
                temp=(self.rect2.x,self.rect2.y)
                self.dealing+=1
            self.headindex+=0.1
            headblit=int(self.headindex)
            if headblit<len(head_frame):
                head=Head(head_frame[headblit],
                temp[0]+f(self.headindex),temp[1]+g(self.headindex,0.5))
                head.draw(camera)
    def move(self):
        self.x-=self.move_speed
    def is_dead(self):
        if self.HP<=70 and self.HP>0:
            self.style=7
            return True
        else:
            return False
    def is_fall(self):
        if self.HP<=0:
            self.style=8
            return True
        else:
            return False
    def is_end(self):
        if self.x<=70 and self.style==0:
            self.style=1
            return True
        else:
            return False


class Button():
    def __init__(self,x,y,width,height,image):
        self.x=x
        self.y=y
        self.image=pygame.transform.scale(pygame.image.load(image).
            convert_alpha(),(width,height))
        self.image2=changecolor(pygame.transform.scale(pygame.image.load(image).
            convert_alpha(),(width,height)), 1.2,1.2,1.2)
        self.rect=pygame.Rect(x,y,width,height)
        self.clicked=20
    def draw(self):
        mouse_pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.image2,(self.x,self.y))
        else:
            screen.blit(self.image,(self.x,self.y))
    def is_clicked(self):
        mouse_pos=pygame.mouse.get_pos()
        mouse_buttons=pygame.mouse.get_pressed()
        if (self.clicked>=20 and self.rect.collidepoint(mouse_pos) 
            and mouse_buttons[0]):
            self.clicked=0
            return self.rect.collidepoint(mouse_pos) and mouse_buttons[0] 
        else:
            self.clicked+=1
            return False

class Button2():
    def __init__(self,x,y,width,height,image):
        self.x=x
        self.y=y
        self.image=pygame.transform.scale(pygame.image.load(image).
        convert_alpha(),(width,height))
        self.image2=changecolor(pygame.transform.scale(pygame.image.
        load(image).convert_alpha(),(width,height)), 1.2,1.2,1.2)
        self.rect=pygame.Rect(x,y,width,height)
        self.clicked=20
    def draw(self,camera):
        mouse_pos=pygame.mouse.get_pos()
        self.rect.x=self.x-camera[0]
        self.rect.y=self.y-camera[1]
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.image2,self.rect)
        else:
            screen.blit(self.image,self.rect)
    def is_clicked(self):
        mouse_pos=pygame.mouse.get_pos()
        mouse_buttons=pygame.mouse.get_pressed()
        if (self.clicked>=20 and self.rect.collidepoint(mouse_pos) 
            and mouse_buttons[0]):
            self.clicked=0
            return self.rect.collidepoint(mouse_pos) and mouse_buttons[0] 
        else:
            self.clicked+=1
            return False


pygame.font.init()
FONTS = [pygame.font.Font(pygame.font.get_default_font(),
 font_size) for font_size in [48, 36, 24]]

NPCs=[]

class NPC(EntityLike,pygame.sprite.Sprite):
    def __init__(self,x,y,image,kind):
        self.x=x
        self.y=y
        self.image=pygame.image.load(image).convert_alpha()
        self.rect=self.image.get_rect()
        self.staus=0
        self.pic_diex=0
        self.kind=kind
    def draw(self,camera):
        self.pic_diex+=0.2
        NPC_blit=int(self.pic_diex%len(NPC_list[self.kind]))
        self.image=NPC_list[self.kind][NPC_blit]
        self.rect=self.image.get_rect()
        self.rect.x=self.x-camera[0]
        self.rect.y=self.y-camera[1]
        screen.blit(self.image,self.rect)
    def is_clicked(self):
        mouse_pos=pygame.mouse.get_pos()
        mouse_buttons=pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and mouse_buttons[0]:
            self.post(Event(Event_kind.TALK,{"object":self.kind}))

class Head(EntityLike,pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        self.image=image
        self.x=x
        self.y=y
    def draw(self,camera):
        screen.blit(self.image, pygame.
        Rect(self.x-camera[0],self.y-camera[1],50,50))
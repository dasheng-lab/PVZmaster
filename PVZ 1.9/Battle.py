import pygame
import random
import sys
import time
import copy
from Creature import *
from Event import *
from moneymanager import *
from Resources import *

class Card:
    def __init__(self):
        self.plant = [False, True, False, False, False]  # 1向日葵，3坚果，4窝瓜
        self.plant_cold = [0, 200, 0, 0, 0]
        self.image = self.dialog_surface = pygame.image.load("images/卡槽.png")
        self.rect = pygame.Rect(200, 0, 1000, 200)
        self.clicked = 0
        self.sunshine = 50
        self.active = 0
        self.suncount = 0
        self.gen_plant = False
        self.reasontime=0

    def draw(self):
        screen.blit(shovelbank, (645, 0))
        self.suncount += 1
        if self.suncount >= 500:
            self.suncount = 0
            self.sunshine += 25
        self.plant_cold[1] = min(self.plant_cold[1] + 1, 200)
        self.plant_cold[3] = min(self.plant_cold[3] + 1, 1500)
        self.plant_cold[4] = min(self.plant_cold[4] + 1, 2000)
        text1 = font1.render(f"{self.sunshine}", True, (0, 0, 0))
        screen.blit(self.image, self.rect)
        screen.blit(text1, (210, 65))
        if self.plant[1]:
            if self.plant_cold[1] >= 200 and self.sunshine >= 50:
                screen.blit(sunflower_image, (280, 0, 55, 80))
            else:
                screen.blit(sunflower2_image, (280, 0, 55, 80))
        if self.plant[3]:
            if self.plant_cold[3] >= 1500 and self.sunshine >= 50:
                screen.blit(nut_image, (335, 0, 55, 80))
            else:
                screen.blit(nut2_image, (335, 0, 55, 80))
        if self.plant[4]:
            if self.plant_cold[4] >= 2000 and self.sunshine >= 50: 
                screen.blit(melon_image, (390, 0, 55, 80))
            else:
                screen.blit(melon2_image, (390, 0, 55, 80))
        if self.active != 0:
            screen.blit(
                cold_dict[f"{self.active}"][0],
                (place_dict[f"{self.active}"], 0, 55, 80),
            )
        if the_level.win_count <= the_level.level * 2 + 4:
            screen.blit(jindut0, (800, 660))
        if (
            the_level.win_count > the_level.level * 2 + 4
            and the_level.win_count <= the_level.level * 3 + 10
        ):
            screen.blit(jindut1, (800, 660))
        if the_level.win_count > the_level.level * 3 + 10:
            screen.blit(jindut2, (800, 660))

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if self.active == 0:
            if (
                self.plant[1]
                and self.clicked >= 20
                and pygame.Rect(280, 0, 55, 80).collidepoint(mouse_pos)
                and mouse_buttons[0]
                and self.sunshine >= 50
                and self.plant_cold[1] >= 200
            ):
                self.active = 1
                self.clicked = 0
            if (
                self.plant[3]
                and self.clicked >= 20
                and pygame.Rect(335, 0, 55, 80).collidepoint(mouse_pos)
                and mouse_buttons[0]
                and self.sunshine >= 50
                and self.plant_cold[3] >= 1500
            ):
                self.active = 3
                self.clicked = 0
            if (
                self.plant[4]
                and self.clicked >= 20
                and pygame.Rect(390, 0, 55, 80).collidepoint(mouse_pos)
                and mouse_buttons[0]
                and self.sunshine >= 50
                and self.plant_cold[4] >= 2000 #change
            ):
                self.active = 4
                self.clicked = 0
            else:
                self.clicked += 1
            if add_hp.is_clicked():
                if player.hp < player.besthp:
                    if self.sunshine >= (player.besthp - player.hp) :
                        self.sunshine -= (player.besthp - player.hp) 
                        player.hp = player.besthp
                    else:
                        player.hp += self.sunshine 
                        self.sunshine = 0
        if self.active != 0:
            if (
                self.plant[1]
                and self.clicked >= 20
                and pygame.Rect(280, 0, 55, 80).collidepoint(mouse_pos)
                and mouse_buttons[0]
                and self.sunshine >= 50
                and self.plant_cold[1] >= 200
            ):
                self.active = 0
                self.clicked = 0
            if (
                self.plant[3]
                and self.clicked >= 20
                and pygame.Rect(335, 0, 55, 80).collidepoint(mouse_pos)
                and mouse_buttons[0]
                and self.sunshine >= 50
                and self.plant_cold[3] >= 1500
            ):
                self.active = 0
                self.clicked = 0
            if (
                self.plant[4]
                and self.clicked >= 20
                and pygame.Rect(390, 0, 55, 80).collidepoint(mouse_pos)
                and mouse_buttons[0]
                and self.sunshine >= 50
                and self.plant_cold[4] >= 2000 #change
            ):
                self.active = 0
                self.clicked = 0
            else:
                self.clicked += 1

    def grow(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        self.gen_plant=False
        global plant_list
        if mouse_buttons[0] and self.reasontime%10==0:
            self.reasontime+=1
            for lawn in lawn_dict.keys():
                if lawn_dict[lawn].rect.collidepoint(mouse_pos) :
                    if self.active == 1:
                        if lawn_avaible[lawn]:
                            self.sunshine -= 50
                            self.plant_cold[1] = 0
                            self.active = 0
                            plant_list.append(
                                Sunflower(lawn_dict[lawn].x, lawn_dict[lawn].y)
                            )
                            self.gen_plant=True
                            lawn_avaible[lawn] = False
                        else:
                            self.active = 0
                    if self.active == 3:
                        if lawn_avaible[lawn]:
                            self.sunshine -= 50
                            self.plant_cold[3] = 0
                            self.active = 0
                            plant_list.append(Nut(lawn_dict[lawn].x, lawn_dict[lawn].y))
                            self.gen_plant=True
                            lawn_avaible[lawn] = False
                        else:
                            self.active = 0
                    if self.active == 4:
                        if lawn_avaible[lawn]:
                            self.sunshine -= 50
                            self.plant_cold[4] = 0
                            self.active = 0
                            plant_list.append(Melon(lawn_dict[lawn].x, lawn_dict[lawn].y))
                            self.gen_plant=True
                            lawn_avaible[lawn] = False
                        else:
                            self.active = 0
            if not self.gen_plant and self.active!=0 and not pygame.Rect(200, 0, 1000, 100).collidepoint(mouse_pos):
                self.active = 0
        if self.reasontime%10!=0:
            self.reasontime+=1    


card_box = Card()

class Shovel:
    def __init__(self):
        self.image = pygame.image.load("images/铲子.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.image2=changecolor(self.image,1.2,1.2,1.2)
        self.rect = self.image.get_rect()
        self.rect.x = 645
        self.rect.y = 0
        self.active = False
        self.clicked=20

    def draw(self):
        global plant_list
        mouse_pos = pygame.mouse.get_pos()
        if not self.active :
            self.rect.x=645
            self.rect.y=0
            if self.rect.collidepoint(mouse_pos):
                screen.blit(self.image2, (self.rect.x, self.rect.y))
            else:
                screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.active :
            screen.blit(self.image, pygame.Rect(mouse_pos[0]-45, mouse_pos[1]-45, 80, 80))
            self.rect.x=mouse_pos[0]-45
            self.rect.y=mouse_pos[1]-45
            for plantx in plant_list:
                if plantx.rect.collidepoint(mouse_pos):
                    plantx.blight=1

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if (
            self.clicked >= 20
            and self.rect.collidepoint(mouse_pos)
            and mouse_buttons[0]
        ):
            self.clicked = 0
            return self.rect.collidepoint(mouse_pos) and mouse_buttons[0]
        else:
            self.clicked += 1
            return False

shovel=Shovel()

class Sunflower:
    def __init__(self, x, y):
        self.hp = 300
        self.x = x
        self.y = y
        self.pic_diex = 0
        self.kind = 0
        self.funccount = 0
        self.stacount = 0
        self.blight = 0

    def draw(self, camera,style=0):
        if style!=11 and style!=12:
            self.pic_diex += 0.2
        plant_blit = int(self.pic_diex % len(NPC_list[1]))
        self.image = NPC_list[1][plant_blit]
        self.rect = self.image.get_rect()
        self.rect.x = self.x - camera[0] + 20
        self.rect.y = self.y - camera[1] + 10
        if style!=12:
            if self.blight == 0:
                screen.blit(
                    self.image,
                    pygame.Rect(
                        self.rect.x,
                        self.rect.y - (self.rect.width - 65),
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            elif self.blight <= 10:
                self.blight += 1
                story = copy.copy(self.image)
                screen.blit(
                    changecolor(story, 1.5, 1.5, 1.5),
                    pygame.Rect(
                        self.rect.x,
                        self.rect.y - (self.rect.width - 65),
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            elif self.blight <= 40:
                self.blight +=1
                screen.blit(
                    self.image,
                    pygame.Rect(
                        self.rect.x,
                        self.rect.y - (self.rect.width - 65),
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            else:
                self.blight = 0
                screen.blit(
                self.image,
                pygame.Rect(
                    self.rect.x,
                    self.rect.y - (self.rect.width - 65),
                    self.rect.width,
                    self.rect.height,
                ),
            )
        else:
            story=copy.copy(self.image)
            screen.blit(
                changecolor(story, 0.6, 0.6, 0.6),
                pygame.Rect(
                    self.rect.x,
                    self.rect.y - (self.rect.width - 65),
                    self.rect.width,
                    self.rect.height,
                ),
            )
        if self.kind == 1:
            self.pic_diex += 0.2
            plant_blit = int(self.pic_diex % len(sunflowerfunc_frame))
            self.image = sunflowerfunc_frame[plant_blit]
            self.rect = self.image.get_rect()
            self.rect.x = self.x - camera[0] + 20
            self.rect.y = self.y - camera[1] + 10
            screen.blit(self.image, self.rect)

    def func(self, camera):
        if not the_level.triumph:
            self.funccount += 1
            if self.funccount >= 500:
                card_box.sunshine += 25
                self.funccount = 0
                self.kind = 1
            if self.kind == 1:
                self.stacount += 1
            if self.stacount >= 30:
                self.stacount = 0
                self.kind = 0

    def is_eaten(self, camera):
        for zombie in emg.zombie_list:
            if (pygame.Rect(self.rect.x,self.rect.y - (self.rect.width - 65),self.rect.width,self.rect.height).colliderect(pygame.Rect(zombie.rect.x - camera[0] + 10,zombie.rect.y - camera[1] + 20,zombie.rect.width / 3,zombie.rect.height / 3)) and zombie.style!= 8 and zombie.style!= 9):
               zombie.collide=True
            if zombie.tag==1:
                if (pygame.Rect(self.rect.x+20,self.rect.y - (self.rect.width - 65)+20,self.rect.width /3,self.rect.height/3).colliderect(pygame.Rect(zombie.rect.x - camera[0] + 15,zombie.rect.y - camera[1] + 40,zombie.rect.width / 3,zombie.rect.height / 3)) and zombie.style != 8 and zombie.style != 9 and zombie.HP > 70):
                    zombie.style = 10
                    zombie.eating=True
                    self.hp -= 3
                    self.blight += 1
                else:
                    zombie.eating=False
            elif zombie.tag==2 or zombie.tag==3:
                if (pygame.Rect(self.rect.x+20,self.rect.y - (self.rect.width - 65)+20,self.rect.width /3,self.rect.height/3).colliderect(pygame.Rect(zombie.rect.x - camera[0] + 15,zombie.rect.y - camera[1] + 50,zombie.rect.width / 3,zombie.rect.height / 3)) and zombie.style!= 8 and zombie.style!= 9):
                    zombie.style = 10
                    zombie.eating=True
                    self.hp -= 3
                    self.blight += 1
                else:
                    zombie.eating=False
        if self.hp <= 0:
            plant_list.remove(self)
            for lawn in lawn_dict.keys():
                if lawn_dict[lawn].x == self.x and lawn_dict[lawn].y == self.y:
                    lawn_avaible[lawn] = True
class Nut:
    def __init__(self, x, y):
        self.hp = 4000
        self.x = x
        self.y = y
        self.pic_diex = 0
        self.kind = 3
        self.blight = 0
        self.status = 0

    def draw(self, camera,style=0):
        if style!=11 and style!=12:
            self.pic_diex += 0.2
        plant_blit = int(self.pic_diex % len(nut_set[self.status]))
        self.image = nut_set[self.status][plant_blit]
        self.rect = self.image.get_rect()
        self.rect.x = self.x - camera[0] + 20
        self.rect.y = self.y - camera[1] + 10
        if style!=12:
            if self.blight == 0:
                screen.blit(
                    self.image,
                    pygame.Rect(
                        self.rect.x,
                        self.rect.y - (self.rect.width - 65),
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            elif self.blight <= 10:
                self.blight += 1
                story = copy.copy(self.image)
                screen.blit(
                    changecolor(story, 1.5, 1.5, 1.5),
                    pygame.Rect(
                        self.rect.x,
                        self.rect.y - (self.rect.width - 65),
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            elif self.blight <= 40:
                self.blight +=1
                screen.blit(
                    self.image,
                    pygame.Rect(
                        self.rect.x,
                        self.rect.y - (self.rect.width - 65),
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            else:
                self.blight = 0
                screen.blit(
                    self.image,
                    pygame.Rect(
                        self.rect.x,
                        self.rect.y - (self.rect.width - 65),
                        self.rect.width,
                        self.rect.height,
                    ),
                )
        else:
            story=copy.copy(self.image)
            screen.blit(
                changecolor(story, 0.6, 0.6, 0.6),
                pygame.Rect(
                    self.rect.x,
                    self.rect.y - (self.rect.width - 65),
                    self.rect.width,
                    self.rect.height,
                ),
            )
    def func(self, camera):
        if self.hp <= 2600 and self.hp >= 1300:
            self.status = 1
        if self.hp < 1300:
            self.status = 2

    def is_eaten(self, camera):
        for zombie in emg.zombie_list:
            if (pygame.Rect(self.rect.x,self.rect.y - (self.rect.width - 65),self.rect.width,self.rect.height).colliderect(pygame.Rect(zombie.rect.x - camera[0] + 10,zombie.rect.y - camera[1] + 20,zombie.rect.width / 3,zombie.rect.height / 3)) and zombie.style!= 8 and zombie.style!= 9):
               zombie.collide=True
            if zombie.tag==1:
                if (pygame.Rect(self.rect.x+20,self.rect.y - (self.rect.width - 65)+20,self.rect.width /3,self.rect.height/3).colliderect(pygame.Rect(zombie.rect.x - camera[0] + 15,zombie.rect.y - camera[1] + 40,zombie.rect.width / 3,zombie.rect.height / 3)) and zombie.style != 8 and zombie.style != 9 and zombie.HP > 70):
                    zombie.style = 10
                    zombie.eating=True
                    self.hp -= 3
                    self.blight += 1
                else:
                    zombie.eating=False
            elif zombie.tag==2 or zombie.tag==3:
                if (pygame.Rect(self.rect.x+20,self.rect.y - (self.rect.width - 65)+20,self.rect.width /3,self.rect.height/3).colliderect(pygame.Rect(zombie.rect.x - camera[0] + 15,zombie.rect.y - camera[1] + 50,zombie.rect.width / 3,zombie.rect.height / 3)) and zombie.style!= 8 and zombie.style!= 9):
                    zombie.style = 10
                    zombie.eating=True
                    self.hp -= 3
                    self.blight += 1
                else:
                    zombie.eating=False
        if self.hp <= 0:
            plant_list.remove(self)
            for lawn in lawn_dict.keys():
                if lawn_dict[lawn].x == self.x and lawn_dict[lawn].y == self.y:
                    lawn_avaible[lawn] = True
class Melon:
    def __init__(self, x, y):
        self.hp = 300
        self.x = x
        self.y = y
        self.pic_diex = 0
        self.pic_diex1 = 0
        self.kind = 4
        self.blight = 0
        self.countfunc = 0
        self.countfunc1F5=0
        self.countfunc2=0
        self.funx = 0
        self.emglist=[]
    def draw(self, camera,style=0):
        if self.funx == 1:
            if style!=11 and style!=12:
                if self.countfunc2<10:
                    self.pic_diex += 0.4
                    plant_blit = int(self.pic_diex % len(NPC_list[self.kind]))
                    self.image = NPC_list[self.kind][plant_blit]
                    self.rect = self.image.get_rect()
                    self.rect.x = self.x - camera[0] + 20+dx/10*self.countfunc2
                    self.rect.y = self.y - camera[1] + 10-dy/15*self.countfunc2
                    screen.blit(
                        self.image,
                        pygame.Rect(
                            self.rect.x,
                            self.rect.y - (self.rect.width - 65),
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                    self.countfunc2+=1
                else:
                    if self.countfunc1F5<20:
                        self.pic_diex += 0.5
                        self.image = NPC_list[self.kind][0]
                        self.rect = self.image.get_rect()
                        self.rect.x = self.x - camera[0] + 20+dx
                        self.rect.y = self.y - camera[1] + 10-100
                        screen.blit(
                            self.image,
                            pygame.Rect(
                                self.rect.x,
                                self.rect.y - (self.rect.width - 65),
                                self.rect.width,
                                self.rect.height,
                            ),
                        )
                        self.countfunc1F5+=1
                    else:
                        if self.countfunc <= 9:
                            self.pic_diex1 += 0.5
                            plant_blit1 = int(self.pic_diex1 % len(melonjump_frame))
                            self.image = melonjump_frame[plant_blit1]
                            screen.blit(
                                self.image,
                                pygame.Rect(
                                    self.rect.x+10,
                                    self.rect.y - (self.rect.width - 65) + self.pic_diex1*25,
                                    self.rect.width,
                                    self.rect.height,
                                ),
                            )
                            self.countfunc += 1
                        else:
                            self.countfunc = 0
                            for zombiee in self.emglist:
                                zombiee.style=9
                                emg.zombie_list.remove(zombiee)
                            plant_list.remove(self)
                            for lawn in lawn_dict.keys():
                                if lawn_dict[lawn].x == self.x and lawn_dict[lawn].y == self.y:
                                    lawn_avaible[lawn] = True
        else:
            if style!=11 or style!=12:
                self.pic_diex += 0.2
            plant_blit = int(self.pic_diex % len(NPC_list[self.kind]))
            self.image = NPC_list[self.kind][plant_blit]
            self.rect = self.image.get_rect()
            self.rect.x = self.x - camera[0] + 20
            self.rect.y = self.y - camera[1] + 10
            if style!=12:
                if self.blight == 0:
                    screen.blit(
                        self.image,
                        pygame.Rect(
                            self.rect.x,
                            self.rect.y - (self.rect.width - 65),
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                elif self.blight <= 10:
                    self.blight += 1
                    story = copy.copy(self.image)
                    screen.blit(
                        changecolor(story, 1.5, 1.5, 1.5),
                        pygame.Rect(
                            self.rect.x,
                            self.rect.y - (self.rect.width - 65),
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                elif self.blight <= 40:
                    self.blight +=1
                    screen.blit(
                        self.image,
                        pygame.Rect(
                            self.rect.x,
                            self.rect.y - (self.rect.width - 65),
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                else:
                    self.blight = 0
                    screen.blit(
                        self.image,
                        pygame.Rect(
                            self.rect.x,
                            self.rect.y - (self.rect.width - 65),
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
            else:
                story=copy.copy(self.image)
                screen.blit(
                    changecolor(story, 0.6, 0.6, 0.6),
                    pygame.Rect(
                        self.rect.x,
                        self.rect.y - (self.rect.width - 65),
                        self.rect.width,
                        self.rect.height,
                    ),
                )

    def func(self, camera):
        if self.funx == 0:
            for zombie in emg.zombie_list:
                if (
                    pygame.Rect(
                        self.rect.x,
                        self.rect.y - (self.rect.width - 65),
                        self.rect.width,
                        self.rect.height,
                    ).colliderect(
                        pygame.Rect(
                            zombie.rect.x - camera[0] - 40,
                            zombie.rect.y - camera[1] + 20,
                            zombie.rect.width * 3,
                            zombie.rect.height / 3,
                        )
                    )
                    and zombie.style != 8
                    and zombie.style != 9
                    and zombie.HP > 70
                ):
                    self.funx = 1
                    self.emglist.append(zombie)
                    global dx,dy,zmobiee
                    zmobiee=zombie
                    dx=zmobiee.rect.x - self.rect.x-camera[0]
                    dy=150

    def is_eaten(self, camera):
        if self.funx == 0:
            for zombie in emg.zombie_list:
                if (pygame.Rect(self.rect.x,self.rect.y - (self.rect.width - 65),self.rect.width,self.rect.height).colliderect(pygame.Rect(zombie.rect.x - camera[0] + 10,zombie.rect.y - camera[1] + 20,zombie.rect.width / 3,zombie.rect.height / 3)) and zombie.style!= 8 and zombie.style!= 9):
                    zombie.collide=True
                if zombie.tag==1:
                    if (pygame.Rect(self.rect.x+20,self.rect.y - (self.rect.width - 65)+20,self.rect.width /3,self.rect.height/3).colliderect(pygame.Rect(zombie.rect.x - camera[0] + 15,zombie.rect.y - camera[1] + 40,zombie.rect.width / 3,zombie.rect.height / 3)) and zombie.style != 8 and zombie.style != 9 and zombie.HP > 70):
                        zombie.style = 10
                        zombie.eating=True
                        self.hp -= 3
                        self.blight += 1
                    else:
                        zombie.eating=False
                elif zombie.tag==2:
                    if (pygame.Rect(self.rect.x+20,self.rect.y - (self.rect.width - 65)+20,self.rect.width /3,self.rect.height/3).colliderect(pygame.Rect(zombie.rect.x - camera[0] + 15,zombie.rect.y - camera[1] + 50,zombie.rect.width / 3,zombie.rect.height / 3)) and zombie.style!= 8 and zombie.style!= 9):
                        zombie.style = 10
                        zombie.eating=True
                        self.hp -= 3
                        self.blight += 1
                    else:
                        zombie.eating=False
            if self.hp <= 0:
                plant_list.remove(self)
                for lawn in lawn_dict.keys():
                    if lawn_dict[lawn].x == self.x and lawn_dict[lawn].y == self.y:
                        lawn_avaible[lawn] = True
class Level(Listener):
    def __init__(self):
        self.level = 1
        self.count = 0
        self.win_count = 0
        self.hp = 0
        self.triumph = False
        self.is_draw = False
        self.startdealing = 0
        self.finaldealing=0
    def reset(self):
        self.startdealing =0

# self.win_count <= self.level * 5 + 10
    def level_start(self):
        if self.startdealing <= 670:
            self.startdealing += 1
            if self.startdealing==670:
                pass  #这里放第一个僵尸来的音效
        if self.startdealing >670:
            if self.level==1:
                if (self.count > 500 or emg.zombie_list==[]) and self.win_count <8:
                    self.count = 0
                    emg.AIput(player.rect.x, player.rect.y,1)
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <13:
                    self.count = 0
                    emg.AIput(player.rect.x, player.rect.y,1)
                    emg.AIput(player.rect.x, player.rect.y,1)
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <15:
                    self.count = 0
                    emg.AIput(player.rect.x, player.rect.y,1)
                    emg.AIput(player.rect.x, player.rect.y,1)
                    emg.AIput(player.rect.x, player.rect.y,1)
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count==15:
                    self.count = 0
                    emg.AIput(player.rect.x, player.rect.y,2)
                    emg.AIput(player.rect.x, player.rect.y,1)
                    emg.AIput(player.rect.x, player.rect.y,1)
                    emg.AIput(player.rect.x, player.rect.y,1)
                    self.win_count += 1
                    self.finaldealing=1
                else:
                    self.count += 1
            elif self.level==2:
                if (self.count > 500 or emg.zombie_list==[]) and self.win_count <4:
                    self.count = 0
                    emg.AIput(player.rect.x, player.rect.y,1)
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <10:
                    self.count = 0
                    emg.AIput(player.rect.x, player.rect.y,1)
                    emg.AIput(player.rect.x, player.rect.y,1)
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <15:
                    self.count = 0
                    emg.AIput(player.rect.x, player.rect.y,1)
                    emg.AIput(player.rect.x, player.rect.y,1)
                    emg.AIput(player.rect.x, player.rect.y,1)
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <18:
                    sum=0
                    while sum<3: 
                        add=random.randint(1,2)
                        emg.AIput(player.rect.x, player.rect.y,add)  
                        sum+=add
                    self.count = 0
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <20:
                    sum=0
                    while sum<4:
                        add=random.randint(1,2)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.count = 0
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count==20:
                    sum=0
                    while sum<7:
                        add=random.randint(1,2)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.count = 0
                    self.win_count += 1
                    self.finaldealing=1
                else:
                    self.count += 1
            elif self.level==3:
                if (self.count > 500 or emg.zombie_list==[]) and self.win_count <3:
                    self.count = 0
                    emg.AIput(player.rect.x, player.rect.y,1)
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <6:
                    self.count = 0
                    emg.AIput(player.rect.x, player.rect.y,1)
                    emg.AIput(player.rect.x, player.rect.y,1)
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <9:
                    self.count = 0
                    sum=0
                    while sum<3:
                        add=random.randint(1,2)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <12:
                    self.count = 0
                    sum=0
                    while sum<5:
                        add=random.randint(1,2)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <16:
                    self.count = 0
                    sum=0
                    while sum<7:
                        add=random.randint(1,2)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <21:
                    self.count = 0
                    sum=0
                    while sum<9:
                        add=random.randint(1,3)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count<25:
                    self.count = 0
                    sum=0
                    while sum<11:
                        add=random.randint(1,3)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count==25:
                    self.count = 0
                    sum=0
                    while sum<15:
                        add=random.randint(1,3)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.win_count += 1
                    self.finaldealing=1
                else:
                    self.count += 1
            elif self.level==4:
                if (self.count > 500 or emg.zombie_list==[]) and self.win_count <3:
                    self.count = 0
                    emg.AIput(player.rect.x, player.rect.y,1)
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <7:
                    self.count = 0
                    sum=0
                    while sum<2:
                        add=random.randint(1,2)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <12:
                    self.count = 0
                    sum=0
                    while sum<4:
                        add=random.randint(1,3)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <15:
                    self.count = 0
                    sum=0
                    while sum<5:
                        add=random.randint(1,3)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <20:
                    self.count = 0
                    sum=0
                    while sum<7:
                        add=random.randint(1,3)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count <24:
                    self.count = 0
                    sum=0
                    while sum<9:
                        add=random.randint(1,4)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count<27:
                    self.count = 0
                    sum=0
                    while sum<12:
                        add=random.randint(1,4)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count<30:
                    self.count = 0
                    sum=0
                    while sum<15:
                        add=random.randint(1,4)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.win_count += 1
                elif (self.count > 500 or emg.zombie_list==[]) and self.win_count==30:
                    self.count = 0
                    sum=0
                    while sum<20:
                        add=random.randint(1,4)
                        emg.AIput(player.rect.x, player.rect.y,add)
                        sum+=add
                    self.win_count += 1
                    self.finaldealing=1
                else:
                    self.count += 1
            elif self.level==5:
                pass
            elif self.level==6:
                pass

        if self.finaldealing>=1 and self.finaldealing<=130:
            finalwave=pygame.image.load("images/FinalWave.png").convert_alpha()
            if self.finaldealing==1:
                pass  #这里放最后一波僵尸来的音效
            self.finaldealing+=1
            if self.finaldealing<=20:
                finalwave=pygame.transform.scale(finalwave,(800-25*self.finaldealing,180-5.5*self.finaldealing))
                screen.blit(finalwave,(100+12.5*self.finaldealing,260+3*self.finaldealing))
            else:
                screen.blit(finalwave,(340,315))
        if self.finaldealing>130:
            self.finaldealing=0
        if self.win_count > self.level * 5 + 10:
            for zombie in emg.zombie_list:
                if zombie.HP >= 0:
                    self.hp += zombie.HP
            if self.hp <= 0:
                moneybox.draw()
                self.is_draw = True
                self.triumph=True
            else:
                self.hp = 0
        if moneybox.is_clicked() and self.is_draw:
            self.win_count = 0
            self.level += 1
            self.triumph=False
            self.is_draw=False
            global lawn_avaible
            for lawn in lawn_avaible.keys():
                lawn_avaible[lawn] = True
            player_money.add_money(100 + 20 * self.level + int(0.2 * card_box.sunshine))
            self.post(
                Event(
                    Event_kind.CHANGE_BAKEGROUND, {"background": 2, "x": -2600, "y": 0}))
        if self.level >= 6:
            self.post(Event(Event_kind.GAMEOVER))

the_level = Level()
card_box = Card()
'''
while sum<12:  #3是总兵力
    add=random.randint(1,3)
    if add==2:   #可能有多个僵尸占同一个兵力
        subadd=random.randint(1,2)
    emg.AIput(player.rect.x, player.rect.y,add,subadd)  #比如subadd=1是路障，subadd=2是舞王
    sum+=add
'''
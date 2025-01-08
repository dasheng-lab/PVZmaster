import pygame
import random
import sys
import time
import copy
from Event import *
from Obstacle import *
from Openai import *
from pautton import *
from moneymanager import *
from Resources import *
class Player(EntityLike, pygame.sprite.Sprite):
    def __init__(self, x=200, y=200):
        self.image = pygame.image.load("images/shootermove/图层 1.png").convert_alpha()
        self.blood_image = pygame.image.load("images/血量.png").convert_alpha()
        self.blood_image = pygame.transform.scale(self.blood_image, (150, 90))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.pic_diex = 0
        self.hp = 1000
        self.besthp = 1000
        self.blight = 0
        self.place = 0
        self.beat = 20
        self.shoot_speed = 50
        self.pause = False
        self.n=0
        self.reasontime=0
        self.dealing=0
    def listen(self,event: Event):  # 玩家类所响应的事件
        if event.code == pygame.KEYDOWN:  # 键盘按下事件
            self.keydown()
        if event.code == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.code == Event_kind.CAN_MOVE:  # 响应场景发出的允许移动事件
            self.rect.x = event.body["POS"][0]
            self.rect.y = event.body["POS"][1]
        super().listen(event)  # 继承原有的响应事件内容，如对DRAW的响应

    def keydown(self):  # 键盘按下事件的响应
        keys = pygame.key.get_pressed()
        pausemanager.detect()
        self.pause=pausemanager.pause
        if not self.pause:
            stay0__1obstacle = obstacl_class[self.place][0].collide(self, 0, -1)
            stay0_1obstacle = obstacl_class[self.place][0].collide(self, 0, 1)
            stay1__0obstacle = obstacl_class[self.place][0].collide(self, -1, 0)
            stay1_0obstacle = obstacl_class[self.place][0].collide(self, 1, 0)
            for obstale in obstacl_class[self.place][1 : len(obstacl_class[self.place])]:
                stay0__1obstacle *= obstale.collide(self, 0, -1)
                stay0_1obstacle *= obstale.collide(self, 0, 1)
                stay1__0obstacle *= obstale.collide(self, -1, 0)
                stay1_0obstacle *= obstale.collide(self, 1, 0)
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and stay0__1obstacle == 1:
                self.rect.y -= self.speed
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and stay0_1obstacle == 1:
                self.rect.y += self.speed
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and stay1__0obstacle == 1:
                self.rect.x -= self.speed
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and stay1_0obstacle == 1:
                self.rect.x += self.speed
            if keys[pygame.K_SPACE]:
                global shooter_count
                shooter_count = min(shooter_count + 1, self.shoot_speed)
                if shooter_count == self.shoot_speed:
                    if self.rect.x > -1000:
                        bulletlist_right.add(Bullet(self))
                    else:
                        bulletlist_left.add(Bullet(self))
                    shooter_count = 0
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_1]:
            text0 = f"攻击力：{self.beat:.1f},射速：{self.shoot_speed:.3f},最大生命值：{self.besthp},移速：{self.speed:.2f}"
            self.post(Event(Event_kind.WORDS, {"text": text0}))

    def draw(self, camera, style):
        if style!=11 and style!=12:
            self.pic_diex += 0.2
        player_blit = int(self.pic_diex % len(player_frame))
        player_image = player_frame[player_blit]
        player_rect = player_image.get_rect()
        if style == 2 or style == 6:
            if camera[0] + 500 - self.rect.x > camera_lack and camera[0] > -2600:
                camera[0] = self.rect.x - 500 + camera_lack
            if -camera[0] - 500 + self.rect.x > camera_lack and camera[0] < 400:
                camera[0] = self.rect.x - 500 - camera_lack
            if self.rect.x <= -1000:
                player_image = pygame.transform.flip(player_image, True, False)
        elif style == 7 :
            if camera[0] + 500 - self.rect.x > camera_lack and camera[0] > -1000:
                camera[0] = self.rect.x - 500 + camera_lack
            if -camera[0] - 500 + self.rect.x > camera_lack and camera[0] < 0:
                camera[0] = self.rect.x - 500 - camera_lack
            if camera[1] + 350 - self.rect.y > camera_lack and camera[1] > 0:
                camera[1] = self.rect.y - 350 + camera_lack
            if -camera[1] - 300 + self.rect.y > camera_lack and camera[1] < 600:
                camera[1] = self.rect.y - 300 - camera_lack
        elif style==12:
            story = copy.copy(player_image)
            screen.blit(
                changecolor(story, 0.6, 0.6, 0.6),
                pygame.Rect(self.rect.x - camera[0],self.rect.y - camera[1] - (player_rect.width - 65),
                    player_rect.width,player_rect.height))
        self.be_eaten(camera)
        if style!=12:
            if self.blight == 0 :
                screen.blit(
                    player_image,
                    pygame.Rect(
                        self.rect.x - camera[0],
                        self.rect.y - camera[1] - (player_rect.width - 65),
                        player_rect.width,
                        player_rect.height,
                    ),
                )
            elif self.blight <= 3 :
                self.blight += 1
                story = copy.copy(player_image)
                screen.blit(
                    changecolor(story, 1.5, 1.5, 1.5),
                    pygame.Rect(
                        self.rect.x - camera[0],
                        self.rect.y - camera[1] - (player_rect.width - 65),
                        player_rect.width,
                        player_rect.height,
                    ),
                )
            else:
                self.blight = 0
                screen.blit(
                    player_image,
                    pygame.Rect(
                        self.rect.x - camera[0],
                        self.rect.y - camera[1] - (player_rect.width - 65),
                        player_rect.width,
                        player_rect.height,
                ),
            )
        #self.rect.x=self.rect.x-camera[0]
        #self.rect.y=self.rect.y-camera[1]-(player_rect.width-65)
        screen.blit(self.blood_image, (0, -20))
        text1 = font2.render(f"{self.hp}", True, (0, 0, 0))
        screen.blit(text1, (50, 16))

    def be_eaten(self, camera):
        for zombie in emg.zombie_list:
            if (
                pygame.Rect(
                    self.rect.x - camera[0],
                    self.rect.y - camera[1] - (self.rect.width - 65),
                    self.rect.width,
                    self.rect.height,
                ).colliderect(
                    pygame.Rect(
                        zombie.rect.x - camera[0],
                        zombie.rect.y - camera[1],
                        zombie.rect.width,
                        zombie.rect.height,
                    )
                )
                and zombie.style != 8
                and zombie.style != 9
            ):
                zombie.collide=True
            else:
                zombie.collide=False
            if zombie.tag==1 and (
                pygame.Rect(
                    self.rect.x - camera[0],
                    self.rect.y - camera[1] - (self.rect.width - 65),
                    self.rect.width,
                    self.rect.height,
                ).colliderect(
                    pygame.Rect(
                        zombie.rect.x - camera[0],
                        zombie.rect.y - camera[1],
                        zombie.rect.width,
                        zombie.rect.height,
                    )
                )
                and zombie.style != 8
                and zombie.style != 9
                and zombie.HP > 70
            ):
                zombie.style = 10
                zombie.eating=True
                self.hp -= 3
                self.blight = 1
                if self.hp <= 0:
                    self.hp = 1000
                    self.post(Event(Event_kind.EATEN, {"objecct": player}))
            else:
                zombie.eating=False
            if (zombie.tag==2 or zombie.tag==3) and (
                pygame.Rect(
                    self.rect.x - camera[0],
                    self.rect.y - camera[1] - (self.rect.width - 65),
                    self.rect.width,
                    self.rect.height,
                ).colliderect(
                    pygame.Rect(
                        zombie.rect.x - camera[0],
                        zombie.rect.y - camera[1],
                        zombie.rect.width,
                        zombie.rect.height,
                    )
                )
                and zombie.style!= 8
                and zombie.style!= 9
            ):
                zombie.style = 10
                zombie.eating=True
                self.hp -= 3
                self.blight = 1
                if self.hp <= 0:
                    self.hp = 1000
                    self.post(Event(Event_kind.EATEN, {"objecct": player}))
            else:
                zombie.eating=False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, shooter):
        super().__init__()
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (22, 22))
        self.rect = self.image.get_rect()
        self.rect.x = shooter.rect.x + 35
        self.rect.y = shooter.rect.y + 5.5
        self.speed = 8
        self.pic_diex = 0

    def draw(self, camera,style=0):
        if style!=12:
            screen.blit(self.image,pygame.Rect(
                self.rect.x - camera[0],self.rect.y - camera[1],self.rect.width,self.rect.height))
        else:
            story=copy.copy(self.image)
            screen.blit(changecolor(story, 0.6, 0.6, 0.6),pygame.Rect(
                self.rect.x - camera[0],self.rect.y - camera[1],self.rect.width,self.rect.height))


    def move(self):
        # 7 在屏幕范围内，实现往右移动
        if -1200 < self.rect.x < 1200:
            self.rect.x += self.speed
        elif self.rect.x >= 1200:  # 8 子弹飞出屏幕，从精灵组删除
            self.kill()
        elif -2600 < self.rect.x <= -1200:
            self.rect.x -= self.speed
        else:
            self.kill()

    def crash_zombie(self):
        for zombie in emg.zombie_list:
            if (
                self.rect.colliderect(zombie.rect)
                and zombie.style != 8
                and zombie.style != 9
            ):
                zombie.HP -= player.beat
                zombie.style = 3
                zombie.hit = True
                self.kill()
                if self in bulletlist_left:
                    bulletlist_left.remove(self)
                else:
                    bulletlist_right.remove(self)
pygame.font.init()
FONTS = [pygame.font.Font(pygame.font.get_default_font(), font_size) for font_size in [48, 36, 24]]
NPCs = []
class NPC(EntityLike, pygame.sprite.Sprite):
    def __init__(self, x, y, image, kind):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.staus = 0
        self.pic_diex = 0
        self.kind = kind

    def draw(self, camera):
        self.pic_diex += 0.2
        NPC_blit = int(self.pic_diex % len(NPC_list[self.kind]))
        self.image = NPC_list[self.kind][NPC_blit]
        self.rect = self.image.get_rect()
        self.rect.x = self.x - camera[0]
        self.rect.y = self.y - camera[1]
        screen.blit(self.image, self.rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and mouse_buttons[0]:
            self.post(Event(Event_kind.TALK, {"object": self.kind}))

class Fallthing(EntityLike, pygame.sprite.Sprite):
    def __init__(self, image, x, y,width,height):
        self.image = image
        self.x = x
        self.y = y
        self.width=width
        self.height=height

    def draw(self, camera):
        screen.blit(self.image, pygame.Rect(self.x - camera[0], self.y - camera[1], self.width, self.height))

class ZombieManager(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.zombie_list = []
        self.dealing = 0
        self.count = 0

    def gen_new_zombie(self, gen):
        # gen=random.choice([425,315,230,125,25])
        self.zombie_list.append(Zombie(1000, gen))
    def gen_new_roadblock_zombie(self, gen):
        self.zombie_list.append(Roadblock_Zombie(1000, gen))
    def gen_new_bucket_zombie(self, gen):
        self.zombie_list.append(Bucket_Zombie(1000, gen))

    def AIput(self, playerx, playery,force,subforce=1):
        staystr = AI_decision(playerx, playery)
        if force==1:  # 普通僵尸
            if "425" in staystr:
                self.gen_new_zombie(425)
            elif "315" in staystr:
                self.gen_new_zombie(315)
            elif "230" in staystr:
                self.gen_new_zombie(210)
            elif "125" in staystr:
                self.gen_new_zombie(125)
            elif "25" in staystr:
                self.gen_new_zombie(25)
            else:
                gen1 = random.choice([425, 315, 210, 125, 25])
                self.gen_new_zombie(gen1)
        elif force==2:  # 路障僵尸
            if "425" in staystr:
                self.gen_new_roadblock_zombie(425)
            elif "315" in staystr:
                self.gen_new_roadblock_zombie(315)
            elif "230" in staystr:
                self.gen_new_roadblock_zombie(210)
            elif "125" in staystr:
                self.gen_new_roadblock_zombie(125)
            elif "25" in staystr:
                self.gen_new_roadblock_zombie(25)
            else:
                gen2 = random.choice([425, 315, 210, 125, 25])
                self.gen_new_roadblock_zombie(gen2)
        elif force==3:  # 铁桶僵尸
            if "425" in staystr:
                self.gen_new_bucket_zombie(425)
            elif "315" in staystr:
                self.gen_new_bucket_zombie(315)
            elif "230" in staystr:
                self.gen_new_bucket_zombie(210)
            elif "125" in staystr:
                self.gen_new_bucket_zombie(125)
            elif "25" in staystr:
                self.gen_new_bucket_zombie(25)
            else:
                gen3 = random.choice([425, 315, 210, 125, 25])
                self.gen_new_bucket_zombie(gen3)
    def move(self):
        for js in self.zombie_list:
            js.move()

    def draw(self, camera):
        for jsd in self.zombie_list:
            jsd.draw(camera)


player = Player()
emg = ZombieManager()
plant_list = []

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.style = 0
        self.x = x
        self.y = y
        self.HP = 270
        self.move_speed = random.uniform(0.25,0.5)
        self.cjsindex = 0
        self.headindex = 0
        self.fallindex = 0
        self.eatindex = 0
        self.noheadeatindex = 0
        self.moneyindex=0
        self.image = pygame.image.load("images/commonjs/cjs1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.n = 0
        self.dealing = 0
        self.eating=False
        self.hit=False
        self.collide=False
        self.money=random.randint(0,100)
        self.tag=1
        self.force=1
    def draw(self, camera):
        if self.style == 0:  # 正常移动
            self.cjsindex += 0.1
            cjsblit = int(self.cjsindex % len(frame))
            self.rect.x = self.x
            self.rect.y = screen_height - (self.y + frame[cjsblit].get_height())
            screen.blit(
                frame[cjsblit],
                (
                    self.rect.x - camera[0],
                    self.rect.y - camera[1],
                    self.rect.width,
                    self.rect.height,
                ),
            )
        elif self.style == 3:  # 被子弹击中
            for plans in plant_list:
                if self.rect.colliderect(plans.rect):
                    self.collide=True
                    break
            if self.HP > 70 and not self.eating:
                self.cjsindex += 0.1
                cjsblit = int(self.cjsindex % len(frame))
                self.rect.x = self.x
                self.rect.y = screen_height - (self.y + frame[cjsblit].get_height())
                story = copy.copy(frame[cjsblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x - camera[0],
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 0
            
            elif self.HP <= 70 and self.HP > 0 and not self.collide:
                self.cjsindex += 0.1
                cjsblit = int(self.cjsindex % len(cjsdiewalk_frame))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + cjsdiewalk_frame[cjsblit].get_height()
                )
                story = copy.copy(cjsdiewalk_frame[cjsblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x - camera[0],
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 7
            
            elif self.HP > 70 and self.eating:
                self.eatindex += 0.1
                eatblit = int(self.eatindex % len(cjseat_frame))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + cjseat_frame[eatblit].get_height()
                )
                story=copy.copy(cjseat_frame[eatblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x - camera[0],
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 10

            elif self.HP <= 70 and self.HP > 0 and self.collide:
                self.noheadeatindex += 0.1
                noheadeatblit = int(self.noheadeatindex % len(cjsnoheadeat_frame))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + cjsnoheadeat_frame[noheadeatblit].get_height()
                )
                story=copy.copy(cjsnoheadeat_frame[noheadeatblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x - camera[0],
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 7
            elif self.HP <= 0:
                self.style = 8

        elif self.style == 4:  # 失败未进家
            self.rect.x = self.x
            self.rect.y = screen_height - (self.y + self.image.get_height())
            screen.blit(self.image, (self.rect.x - camera[0], self.rect.y - camera[1]))

        elif self.style == 5:  # 失败进家
            self.y = 200
            self.rect.x = self.x
            self.cjsindex += 0.1
            cjsblit = int(self.cjsindex % len(frame))
            self.y = screen_height - (self.y + frame[cjsblit].get_height())
            screen.blit(frame[cjsblit], (self.x - camera[0], self.y - camera[1]))
            zombie_rect = fm_cjs.get_rect()
            zombie_rect.x = self.x
            zombie_rect.y = self.y
            self.image = frame[cjsblit]
        elif self.style == 6:  # 失败未进家但吃完脑子
            if self.dealing == 0:
                self.image = changecolor(self.image, 0.5, 0.5, 0.5)
                self.dealing = 1
            screen.blit(self.image, (self.rect.x - camera[0], self.rect.y - camera[1]))
        elif self.style == 7:  # 无头行走
            self.HP -= 0.6
            for planr in plant_list:
                if self.rect.colliderect(planr.rect):
                    self.collide=True
                    break
            if not self.collide:
                self.cjsindex += 0.1
                cjsblit = int(self.cjsindex % len(cjsdiewalk_frame))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + cjsdiewalk_frame[cjsblit].get_height()
                )
                screen.blit(
                    cjsdiewalk_frame[cjsblit],
                    (
                        self.rect.x - camera[0],
                        self.rect.y - camera[1],
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            else:
                self.noheadeatindex += 0.1
                noheadeatblit = int(self.noheadeatindex % len(cjsnoheadeat_frame))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + cjsnoheadeat_frame[noheadeatblit].get_height()
                )
                screen.blit(
                    cjsnoheadeat_frame[noheadeatblit],
                    (
                        self.rect.x - camera[0],
                        self.rect.y - camera[1],
                        self.rect.width,
                        self.rect.height,
                    ),
                )
                if self.HP <= 0:
                    self.style = 8
        elif self.style == 8:  # 尸体倒下
            self.fallindex += 0.1
            fallblit = int(self.fallindex)
            if fallblit < len(cjsfall_frame):
                rect = cjsfall_frame[fallblit].get_rect()
                screen.blit(cjsfall_frame[fallblit],\
                (self.rect.x - camera[0] - rect.width + self.rect.width - 10,\
                self.rect.y - camera[1] - rect.height + self.rect.height - 22,\
                self.rect.width,self.rect.height,))
            elif fallblit >= len(cjsfall_frame):
                emg.zombie_list.remove(self)
                self.kill()
        elif self.style == 9:  # 尸体倒下后消失
            emg.zombie_list.remove(self)
            self.kill()
        elif self.style == 10 :  # 吃植物
            if self.HP>70 and not self.hit:
                self.eatindex += 0.2
                eatblit = int(self.eatindex % len(cjseat_frame))
                screen.blit(
                    cjseat_frame[eatblit],
                        (self.rect.x - camera[0], self.rect.y - camera[1]),
                        )
                if not pygame.Rect(
                    player.rect.x - camera[0],
                    player.rect.y - camera[1] - (player.rect.width - 65),
                    player.rect.width,
                    player.rect.height,
                ).colliderect(
                    pygame.Rect(
                        self.rect.x - camera[0],
                        self.rect.y - camera[1],
                        self.rect.width,
                        self.rect.height,
                    )
                ):
                    self.style = 0
                    self.eating=False
            elif self.HP>70 and self.hit:
                self.eatindex+=0.2
                eatblit=int(self.eatindex%len(cjseat_frame))
                self.rect.x=self.x
                self.rect.y=screen_height-(self.y+cjseat_frame[eatblit].get_height())
                story=copy.copy(cjseat_frame[eatblit])
                if self.n<3:
                    self.n+=1
                    screen.blit(changecolor(story,1.6,1.6,1.6),
                                (self.rect.x-camera[0],self.rect.y-camera[1],
                                 self.rect.width,
                                 self.rect.height))
                if self.n==3:
                    self.n=0
                    self.hit=False
        if self.HP <= 70:
            if self.dealing < 1:
                global temp
                temp = (self.rect.x, self.rect.y)
                self.dealing = 1
            self.headindex += 0.2
            headblit = int(self.headindex)
            if headblit < len(head_frame):
                head = Fallthing(
                    head_frame[headblit],
                    temp[0] + f(self.headindex),
                    temp[1] + g(self.headindex, 0.5),
                    50,50
                )
                head.draw(camera)
            if self.money>=99:  #diamond
                self.moneyindex+=0.2
                moneyblit=int(self.moneyindex%5)+4
                if self.moneyindex<15:
                    diamond=Fallthing(
                        money_frame[moneyblit],
                        temp[0]-f(self.moneyindex),
                        temp[1]+g(self.moneyindex,0.5),
                        40,40
                    )
                    diamond.draw(camera)
                elif self.moneyindex<20:
                    x=temp[0]-f(15)+camera[0]
                    y=temp[1]+g(15,0.5)+camera[1]
                    diamond=Fallthing(
                        money_frame[moneyblit],
                        x-h(self.moneyindex-15,temp[0]-30),
                        y+h(self.moneyindex-15,630-temp[1]),
                        40,40
                    )
                    diamond.draw(camera)
                elif self.moneyindex<25:
                    player_money.add_money(1000)
                    self.moneyindex=114514
                else:
                    pass  
            elif self.money<99 and self.money>=94:  #goldcoin
                self.moneyindex+=0.2
                moneyblit=int(self.moneyindex%2)+2
                if self.moneyindex<15:
                    diamond=Fallthing(
                        money_frame[moneyblit],
                        temp[0]-f(self.moneyindex),
                        temp[1]+g(self.moneyindex,0.5),
                        40,40
                    )
                    diamond.draw(camera)
                elif self.moneyindex<20:
                    x=temp[0]-f(15)+camera[0]
                    y=temp[1]+g(15,0.5)+camera[1]
                    diamond=Fallthing(
                        money_frame[moneyblit],
                        x-h(self.moneyindex-15,temp[0]-30),
                        y+h(self.moneyindex-15,610-temp[1]),
                        40,40
                    )
                    diamond.draw(camera)
                elif self.moneyindex<25:
                    player_money.add_money(50)
                    self.moneyindex=114514
                else:
                    pass  
            elif self.money<94 and self.money>=75:  #coin
                self.moneyindex+=0.2
                moneyblit=int(self.moneyindex%2)
                if self.moneyindex<15:
                    diamond=Fallthing(
                        money_frame[moneyblit],
                        temp[0]-f(self.moneyindex),
                        temp[1]+g(self.moneyindex,0.5),
                        40,40
                    )
                    diamond.draw(camera)
                elif self.moneyindex<20:
                    x=temp[0]-f(15)+camera[0]
                    y=temp[1]+g(15,0.5)+camera[1]
                    diamond=Fallthing(
                        money_frame[moneyblit],
                        x-h(self.moneyindex-15,temp[0]-30),
                        y+h(self.moneyindex-15,610-temp[1]),
                        40,40
                    )
                    diamond.draw(camera)
                elif self.moneyindex<25:
                    player_money.add_money(10)
                    self.moneyindex=114514
                else:
                    pass  
    def move(self,default=0):
        if self.style!=9:
            self.x -= (self.move_speed+default)

    def is_fall(self):
        if self.HP <= 0:
            self.style = 8
            return True
        else:
            return False
    def is_end(self):
        if self.x <= 70 and self.style == 0:
            self.style = 1
            return True
        else:
            return False
        
class Roadblock_Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = roadblock_frame[0]
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.HP=370
        self.style=0
        self.move_speed = random.uniform(0.25,0.5)
        self.walkindex=0
        self.eatindex=0
        self.collide=False
        self.eating=False
        self.n=0
        self.dealing=0
        self.hit=False
        self.tag=2
        self.yfix=y
        self.force=2
    def draw(self, camera):
        if self.style==0: #行走
            self.walkindex+=0.2
            walkblit=int(self.walkindex%len(roadblock_frame))
            self.image=roadblock_frame[walkblit]
            self.rect.x = self.x
            self.rect.y = screen_height - (self.y + self.image.get_height())
            screen.blit(
                roadblock_frame[walkblit],
                (
                    self.rect.x - camera[0],
                    self.rect.y - camera[1],
                    self.rect.width,
                    self.rect.height,
                ),
            )
            if self.HP<=0:
                self.style=9
        elif self.style == 3:  # 被子弹击中
            for plans in plant_list:
                if self.rect.colliderect(plans.rect):
                    self.collide=True
                    break
            if not self.eating:
                self.walkindex += 0.1
                walkblit = int(self.walkindex % len(roadblock_frame))
                self.rect.x = self.x
                self.rect.y = screen_height - (self.y + roadblock_frame[walkblit].get_height())
                story = copy.copy(roadblock_frame[walkblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x - camera[0],
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 0
            if self.eating:
                self.eatindex += 0.1
                eatblit = int(self.eatindex % len(roadblockeat_frame))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + roadblockeat_frame[eatblit].get_height()
                )
                story=copy.copy(roadblockeat_frame[eatblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x - camera[0],
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 10
            if self.HP <= 0:
                self.style = 9   #不执行
        elif self.style == 4:  # 失败未进家
            self.rect.x = self.x
            self.rect.y = screen_height - (self.y + self.image.get_height())
            screen.blit(self.image, (self.rect.x - camera[0], self.rect.y - camera[1]))

        elif self.style == 5:  # 失败进家
            self.y = 200
            self.rect.x = self.x
            self.walkindex += 0.1
            walkblit = int(self.walkindex % len(roadblock_frame))
            self.y = screen_height - (self.y + roadblock_frame[walkblit].get_height())
            screen.blit(roadblock_frame[walkblit], (self.x - camera[0], self.y - camera[1]))
            zombie_rect = fm_cjs.get_rect()
            zombie_rect.x = self.x
            zombie_rect.y = self.y
            self.image = roadblock_frame[walkblit]
        elif self.style == 6:  # 失败未进家但吃完脑子
            if self.dealing == 0:
                self.image = changecolor(self.image, 0.5, 0.5, 0.5)
                self.dealing = 1
            screen.blit(self.image, (self.rect.x - camera[0], self.rect.y - camera[1]))
        elif self.style == 9:  # 尸体倒下后消失
            #self.rect.x = self.x
            #self.rect.y = screen_height - (self.y + self.image.get_height())
            emg.zombie_list.append(Zombie(self.rect.x, self.yfix))
            emg.zombie_list.remove(self)
            self.kill()
        elif self.style == 10 :  # 吃植物
            if not self.hit:
                self.eatindex += 0.2
                eatblit = int(self.eatindex % len(roadblockeat_frame))
                screen.blit(
                    roadblockeat_frame[eatblit],
                        (self.rect.x - camera[0], self.rect.y - camera[1]),
                        )
                if not pygame.Rect(
                    player.rect.x - camera[0],
                    player.rect.y - camera[1] - (player.rect.width - 65),
                    player.rect.width,
                    player.rect.height,
                ).colliderect(
                    pygame.Rect(
                        self.rect.x - camera[0],
                        self.rect.y - camera[1],
                        self.rect.width,
                        self.rect.height,
                    )
                ):
                    self.style = 0
                    self.eating=False
            elif self.hit:
                self.eatindex+=0.2
                eatblit=int(self.eatindex%len(roadblockeat_frame))
                self.rect.x=self.x
                self.rect.y=screen_height-(self.y+roadblockeat_frame[eatblit].get_height())
                story=copy.copy(roadblockeat_frame[eatblit])
                if self.n<3:
                    self.n+=1
                    screen.blit(changecolor(story,1.6,1.6,1.6),
                                (self.rect.x-camera[0],self.rect.y-camera[1],
                                 self.rect.width,
                                 self.rect.height))
                if self.n==3:
                    self.n=0
                    self.hit=False
            if self.HP<=0:
                self.style=9
    def move(self,default=0):
        if self.style!=9:
            self.x -= (self.move_speed+default)

    def is_fall(self):
        if self.HP <= 0:
            self.style = 9
            return True
        else:
            return False
    def is_end(self):
        if self.x <= 70 and self.style == 0:
            self.style = 1
            return True
        else:
            return False

class Bucket_Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bucket_frame[0]
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.HP=1100
        self.style=0
        self.move_speed = random.uniform(0.25,0.5)
        self.walkindex=0
        self.eatindex=0
        self.collide=False
        self.eating=False
        self.n=0
        self.dealing=0
        self.hit=False
        self.tag=3
        self.yfix=y
        self.force=3
    def draw(self, camera):
        if self.style==0: #行走
            self.walkindex+=0.2
            walkblit=int(self.walkindex%len(bucket_frame))
            self.image=bucket_frame[walkblit]
            self.rect.x = self.x
            self.rect.y = screen_height - (self.y + self.image.get_height())
            screen.blit(
                bucket_frame[walkblit],
                (
                    self.rect.x - camera[0],
                    self.rect.y - camera[1],
                    self.rect.width,
                    self.rect.height,
                ),
            )
            if self.HP<=0:
                self.style=9
        elif self.style == 3:  # 被子弹击中
            for plans in plant_list:
                if self.rect.colliderect(plans.rect):
                    self.collide=True
                    break
            if not self.eating:
                self.walkindex += 0.1
                walkblit = int(self.walkindex % len(bucket_frame))
                self.rect.x = self.x
                self.rect.y = screen_height - (self.y + bucket_frame[walkblit].get_height())
                story = copy.copy(bucket_frame[walkblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x - camera[0],
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 0
            if self.eating:
                self.eatindex += 0.1
                eatblit = int(self.eatindex % len(bucketeat_frame))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + bucketeat_frame[eatblit].get_height()
                )
                story=copy.copy(bucketeat_frame[eatblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x - camera[0],
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 10
            if self.HP <= 0:
                self.style = 9   #不执行
        elif self.style == 4:  # 失败未进家
            self.rect.x = self.x
            self.rect.y = screen_height - (self.y + self.image.get_height())
            screen.blit(self.image, (self.rect.x - camera[0], self.rect.y - camera[1]))

        elif self.style == 5:  # 失败进家
            self.y = 200
            self.rect.x = self.x
            self.walkindex += 0.1
            walkblit = int(self.walkindex % len(bucket_frame))
            self.y = screen_height - (self.y + bucket_frame[walkblit].get_height())
            screen.blit(bucket_frame[walkblit], (self.x - camera[0], self.y - camera[1]))
            zombie_rect = fm_cjs.get_rect()
            zombie_rect.x = self.x
            zombie_rect.y = self.y
            self.image = bucket_frame[walkblit]
        elif self.style == 6:  # 失败未进家但吃完脑子
            if self.dealing == 0:
                self.image = changecolor(self.image, 0.5, 0.5, 0.5)
                self.dealing = 1
            screen.blit(self.image, (self.rect.x - camera[0], self.rect.y - camera[1]))
        elif self.style == 9:  # 尸体倒下后消失
            #self.rect.x = self.x
            #self.rect.y = screen_height - (self.y + self.image.get_height())
            emg.zombie_list.append(Zombie(self.rect.x, self.yfix))
            emg.zombie_list.remove(self)
            self.kill()
        elif self.style == 10 :  # 吃植物
            if not self.hit:
                self.eatindex += 0.2
                eatblit = int(self.eatindex % len(bucketeat_frame))
                screen.blit(
                    bucketeat_frame[eatblit],
                        (self.rect.x - camera[0], self.rect.y - camera[1]),
                        )
                if not pygame.Rect(
                    player.rect.x - camera[0],
                    player.rect.y - camera[1] - (player.rect.width - 65),
                    player.rect.width,
                    player.rect.height,
                ).colliderect(
                    pygame.Rect(
                        self.rect.x - camera[0],
                        self.rect.y - camera[1],
                        self.rect.width,
                        self.rect.height,
                    )
                ):
                    self.style = 0
                    self.eating=False
            elif self.hit:
                self.eatindex+=0.2
                eatblit=int(self.eatindex%len(bucketeat_frame))
                self.rect.x=self.x
                self.rect.y=screen_height-(self.y+bucketeat_frame[eatblit].get_height())
                story=copy.copy(bucketeat_frame[eatblit])
                if self.n<3:
                    self.n+=1
                    screen.blit(changecolor(story,1.6,1.6,1.6),
                                (self.rect.x-camera[0],self.rect.y-camera[1],
                                 self.rect.width,
                                 self.rect.height))
                if self.n==3:
                    self.n=0
                    self.hit=False
            if self.HP<=0:
                self.style=9
    def move(self,default=0):
        if self.style!=9:
            self.x -= (self.move_speed+default)

    def is_fall(self):
        if self.HP <= 0:
            self.style = 9
            return True
        else:
            return False
    def is_end(self):
        if self.x <= 70 and self.style == 0:
            self.style = 1
            return True
        else:
            return False
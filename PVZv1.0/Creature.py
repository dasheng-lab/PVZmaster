import pygame
import random
import sys
import time
import copy
from Event import *
from Obstacle import *
from Openai import *
from Pautton import *
from Moneymanager import *
from Resources import *
from Music import *


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
        self.besthp = 1000
        self.hp = self.besthp
        self.blight = 0
        self.place = 0
        self.beat = 20
        self.shoot_speed = 80
        self.story = [5, 1000, 1000, 20, 80]
        self.pause = False
        self.n = 0
        self.reasontime = 0
        self.dealing = 0

    def listen(self, event: Event):  # 玩家类所响应的事件
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
        self.pause = pausemanager.pause
        if not self.pause:
            stay0__1obstacle = obstacl_class[self.place][0].collide(self, 0, -1)
            stay0_1obstacle = obstacl_class[self.place][0].collide(self, 0, 1)
            stay1__0obstacle = obstacl_class[self.place][0].collide(self, -1, 0)
            stay1_0obstacle = obstacl_class[self.place][0].collide(self, 1, 0)
            for obstale in obstacl_class[self.place][
                1 : len(obstacl_class[self.place])
            ]:
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
                        bulletlist_right.add(Bullet(self, 2))
                        audio_player.play_sound("豌豆发射", 0, 0.4)
                    else:
                        bulletlist_left.add(Bullet(self, 2))
                        audio_player.play_sound("豌豆发射", 0, 0.4)
                    shooter_count = 0
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_1]:
            text0 = f"攻击力：{self.beat:.1f},射速：{(80/self.shoot_speed)*100:.3f}%,最大生命值：{self.besthp},移速：{self.speed:.2f}"
            self.post(Event(Event_kind.WORDS, {"text": text0}))

    def draw(self, camera, style=0):
        if style != 11 and style != 12:
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
        elif style == 7:
            if camera[0] + 500 - self.rect.x > camera_lack and camera[0] > -1000:
                camera[0] = self.rect.x - 500 + camera_lack
            if -camera[0] - 500 + self.rect.x > camera_lack and camera[0] < 0:
                camera[0] = self.rect.x - 500 - camera_lack
            if camera[1] + 350 - self.rect.y > camera_lack and camera[1] > 0:
                camera[1] = self.rect.y - 350 + camera_lack
            if -camera[1] - 300 + self.rect.y > camera_lack and camera[1] < 600:
                camera[1] = self.rect.y - 300 - camera_lack
        elif style == 12:
            story = copy.copy(player_image)
            screen.blit(
                changecolor(story, 0.6, 0.6, 0.6),
                pygame.Rect(
                    self.rect.x - camera[0],
                    self.rect.y - camera[1] - (player_rect.width - 65),
                    player_rect.width,
                    player_rect.height,
                ),
            )
        self.be_eaten(camera)
        if style != 12:
            if self.blight == 0:
                screen.blit(
                    player_image,
                    pygame.Rect(
                        self.rect.x - camera[0],
                        self.rect.y - camera[1] - (player_rect.width - 65),
                        player_rect.width,
                        player_rect.height,
                    ),
                )
            elif self.blight <= 3:
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
        screen.blit(self.blood_image, (0, -20))
        text1 = font2.render(f"{int(self.hp)}", True, (0, 0, 0))
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
                zombie.collide = True
            else:
                zombie.collide = False
            if (zombie.tag == 1 or zombie.tag == 5) and (
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
                zombie.eating = True
                if zombie.snow == 0:
                    self.hp -= 3
                elif zombie.snow == 1:
                    self.hp -= 1.5
                self.blight = 1
                audio_player.play_sound("啃植物", 0, 0.5)
                if self.hp <= 0:
                    self.hp = 1000
                    self.post(Event(Event_kind.EATEN, {"objecct": player}))
            else:
                zombie.eating = False
            if (zombie.tag == 2 or zombie.tag == 3) and (
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
                zombie.style = 10
                zombie.eating = True
                if zombie.snow == 0:
                    self.hp -= 3
                elif zombie.snow == 1:
                    self.hp -= 1.5
                self.blight = 1
                audio_player.play_sound("啃植物", 0, 0.5)
                if self.hp <= 0:
                    self.hp = 1000
                    self.post(Event(Event_kind.EATEN, {"objecct": player}))
            else:
                zombie.eating = False
            if zombie.tag == 4 and (
                pygame.Rect(
                    self.rect.x - camera[0] - 80,
                    self.rect.y - camera[1] - (self.rect.width - 65),
                    self.rect.width,
                    self.rect.height,
                ).colliderect(
                    pygame.Rect(
                        zombie.rect.x - camera[0],
                        zombie.rect.y - camera[1],
                        zombie.rect.width // 2,
                        zombie.rect.height // 2,
                    )
                )
                and zombie.style != 8
                and zombie.style != 9
                and zombie.HP > 120
            ):
                zombie.style = 10
                zombie.eating = True
                if zombie.snow == 0:
                    self.hp -= 3
                elif zombie.snow == 1:
                    self.hp -= 1.5
                self.blight = 1
                audio_player.play_sound("啃植物", 0, 0.5)
                if self.hp <= 0:
                    self.hp = 1000
                    self.post(Event(Event_kind.EATEN, {"objecct": player}))
            else:
                zombie.eating = False
            if zombie.tag == 6 and (
                pygame.Rect(
                    self.rect.x - camera[0] - 60,
                    self.rect.y - camera[1] - (self.rect.width - 65) - 10,
                    self.rect.width,
                    self.rect.height,
                ).colliderect(
                    pygame.Rect(
                        zombie.rect.x - camera[0],
                        zombie.rect.y - camera[1],
                        zombie.rect.width // 2,
                        zombie.rect.height // 2,
                    )
                )
                and zombie.style != 8
                and zombie.style != 9
                and zombie.style != 12
                and zombie.HP > 120
            ):
                zombie.style = 10
                zombie.eating = True
                if zombie.snow == 0 or zombie.HP > 720:
                    self.hp -= 24
                elif zombie.snow == 1 and zombie.HP <= 720:
                    self.hp -= 12
                self.blight = 1
                audio_player.play_sound("啃植物", 0, 0.5)
                if self.hp <= 0:
                    self.hp = self.besthp
                    self.post(Event(Event_kind.EATEN, {"objecct": player}))
            else:
                zombie.eating = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, shooter, kind):
        super().__init__()
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (22, 22))
        self.image1 = pygame.image.load("images/冰豆.png").convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, (22, 22))
        self.rect = self.image.get_rect()
        try:
            self.rect.x = shooter.rect2.x + 35
            self.rect.y = shooter.rect2.y + 5.5
        except:
            self.rect.x = shooter.rect.x + 35
            self.rect.y = shooter.rect.y + 5.5
        self.speed = 8
        self.pic_diex = 0
        self.kind = kind
        self.dealing = 0

    def draw(self, camera, style=0):
        if self.kind == 0 or self.kind == 2:
            if style != 12:
                screen.blit(
                    self.image,
                    pygame.Rect(
                        self.rect.x - camera[0],
                        self.rect.y - camera[1],
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            else:
                story = copy.copy(self.image)
                screen.blit(
                    changecolor(story, 0.6, 0.6, 0.6),
                    pygame.Rect(
                        self.rect.x - camera[0],
                        self.rect.y - camera[1],
                        self.rect.width,
                        self.rect.height,
                    ),
                )
        elif self.kind == 1:
            if style != 12:
                screen.blit(
                    self.image1,
                    pygame.Rect(
                        self.rect.x - camera[0],
                        self.rect.y - camera[1],
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            else:
                story = copy.copy(self.image1)
                screen.blit(
                    changecolor(story, 0.6, 0.6, 0.6),
                    pygame.Rect(
                        self.rect.x - camera[0],
                        self.rect.y - camera[1],
                        self.rect.width,
                        self.rect.height,
                    ),
                )

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
            ) and self.dealing == 0:
                if zombie.tag != 6:
                    if self.kind == 2:
                        if self.dealing == 0:
                            zombie.HP -= player.beat
                            self.dealing = 1
                    else:
                        if self.dealing == 0:
                            zombie.HP -= 20
                            self.dealing = 1
                else:
                    if zombie.HP > 720:
                        if self.kind == 2:
                            if self.dealing == 0:
                                zombie.HP -= player.beat
                                self.dealing = 1
                        else:
                            if self.dealing == 0:
                                zombie.HP -= 20
                                self.dealing = 1
                        if zombie.HP <= 720:
                            zombie.HP = 720
                            zombie.style = 12
                    else:
                        if self.kind == 2:
                            if self.dealing == 0:
                                zombie.HP -= player.beat
                                self.dealing = 1
                        else:
                            if self.dealing == 0:
                                zombie.HP -= 20
                                self.dealing = 1
                if zombie.tag == 1 or zombie.tag == 5 or zombie.tag == 6:
                    audio_player.play_sound("豌豆击中1", 0, 0.5)
                if zombie.tag == 2 or zombie.tag == 4:
                    audio_player.play_sound("豌豆击中3", 0, 0.5)
                if zombie.tag == 3:
                    audio_player.play_sound("豌豆击中4", 0, 0.5)
                if zombie.style != 12:
                    zombie.style = 3
                    zombie.hit = True
                if self.kind == 1:
                    if not (zombie.tag == 6 and zombie.HP > 720):
                        zombie.snowcount = 700
                self.kill()
                if self in bulletlist_left:
                    bulletlist_left.remove(self)
                else:
                    bulletlist_right.remove(self)
            if self.dealing == 1:
                break


pygame.font.init()
FONTS = [
    pygame.font.Font(pygame.font.get_default_font(), font_size)
    for font_size in [48, 36, 24]
]
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
    def __init__(self, image, x, y, width, height):
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, camera):
        screen.blit(
            self.image,
            pygame.Rect(
                self.x - camera[0], self.y - camera[1], self.width, self.height
            ),
        )


class ZombieManager(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.zombie_list = []
        self.dealing = 0
        self.count = 0

    def gen_new_zombie(self, gen, x=1000):
        # gen=random.choice([425,315,230,125,25])
        self.zombie_list.append(Zombie(x, gen))

    def gen_new_roadblock_zombie(self, gen, x=1000):
        self.zombie_list.append(Roadblock_Zombie(x, gen))

    def gen_new_bucket_zombie(self, gen, x=1000):
        self.zombie_list.append(Bucket_Zombie(x, gen))

    def gen_new_rugby_zombie(self, gen, x=1000):
        self.zombie_list.append(Rugby_Zombie(x, gen))

    def gen_new_flag_zombie(self, gen, x=950):
        self.zombie_list.append(Flag_Zombie(x, gen))

    def gen_new_paper_zombie(self, gen, x=950):
        self.zombie_list.append(Paper_Zombie(x, gen))

    def AIput(self, playerx, playery, force, subforce=1):
        staystr = AI_decision(playerx, playery)
        if force == 1:  # 普通僵尸
            if subforce == 1:
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
            elif subforce == 2:
                if "425" in staystr:
                    self.gen_new_flag_zombie(425)
                elif "315" in staystr:
                    self.gen_new_flag_zombie(315)
                elif "230" in staystr:
                    self.gen_new_flag_zombie(210)
                elif "125" in staystr:
                    self.gen_new_flag_zombie(125)
                elif "25" in staystr:
                    self.gen_new_flag_zombie(25)
                else:
                    gen2 = random.choice([425, 315, 210, 125, 25])
                    self.gen_new_flag_zombie(gen2)
        elif force == 2:  # 路障僵尸
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
        elif force == 3:  # 铁桶僵尸
            if subforce == 1:
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
            elif subforce == 2:
                if "425" in staystr:
                    self.gen_new_paper_zombie(425)
                elif "315" in staystr:
                    self.gen_new_paper_zombie(315)
                elif "230" in staystr:
                    self.gen_new_paper_zombie(210)
                elif "125" in staystr:
                    self.gen_new_paper_zombie(125)
                elif "25" in staystr:
                    self.gen_new_paper_zombie(25)
                else:
                    gen3 = random.choice([425, 315, 210, 125, 25])
                    self.gen_new_paper_zombie(gen3)
        elif force == 4:  # 橄榄球僵尸
            if "425" in staystr:
                self.gen_new_rugby_zombie(425)
            elif "315" in staystr:
                self.gen_new_rugby_zombie(315)
            elif "230" in staystr:
                self.gen_new_rugby_zombie(210)
            elif "125" in staystr:
                self.gen_new_rugby_zombie(125)
            elif "25" in staystr:
                self.gen_new_rugby_zombie(25)
            else:
                gen3 = random.choice([425, 315, 210, 125, 25])
                self.gen_new_rugby_zombie(gen3)

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
        self.move_speed = random.uniform(0.2, 0.3)
        self.cjsindex = 0
        self.headindex = 0
        self.fallindex = 0
        self.eatindex = 0
        self.noheadeatindex = 0
        self.moneyindex = 0
        self.image = pygame.image.load("images/commonjs/cjs1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.n = 0
        self.dealing = 0
        self.eating = False
        self.hit = False
        self.collide = False
        self.money = random.randint(0, 100)
        self.tag = 1
        self.force = 1
        self.snowcount = 0
        self.snow = 0
        self.falltemp = (self.rect.x, self.rect.y)
        self.dealing1 = 0

    def draw(self, camera):
        if self.snowcount > 0:
            self.snowcount -= 1
            self.snow = 1
        else:
            self.snow = 0
        if self.style == 0 or self.style == 1:  # 正常移动
            self.cjsindex += 0.1 / (self.snow + 1)
            cjsblit = int(self.cjsindex % len(frame0[self.snow]))
            self.rect.x = self.x
            self.rect.y = screen_height - (
                self.y + frame0[self.snow][cjsblit].get_height()
            )
            screen.blit(
                frame0[self.snow][cjsblit],
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
                    self.collide = True
                    break
            if self.HP > 70 and not self.eating:
                self.cjsindex += 0.1 / (self.snow + 1)
                cjsblit = int(self.cjsindex % len(frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + frame0[self.snow][cjsblit].get_height()
                )
                story = copy.copy(frame0[self.snow][cjsblit])
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
                self.cjsindex += 0.1 / (self.snow + 1)
                cjsblit = int(self.cjsindex % len(cjsdiewalk_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + cjsdiewalk_frame0[self.snow][cjsblit].get_height()
                )
                story = copy.copy(cjsdiewalk_frame0[self.snow][cjsblit])
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
                self.eatindex += 0.1 / (self.snow + 1)
                eatblit = int(self.eatindex % len(cjseat_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + cjseat_frame0[self.snow][eatblit].get_height()
                )
                story = copy.copy(cjseat_frame0[self.snow][eatblit])
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
                self.noheadeatindex += 0.1 / (self.snow + 1)
                noheadeatblit = int(
                    self.noheadeatindex % len(cjsnoheadeat_frame0[self.snow])
                )
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + cjsnoheadeat_frame0[self.snow][noheadeatblit].get_height()
                )
                story = copy.copy(cjsnoheadeat_frame0[self.snow][noheadeatblit])
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
            self.cjsindex += 0.1 / (self.snow + 1)
            cjsblit = int(self.cjsindex % len(frame0[self.snow]))
            self.y = screen_height - (self.y + frame0[self.snow][cjsblit].get_height())
            screen.blit(
                frame0[self.snow][cjsblit], (self.x - camera[0], self.y - camera[1])
            )
        elif self.style == 6:  # 失败未进家但吃完脑子
            story = copy.copy(self.image)
            screen.blit(
                changecolor(story, 0.5, 0.5, 0.5),
                (self.rect.x - camera[0], self.rect.y - camera[1]),
            )
        elif self.style == 7:  # 无头行走
            self.HP -= 0.6
            for planr in plant_list:
                if self.rect.colliderect(planr.rect):
                    self.collide = True
                    break
            if not self.collide:
                self.cjsindex += 0.1 / (self.snow + 1)
                cjsblit = int(self.cjsindex % len(cjsdiewalk_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + cjsdiewalk_frame0[self.snow][cjsblit].get_height()
                )
                screen.blit(
                    cjsdiewalk_frame0[self.snow][cjsblit],
                    (
                        self.rect.x - camera[0],
                        self.rect.y - camera[1],
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            else:
                self.noheadeatindex += 0.1 / (self.snow + 1)
                noheadeatblit = int(
                    self.noheadeatindex % len(cjsnoheadeat_frame0[self.snow])
                )
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + cjsnoheadeat_frame0[self.snow][noheadeatblit].get_height()
                )
                screen.blit(
                    cjsnoheadeat_frame0[self.snow][noheadeatblit],
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
            self.fallindex += 0.1 / (self.snow + 1)
            fallblit = int(self.fallindex)
            if fallblit < len(cjsfall_frame0[self.snow]):
                rect = cjsfall_frame0[self.snow][fallblit].get_rect()
                screen.blit(
                    cjsfall_frame0[self.snow][fallblit],
                    (
                        self.rect.x - camera[0] - rect.width + self.rect.width - 10,
                        self.rect.y - camera[1] - rect.height + self.rect.height - 22,
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            elif fallblit >= len(cjsfall_frame0[self.snow]):
                emg.zombie_list.remove(self)
                self.kill()
        elif self.style == 9:  # 尸体倒下后消失
            emg.zombie_list.remove(self)
            self.kill()
        elif self.style == 10:  # 吃植物
            if self.HP > 70 and not self.hit:
                self.eatindex += 0.2 / (self.snow + 1)
                eatblit = int(self.eatindex % len(cjseat_frame0[self.snow]))
                screen.blit(
                    cjseat_frame0[self.snow][eatblit],
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
                    self.eating = False
            elif self.HP > 70 and self.hit:
                self.eatindex += 0.2 / (self.snow + 1)
                eatblit = int(self.eatindex % len(cjseat_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + cjseat_frame0[self.snow][eatblit].get_height()
                )
                story = copy.copy(cjseat_frame0[self.snow][eatblit])
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
                    self.hit = False
        if self.HP <= 70:
            if self.dealing < 1:
                self.falltemp = (self.rect.x, self.rect.y)
                self.dealing = 1
            self.headindex += 0.2 / (self.snow + 1)
            headblit = int(self.headindex)
            if headblit < len(head_frame):
                head = Fallthing(
                    head_frame[headblit],
                    self.falltemp[0] + f(self.headindex),
                    self.falltemp[1] + g(self.headindex, 0.5),
                    50,
                    50,
                )
                head.draw(camera)
            if self.money >= 100:  # diamond
                self.moneyindex += 0.2
                moneyblit = int(self.moneyindex % 5) + 4
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)
                    audio_player.play_sound("产生钻石", 0, 0.5)
                if self.moneyindex < 15:
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        self.falltemp[0] - f(self.moneyindex),
                        self.falltemp[1] + g(self.moneyindex, 0.5),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 20:
                    x = self.falltemp[0] - f(15) + camera[0]
                    y = self.falltemp[1] + g(15, 0.5) + camera[1]
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        x - h(self.moneyindex - 15, self.falltemp[0] - 30),
                        y + h(self.moneyindex - 15, 630 - self.falltemp[1]),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 25:
                    player_money.add_money(1000)
                    self.moneyindex = 114514
                else:
                    pass
            elif self.money < 100 and self.money >= 94:  # goldcoin
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)
                    audio_player.play_sound("产生币", 0, 0.5)
                self.moneyindex += 0.2
                moneyblit = int(self.moneyindex % 2) + 2
                if self.moneyindex < 15:
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        self.falltemp[0] - f(self.moneyindex),
                        self.falltemp[1] + g(self.moneyindex, 0.5),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 20:
                    x = self.falltemp[0] - f(15) + camera[0]
                    y = self.falltemp[1] + g(15, 0.5) + camera[1]
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        x - h(self.moneyindex - 15, self.falltemp[0] - 30),
                        y + h(self.moneyindex - 15, 610 - self.falltemp[1]),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 25:
                    player_money.add_money(50)
                    self.moneyindex = 114514
                else:
                    pass
            elif self.money < 94 and self.money >= 75:  # coin
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)
                    audio_player.play_sound("产生币", 0, 0.5)
                self.moneyindex += 0.2
                moneyblit = int(self.moneyindex % 2)
                if self.moneyindex < 15:
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        self.falltemp[0] - f(self.moneyindex),
                        self.falltemp[1] + g(self.moneyindex, 0.5),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 20:
                    x = self.falltemp[0] - f(15) + camera[0]
                    y = self.falltemp[1] + g(15, 0.5) + camera[1]
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        x - h(self.moneyindex - 15, self.falltemp[0] - 30),
                        y + h(self.moneyindex - 15, 610 - self.falltemp[1]),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 25:
                    player_money.add_money(10)
                    self.moneyindex = 114514
            else:
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)

    def move(self, default=0):
        if (
            self.style != 9
            and not (self.style == 3 and self.eating)
            and self.style != 1
        ):
            self.x -= self.move_speed / (self.snow + 1) + default

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
        self.HP = 370
        self.style = 0
        self.move_speed = random.uniform(0.25, 0.5)
        self.walkindex = 0
        self.eatindex = 0
        self.collide = False
        self.eating = False
        self.n = 0
        self.dealing = 0
        self.hit = False
        self.tag = 2
        self.yfix = y
        self.force = 2
        self.snowcount = 0
        self.snow = 0

    def draw(self, camera):
        if self.snowcount > 0:
            self.snowcount -= 1
            self.snow = 1
        else:
            self.snow = 0
        if self.style == 0 or self.style == 1:  # 行走
            self.walkindex += 0.1 / (self.snow + 1)
            walkblit = int(self.walkindex % len(roadblock_frame0[self.snow]))
            self.image = roadblock_frame0[self.snow][walkblit]
            self.rect.x = self.x
            self.rect.y = screen_height - (self.y + self.image.get_height())
            screen.blit(
                roadblock_frame0[self.snow][walkblit],
                (
                    self.rect.x - camera[0],
                    self.rect.y - camera[1],
                    self.rect.width,
                    self.rect.height,
                ),
            )
            if self.HP <= 0:
                self.style = 9
        elif self.style == 3:  # 被子弹击中
            for plans in plant_list:
                if self.rect.colliderect(plans.rect):
                    self.collide = True
                    break
            if not self.eating:
                self.walkindex += 0.1 / (self.snow + 1)
                walkblit = int(self.walkindex % len(roadblock_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + roadblock_frame0[self.snow][walkblit].get_height()
                )
                story = copy.copy(roadblock_frame0[self.snow][walkblit])
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
                self.eatindex += 0.1 / (self.snow + 1)
                eatblit = int(self.eatindex % len(roadblockeat_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + roadblockeat_frame0[self.snow][eatblit].get_height()
                )
                story = copy.copy(roadblockeat_frame0[self.snow][eatblit])
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
                self.style = 9  # 不执行
        elif self.style == 4:  # 失败未进家
            self.rect.x = self.x
            self.rect.y = screen_height - (self.y + self.image.get_height())
            screen.blit(self.image, (self.rect.x - camera[0], self.rect.y - camera[1]))
        elif self.style == 5:  # 失败进家
            self.y = 200
            self.rect.x = self.x
            self.walkindex += 0.1 / (self.snow + 1)
            walkblit = int(self.walkindex % len(roadblock_frame0[self.snow]))
            self.y = screen_height - (
                self.y + roadblock_frame0[self.snow][walkblit].get_height()
            )
            screen.blit(
                roadblock_frame0[self.snow][walkblit],
                (self.x - camera[0], self.y - camera[1]),
            )
        elif self.style == 6:  # 失败未进家但吃完脑子
            story = copy.copy(self.image)
            screen.blit(
                changecolor(story, 0.5, 0.5, 0.5),
                (self.rect.x - camera[0], self.rect.y - camera[1]),
            )
        elif self.style == 9:  # 尸体倒下后消失
            emg.zombie_list.append(Zombie(self.rect.x, self.yfix))
            emg.zombie_list.remove(self)
            self.kill()
        elif self.style == 10:  # 吃植物
            if not self.hit:
                self.eatindex += 0.2
                eatblit = int(self.eatindex % len(roadblockeat_frame0[self.snow]))
                screen.blit(
                    roadblockeat_frame0[self.snow][eatblit],
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
                    self.eating = False
            elif self.hit:
                self.eatindex += 0.2 / (self.snow + 1)
                eatblit = int(self.eatindex % len(roadblockeat_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + roadblockeat_frame0[self.snow][eatblit].get_height()
                )
                story = copy.copy(roadblockeat_frame0[self.snow][eatblit])
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
                    self.hit = False
            if self.HP <= 0:
                self.style = 9

    def move(self, default=0):
        if (
            self.style != 9
            and not (self.style == 3 and self.eating)
            and self.style != 1
        ):
            self.x -= self.move_speed / (self.snow + 1) + default

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
        self.HP = 1100
        self.style = 0
        self.move_speed = random.uniform(0.25, 0.5)
        self.walkindex = 0
        self.eatindex = 0
        self.collide = False
        self.eating = False
        self.n = 0
        self.dealing = 0
        self.hit = False
        self.tag = 3
        self.yfix = y
        self.force = 3
        self.snowcount = 0
        self.snow = 0

    def draw(self, camera):
        if self.snowcount > 0:
            self.snowcount -= 1
            self.snow = 1
        else:
            self.snow = 0
        if self.style == 0 or self.style == 1:  # 行走
            self.walkindex += 0.1 / (self.snow + 1)
            walkblit = int(self.walkindex % len(bucket_frame0[self.snow]))
            self.image = bucket_frame0[self.snow][walkblit]
            self.rect.x = self.x
            self.rect.y = screen_height - (self.y + self.image.get_height())
            screen.blit(
                bucket_frame0[self.snow][walkblit],
                (
                    self.rect.x - camera[0],
                    self.rect.y - camera[1],
                    self.rect.width,
                    self.rect.height,
                ),
            )
            if self.HP <= 0:
                self.style = 9
        elif self.style == 3:  # 被子弹击中
            for plans in plant_list:
                if self.rect.colliderect(plans.rect):
                    self.collide = True
                    break
            if not self.eating:
                self.walkindex += 0.1 / (self.snow + 1)
                walkblit = int(self.walkindex % len(bucket_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + bucket_frame0[self.snow][walkblit].get_height()
                )
                story = copy.copy(bucket_frame0[self.snow][walkblit])
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
                self.eatindex += 0.1 / (self.snow + 1)
                eatblit = int(self.eatindex % len(bucketeat_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + bucketeat_frame0[self.snow][eatblit].get_height()
                )
                story = copy.copy(bucketeat_frame0[self.snow][eatblit])
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
                self.style = 9  # 不执行
        elif self.style == 4:  # 失败未进家
            self.rect.x = self.x
            self.rect.y = screen_height - (self.y + self.image.get_height())
            screen.blit(self.image, (self.rect.x - camera[0], self.rect.y - camera[1]))

        elif self.style == 5:  # 失败进家
            self.y = 200
            self.rect.x = self.x
            self.walkindex += 0.1 / (self.snow + 1)
            walkblit = int(self.walkindex % len(bucket_frame0[self.snow]))
            self.y = screen_height - (
                self.y + bucket_frame0[self.snow][walkblit].get_height()
            )
            screen.blit(
                bucket_frame0[self.snow][walkblit],
                (self.x - camera[0], self.y - camera[1]),
            )
        elif self.style == 6:  # 失败未进家但吃完脑子
            story = copy.copy(self.image)
            screen.blit(
                changecolor(story, 0.5, 0.5, 0.5),
                (self.rect.x - camera[0], self.rect.y - camera[1]),
            )
        elif self.style == 9:  # 尸体倒下后消失
            # self.rect.x = self.x
            # self.rect.y = screen_height - (self.y + self.image.get_height())
            emg.zombie_list.append(Zombie(self.rect.x, self.yfix))
            emg.zombie_list.remove(self)
            self.kill()
        elif self.style == 10:  # 吃植物
            if not self.hit:
                self.eatindex += 0.2 / (self.snow + 1)
                eatblit = int(self.eatindex % len(bucketeat_frame0[self.snow]))
                screen.blit(
                    bucketeat_frame0[self.snow][eatblit],
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
                    self.eating = False
            elif self.hit:
                self.eatindex += 0.2 / (self.snow + 1)
                eatblit = int(self.eatindex % len(bucketeat_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + bucketeat_frame0[self.snow][eatblit].get_height()
                )
                story = copy.copy(bucketeat_frame0[self.snow][eatblit])
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
                    self.hit = False
            if self.HP <= 0:
                self.style = 9

    def move(self, default=0):
        if (
            self.style != 9
            and not (self.style == 3 and self.eating)
            and self.style != 1
        ):
            self.x -= self.move_speed / (1 + self.snow) + default

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


class Rugby_Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = rugby_frame[0]
        self.image2 = rugbynocap_frame[0]
        self.style = 0
        self.x = x
        self.y = y
        self.HP = 500 + 1400
        self.move_speed = random.uniform(0.5, 0.6)
        self.walkindex = 0
        self.headindex = 0
        self.fallindex = 0
        self.eatindex = 0
        self.nocapeatindex = 0
        self.noheadeatindex = 0
        self.moneyindex = 0
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.n = 0
        self.dealing = 0
        self.eating = False
        self.hit = False
        self.collide = False
        self.money = random.randint(0, 100)
        self.tag = 4
        self.force = 4
        self.snowcount = 0
        self.snow = 0
        self.falltemp = (self.rect.x, self.rect.y)
        self.dealing1 = 0

    def draw(self, camera):
        if self.snowcount > 0:
            self.snowcount -= 1
            self.snow = 1
        else:
            self.snow = 0
        if self.style == 0 or self.style == 1:  # 正常移动
            self.walkindex += 0.25 / (self.snow + 1)
            walkblit = int(self.walkindex % len(rugby_frame0[self.snow]))
            self.rect.x = self.x
            self.rect.y = screen_height - (
                self.y + rugby_frame0[self.snow][walkblit].get_height()
            )
            screen.blit(
                rugby_frame0[self.snow][walkblit],
                (
                    self.rect.x
                    - camera[0]
                    + (160 - rugby_frame0[self.snow][walkblit].get_width()),
                    self.rect.y - camera[1],
                    self.rect.width,
                    self.rect.height,
                ),
            )
        elif self.style == 3:  # 被子弹击中
            for plans in plant_list:
                if pygame.Rect(
                    self.rect.x + 40,
                    self.rect.y + 40,
                    self.rect.width / 3,
                    self.rect.height / 3,
                ).colliderect(plans.rect):
                    self.collide = True
                    break
            if self.HP > 500 and not self.eating:
                self.walkindex += 0.1 / (self.snow + 1)
                walkblit = int(self.walkindex % len(rugby_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + rugby_frame0[self.snow][walkblit].get_height()
                )
                story = copy.copy(rugby_frame0[self.snow][walkblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (160 - rugby_frame0[self.snow][walkblit].get_width()),
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 0

            elif self.HP <= 500 and self.HP > 120 and not self.eating:
                self.walkindex += 0.1 / (self.snow + 1)
                walkblit = int(self.walkindex % len(rugbynocap_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + rugbynocap_frame0[self.snow][walkblit].get_height()
                )
                story = copy.copy(rugbynocap_frame0[self.snow][walkblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (
                                160 - rugbynocap_frame0[self.snow][walkblit].get_width()
                            ),
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 11  # need change
            elif self.HP <= 120 and self.HP > 0 and not self.collide:
                self.walkindex += 0.1 / (self.snow + 1)
                walkblit = int(self.walkindex % len(rugbynohead_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + rugbynohead_frame0[self.snow][walkblit].get_height()
                )
                story = copy.copy(rugbynohead_frame0[self.snow][walkblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (
                                160
                                - rugbynohead_frame0[self.snow][walkblit].get_width()
                            ),
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 7
            elif self.HP > 500 and self.eating:
                self.eatindex += 0.1 / (self.snow + 1)
                eatblit = int(self.eatindex % len(rugbyeat_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + rugbyeat_frame0[self.snow][eatblit].get_height()
                )
                story = copy.copy(rugbyeat_frame0[self.snow][eatblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (160 - rugbyeat_frame0[self.snow][eatblit].get_width()),
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 10

            elif self.HP <= 500 and self.HP > 120 and self.eating:
                self.nocapeatindex += 0.1 / (self.snow + 1)
                nocapeatblit = int(
                    self.nocapeatindex % len(rugbynocapeat_frame0[self.snow])
                )
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + rugbynocapeat_frame0[self.snow][nocapeatblit].get_height()
                )
                story = copy.copy(rugbynocapeat_frame0[self.snow][nocapeatblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (
                                160
                                - rugbynocapeat_frame0[self.snow][
                                    nocapeatblit
                                ].get_width()
                            ),
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 10  # need change

            elif self.HP <= 120 and self.HP > 0 and self.collide:
                self.noheadeatindex += 0.1 / (self.snow + 1)
                noheadeatblit = int(
                    self.noheadeatindex % len(rugbynoheadeat_frame0[self.snow])
                )
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y
                    + rugbynoheadeat_frame0[self.snow][noheadeatblit].get_height()
                )
                story = copy.copy(rugbynoheadeat_frame0[self.snow][noheadeatblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (
                                160
                                - rugbynoheadeat_frame0[self.snow][
                                    noheadeatblit
                                ].get_width()
                            ),
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
            if self.HP > 500:
                self.rect.x = self.x
                self.rect.y = screen_height - (self.y + self.image.get_height())
                screen.blit(
                    self.image, (self.rect.x - camera[0], self.rect.y - camera[1])
                )
            else:
                self.rect.x = self.x
                self.rect.y = screen_height - (self.y + self.image2.get_height())
                screen.blit(
                    self.image2, (self.rect.x - camera[0], self.rect.y - camera[1])
                )

        elif self.style == 5:  # 失败进家
            self.y = 200
            self.rect.x = self.x
            self.walkindex += 0.1 / (self.snow + 1)
            walkblit = int(self.walkindex % len(rugby_frame0[self.snow]))
            self.y = screen_height - (
                self.y + rugby_frame0[self.snow][walkblit].get_height()
            )
            if self.HP > 500:
                screen.blit(
                    rugby_frame0[self.snow][walkblit],
                    (self.x - camera[0], self.y - camera[1]),
                )
                self.image = rugby_frame0[self.snow][walkblit]
            else:
                screen.blit(
                    rugbynocap_frame0[self.snow][walkblit],
                    (self.x - camera[0], self.y - camera[1]),
                )
                self.image2 = rugbynocap_frame0[self.snow][walkblit]
        elif self.style == 6:  # 失败未进家但吃完脑子
            if self.HP > 500:
                story = copy.copy(self.image)
                screen.blit(
                    changecolor(story, 0.6, 0.6, 0.6),
                    (self.rect.x - camera[0], self.rect.y - camera[1]),
                )
            else:
                story = copy.copy(self.image2)
                screen.blit(
                    changecolor(story, 0.6, 0.6, 0.6),
                    (self.rect.x - camera[0], self.rect.y - camera[1]),
                )
        elif self.style == 7:  # 无头行走
            self.HP -= 0.5
            for planr in plant_list:
                if pygame.Rect(
                    self.rect.x
                    - camera[0]
                    + (160 - rugbynohead_frame0[self.snow][0].get_width()),
                    self.rect.y - camera[1],
                    self.rect.width,
                    self.rect.height,
                ).colliderect(planr.rect):
                    self.collide = True
                    break
            if not self.collide:
                self.walkindex += 0.1 / (self.snow + 1)
                walkblit = int(self.walkindex % len(rugbynohead_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + rugbynohead_frame0[self.snow][walkblit].get_height()
                )
                screen.blit(
                    rugbynohead_frame0[self.snow][walkblit],
                    (
                        self.rect.x
                        - camera[0]
                        + (160 - rugbynohead_frame0[self.snow][walkblit].get_width()),
                        self.rect.y - camera[1],
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            else:
                self.noheadeatindex += 0.1 / (self.snow + 1)
                noheadeatblit = int(
                    self.noheadeatindex % len(rugbynoheadeat_frame0[self.snow])
                )
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y
                    + rugbynoheadeat_frame0[self.snow][noheadeatblit].get_height()
                )
                screen.blit(
                    rugbynoheadeat_frame0[self.snow][noheadeatblit],
                    (
                        self.rect.x
                        - camera[0]
                        + (
                            160
                            - rugbynoheadeat_frame0[self.snow][
                                noheadeatblit
                            ].get_width()
                        ),
                        self.rect.y - camera[1],
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            if self.HP <= 0:
                self.style = 8
        elif self.style == 8:  # 尸体倒下
            self.fallindex += 0.1 / (self.snow + 1)
            fallblit = int(self.fallindex)
            if fallblit < len(rugbyfall_frame0[self.snow]):
                rect = rugbyfall_frame0[self.snow][fallblit].get_rect()
                screen.blit(
                    rugbyfall_frame0[self.snow][fallblit],
                    (
                        self.rect.x - camera[0] - rect.width + self.rect.width - 10,
                        self.rect.y - camera[1] - rect.height + self.rect.height - 22,
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            elif fallblit >= len(rugbyfall_frame0[self.snow]):
                emg.zombie_list.remove(self)
                self.kill()
        elif self.style == 9:  # 尸体倒下后消失
            emg.zombie_list.remove(self)
            self.kill()
        elif self.style == 10:  # 吃植物
            if self.HP > 500 and not self.hit:
                self.eatindex += 0.2 / (self.snow + 1)
                eatblit = int(self.eatindex % len(rugbyeat_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + rugbyeat_frame0[self.snow][eatblit].get_height()
                )
                screen.blit(
                    rugbyeat_frame0[self.snow][eatblit],
                    (
                        self.rect.x
                        - camera[0]
                        + (160 - rugbyeat_frame0[self.snow][eatblit].get_width()),
                        self.rect.y - camera[1],
                    ),
                )
                if not pygame.Rect(
                    player.rect.x
                    - camera[0]
                    + (80 - rugbyeat_frame0[self.snow][eatblit].get_width()),
                    player.rect.y - camera[1],
                    player.rect.width,
                    player.rect.height,
                ).colliderect(
                    pygame.Rect(
                        self.rect.x
                        - camera[0]
                        + (160 - rugbyeat_frame0[self.snow][eatblit].get_width()),
                        self.rect.y - camera[1],
                        self.rect.width // 2,
                        self.rect.height // 2,
                    )
                ):
                    self.style = 0
                    self.eating = False
            elif self.HP > 500 and self.hit:
                self.eatindex += 0.2 / (self.snow + 1)
                eatblit = int(self.eatindex % len(rugbyeat_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + rugbyeat_frame0[self.snow][eatblit].get_height()
                )
                story = copy.copy(rugbyeat_frame0[self.snow][eatblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (160 - rugbyeat_frame0[self.snow][eatblit].get_width()),
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.hit = False
            elif self.HP > 120 and not self.hit:
                self.eatindex += 0.2 / (self.snow + 1)
                eatblit = int(self.eatindex % len(rugbynocapeat_frame0[self.snow]))
                screen.blit(
                    rugbynocapeat_frame0[self.snow][eatblit],
                    (
                        self.rect.x
                        - camera[0]
                        + (160 - rugbynocapeat_frame0[self.snow][eatblit].get_width()),
                        self.rect.y - camera[1],
                    ),
                )
                if not pygame.Rect(
                    player.rect.x
                    - camera[0]
                    + (80 - rugbynocapeat_frame0[self.snow][eatblit].get_width()),
                    player.rect.y - camera[1] - (player.rect.width - 65),
                    player.rect.width,
                    player.rect.height,
                ).colliderect(
                    pygame.Rect(
                        self.rect.x
                        - camera[0]
                        + (160 - rugbynocapeat_frame0[self.snow][eatblit].get_width()),
                        self.rect.y - camera[1],
                        self.rect.width // 2,
                        self.rect.height // 2,
                    )
                ):
                    self.style = 11
                    self.eating = False
            elif self.HP > 120 and self.hit:
                self.eatindex += 0.2 / (self.snow + 1)
                eatblit = int(self.eatindex % len(rugbynocapeat_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + rugbynocapeat_frame0[self.snow][eatblit].get_height()
                )
                story = copy.copy(rugbynocapeat_frame0[self.snow][eatblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (
                                160
                                - rugbynocapeat_frame0[self.snow][eatblit].get_width()
                            ),
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.hit = False
            else:
                self.style = 7
        elif self.style == 11:  # 掉帽子行走
            self.walkindex += 0.1 / (self.snow + 1)
            walkblit = int(self.walkindex % len(rugbynocap_frame0[self.snow]))
            self.rect.x = self.x
            self.rect.y = screen_height - (
                self.y + rugbynocap_frame0[self.snow][walkblit].get_height()
            )
            screen.blit(
                rugbynocap_frame0[self.snow][walkblit],
                (
                    self.rect.x
                    - camera[0]
                    + (160 - rugbynocap_frame0[self.snow][walkblit].get_width()),
                    self.rect.y - camera[1],
                    self.rect.width,
                    self.rect.height,
                ),
            )
        if self.HP <= 120:
            if self.dealing < 1:
                self.falltemp = (self.rect.x + 20, self.rect.y + 10)
                self.dealing = 1
            self.headindex += 0.4 / (self.snow + 1)
            headblit = int(self.headindex)
            if headblit < len(head_frame):
                head = Fallthing(
                    head_frame0[self.snow][headblit],
                    self.falltemp[0] + f(self.headindex),
                    self.falltemp[1] + g(self.headindex, 0.5),
                    50,
                    50,
                )
                head.draw(camera)
            if self.money >= 96:  # diamond
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)
                    audio_player.play_sound("产生钻石", 0, 0.5)
                self.moneyindex += 0.2
                moneyblit = int(self.moneyindex % 5) + 4
                if self.moneyindex < 15:
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        self.falltemp[0] - f(self.moneyindex),
                        self.falltemp[1] + g(self.moneyindex, 0.5),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 20:
                    x = self.falltemp[0] - f(15) + camera[0]
                    y = self.falltemp[1] + g(15, 0.5) + camera[1]
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        x - h(self.moneyindex - 15, self.falltemp[0] - 30),
                        y + h(self.moneyindex - 15, 630 - self.falltemp[1]),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 25:
                    player_money.add_money(1000)
                    self.moneyindex = 114514
                else:
                    pass
            elif self.money < 96 and self.money >= 85:  # goldcoin
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)
                    audio_player.play_sound("产生币", 0, 0.5)
                self.moneyindex += 0.2
                moneyblit = int(self.moneyindex % 2) + 2
                if self.moneyindex < 15:
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        self.falltemp[0] - f(self.moneyindex),
                        self.falltemp[1] + g(self.moneyindex, 0.5),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 20:
                    x = self.falltemp[0] - f(15) + camera[0]
                    y = self.falltemp[1] + g(15, 0.5) + camera[1]
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        x - h(self.moneyindex - 15, self.falltemp[0] - 30),
                        y + h(self.moneyindex - 15, 610 - self.falltemp[1]),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 25:
                    player_money.add_money(50)
                    self.moneyindex = 114514
                else:
                    pass
            elif self.money < 85 and self.money >= 50:  # coin
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)
                    audio_player.play_sound("产生币", 0, 0.5)
                self.moneyindex += 0.2
                moneyblit = int(self.moneyindex % 2)
                if self.moneyindex < 15:
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        self.falltemp[0] - f(self.moneyindex),
                        self.falltemp[1] + g(self.moneyindex, 0.5),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 20:
                    x = self.falltemp[0] - f(15) + camera[0]
                    y = self.falltemp[1] + g(15, 0.5) + camera[1]
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        x - h(self.moneyindex - 15, self.falltemp[0] - 30),
                        y + h(self.moneyindex - 15, 610 - self.falltemp[1]),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 25:
                    player_money.add_money(10)
                    self.moneyindex = 114514
            else:
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)

    def move(self, default=0):
        if (
            self.style != 9
            and not (self.style == 3 and self.eating)
            and self.style != 10
            and self.style != 1
        ):
            self.x -= self.move_speed / (self.snow + 1) + default

    def is_fall(self):
        if self.HP <= 0:
            self.style = 8
            return True
        else:
            return False

    def is_end(self):
        if self.x <= 50 and (self.style == 0 or self.style == 11):
            if self.HP > 500:
                self.style = 1
            else:
                self.style = 11
            return True
        else:
            return False


class Flag_Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.style = 0
        self.x = x
        self.y = y
        self.HP = 270
        self.move_speed = random.uniform(0.3, 0.5)
        self.walkindex = 0
        self.headindex = 0
        self.fallindex = 0
        self.eatindex = 0
        self.noheadeatindex = 0
        self.moneyindex = 0
        self.image = pygame.image.load(
            "images/旗帜僵尸/旗帜僵尸图层-1.png"
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.n = 0
        self.dealing = 0
        self.eating = False
        self.hit = False
        self.collide = False
        self.money = random.randint(0, 100)
        self.tag = 5
        self.force = 1
        self.snowcount = 0
        self.snow = 0
        self.falltemp = (self.rect.x, self.rect.y)
        self.dealing1 = 0

    def draw(self, camera):
        if self.snowcount > 0:
            self.snowcount -= 1
            self.snow = 1
        else:
            self.snow = 0
        if self.style == 0 or self.style == 1:  # 正常移动
            self.walkindex += 0.1 / (self.snow + 1)
            walkblit = int(self.walkindex % len(flag_frame0[self.snow]))
            self.rect.x = self.x
            self.rect.y = screen_height - (
                self.y + flag_frame0[self.snow][walkblit].get_height()
            )
            screen.blit(
                flag_frame0[self.snow][walkblit],
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
                    self.collide = True
                    break
            if self.HP > 70 and not self.eating:
                self.walkindex += 0.1 / (self.snow + 1)
                walkblit = int(self.walkindex % len(flag_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + flag_frame0[self.snow][walkblit].get_height()
                )
                story = copy.copy(flag_frame0[self.snow][walkblit])
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
                self.walkindex += 0.1 / (self.snow + 1)
                walkblit = int(self.walkindex % len(flagnohead_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + flagnohead_frame0[self.snow][walkblit].get_height()
                )
                story = copy.copy(flagnohead_frame0[self.snow][walkblit])
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
                self.eatindex += 0.3 / (self.snow + 1)
                eatblit = int(self.eatindex % len(flageat_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + flageat_frame0[self.snow][eatblit].get_height()
                )
                story = copy.copy(flageat_frame0[self.snow][eatblit])
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
                self.noheadeatindex += 0.3 / (self.snow + 1)
                noheadeatblit = int(
                    self.noheadeatindex % len(flagnoheadeat_frame0[self.snow])
                )
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + flagnoheadeat_frame0[self.snow][noheadeatblit].get_height()
                )
                story = copy.copy(flagnoheadeat_frame0[self.snow][noheadeatblit])
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
            self.walkindex += 0.1 / (self.snow + 1)
            walkblit = int(self.walkindex % len(flag_frame0[self.snow]))
            self.y = screen_height - (
                self.y + flag_frame0[self.snow][walkblit].get_height()
            )
            screen.blit(
                flag_frame0[self.snow][walkblit],
                (self.x - camera[0], self.y - camera[1]),
            )
        elif self.style == 6:  # 失败未进家但吃完脑子
            story = copy.copy(self.image)
            screen.blit(
                changecolor(story, 0.5, 0.5, 0, 5),
                (self.rect.x - camera[0], self.rect.y - camera[1]),
            )
        elif self.style == 7:  # 无头行走
            self.HP -= 0.6
            for planr in plant_list:
                if self.rect.colliderect(planr.rect):
                    self.collide = True
                    break
            if not self.collide:
                self.walkindex += 0.1 / (self.snow + 1)
                walkblit = int(self.walkindex % len(flagnohead_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + flagnohead_frame0[self.snow][walkblit].get_height()
                )
                screen.blit(
                    flagnohead_frame0[self.snow][walkblit],
                    (
                        self.rect.x - camera[0],
                        self.rect.y - camera[1],
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            else:
                self.noheadeatindex += 0.3 / (self.snow + 1)
                noheadeatblit = int(
                    self.noheadeatindex % len(flagnoheadeat_frame0[self.snow])
                )
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + flagnoheadeat_frame0[self.snow][noheadeatblit].get_height()
                )
                screen.blit(
                    flagnoheadeat_frame0[self.snow][noheadeatblit],
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
            self.fallindex += 0.2 / (self.snow + 1)
            fallblit = int(self.fallindex)
            if fallblit < len(cjsfall_frame0[self.snow]):
                rect = cjsfall_frame0[self.snow][fallblit].get_rect()
                screen.blit(
                    cjsfall_frame0[self.snow][fallblit],
                    (
                        self.rect.x - camera[0] - rect.width + self.rect.width - 10,
                        self.rect.y - camera[1] - rect.height + self.rect.height - 22,
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            elif fallblit >= len(cjsfall_frame0[self.snow]):
                emg.zombie_list.remove(self)
                self.kill()
        elif self.style == 9:  # 尸体倒下后消失
            emg.zombie_list.remove(self)
            self.kill()
        elif self.style == 10:  # 吃植物
            if self.HP > 70 and not self.hit:
                self.eatindex += 0.3 / (self.snow + 1)
                eatblit = int(self.eatindex % len(flageat_frame0[self.snow]))
                screen.blit(
                    flageat_frame0[self.snow][eatblit],
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
                    self.eating = False
            elif self.HP > 70 and self.hit:
                self.eatindex += 0.3 / (self.snow + 1)
                eatblit = int(self.eatindex % len(flageat_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + flageat_frame0[self.snow][eatblit].get_height()
                )
                story = copy.copy(flageat_frame0[self.snow][eatblit])
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
                    self.hit = False
        if self.HP <= 70:
            if self.dealing < 1:
                self.falltemp = (self.rect.x, self.rect.y)
                self.dealing = 1
            self.headindex += 0.2 / (self.snow + 1)
            headblit = int(self.headindex)
            if headblit < len(head_frame):
                head = Fallthing(
                    head_frame[headblit],
                    self.falltemp[0] + f(self.headindex),
                    self.falltemp[1] + g(self.headindex, 0.5),
                    50,
                    50,
                )
                head.draw(camera)
            if self.money >= 99:  # diamond
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)
                    audio_player.play_sound("产生钻石", 0, 0.5)
                self.moneyindex += 0.2
                moneyblit = int(self.moneyindex % 5) + 4
                if self.moneyindex < 15:
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        self.falltemp[0] - f(self.moneyindex),
                        self.falltemp[1] + g(self.moneyindex, 0.5),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 20:
                    x = self.falltemp[0] - f(15) + camera[0]
                    y = self.falltemp[1] + g(15, 0.5) + camera[1]
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        x - h(self.moneyindex - 15, self.falltemp[0] - 30),
                        y + h(self.moneyindex - 15, 630 - self.falltemp[1]),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 25:
                    player_money.add_money(1000)
                    self.moneyindex = 114514
                else:
                    pass
            elif self.money < 99 and self.money >= 94:  # goldcoin
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)
                    audio_player.play_sound("产生币", 0, 0.5)
                self.moneyindex += 0.2
                moneyblit = int(self.moneyindex % 2) + 2
                if self.moneyindex < 15:
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        self.falltemp[0] - f(self.moneyindex),
                        self.falltemp[1] + g(self.moneyindex, 0.5),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 20:
                    x = self.falltemp[0] - f(15) + camera[0]
                    y = self.falltemp[1] + g(15, 0.5) + camera[1]
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        x - h(self.moneyindex - 15, self.falltemp[0] - 30),
                        y + h(self.moneyindex - 15, 610 - self.falltemp[1]),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 25:
                    player_money.add_money(50)
                    self.moneyindex = 114514
                else:
                    pass
            elif self.money < 94 and self.money >= 75:  # coin
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)
                    audio_player.play_sound("产生币", 0, 0.5)
                self.moneyindex += 0.2
                moneyblit = int(self.moneyindex % 2)
                if self.moneyindex < 15:
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        self.falltemp[0] - f(self.moneyindex),
                        self.falltemp[1] + g(self.moneyindex, 0.5),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 20:
                    x = self.falltemp[0] - f(15) + camera[0]
                    y = self.falltemp[1] + g(15, 0.5) + camera[1]
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        x - h(self.moneyindex - 15, self.falltemp[0] - 30),
                        y + h(self.moneyindex - 15, 610 - self.falltemp[1]),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 25:
                    player_money.add_money(10)
                    self.moneyindex = 114514
            else:
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)

    def move(self, default=0):
        if self.style != 9 and not (self.style == 3 and self.eating):
            self.x -= self.move_speed / (self.snow + 1) + default

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


class Paper_Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = erye_frame[0]
        self.image2 = eryeangry_frame[0]
        self.style = 0
        self.x = x
        self.y = y
        self.HP = 720 + 1100
        self.move_speed = random.uniform(0.2, 0.3)
        self.walkindex = 0
        self.headindex = 0
        self.fallindex = 0
        self.paperindex = 0
        self.eatindex = 0
        self.angryeatindex = 0
        self.noheadeatindex = 0
        self.moneyindex = 0
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.n = 0
        self.dealing = 0
        self.eating = False
        self.hit = False
        self.collide = False
        self.money = random.randint(0, 100)
        self.tag = 6
        self.force = 3
        self.snowcount = 0
        self.snow = 0
        self.falltemp = (self.rect.x, self.rect.y)
        self.is_fallpaper = False
        self.dealing1 = 0
        self.dealing2 = 0
        self.dealing3 = 0

    def draw(self, camera):
        if self.snowcount > 0:
            self.snowcount -= 1
            self.snow = 1
        else:
            self.snow = 0
        if self.style == 0 or self.style == 1:  # 正常移动
            self.walkindex += 0.2
            walkblit = int(self.walkindex % len(erye_frame0[0]))
            self.rect.x = self.x
            self.rect.y = screen_height - (
                self.y + erye_frame0[0][walkblit].get_height()
            )
            screen.blit(
                erye_frame0[0][walkblit],
                (
                    self.rect.x
                    - camera[0]
                    + (120 - erye_frame0[0][walkblit].get_width()),
                    self.rect.y - camera[1],
                    self.rect.width,
                    self.rect.height,
                ),
            )
        elif self.style == 3:  # 被子弹击中
            for plans in plant_list:
                if pygame.Rect(
                    self.rect.x + 30,
                    self.rect.y + 30,
                    self.rect.width / 3,
                    self.rect.height / 3,
                ).colliderect(plans.rect):
                    self.collide = True
                    break
            if self.HP > 720 and not self.eating:
                self.walkindex += 0.2
                walkblit = int(self.walkindex % len(erye_frame0[0]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + erye_frame0[0][walkblit].get_height()
                )
                story = copy.copy(erye_frame0[0][walkblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (120 - erye_frame0[0][walkblit].get_width()),
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 0

            elif self.HP <= 720 and self.HP > 120 and not self.eating:
                self.walkindex += 0.8 / (self.snow + 1)
                walkblit = int(self.walkindex % len(eryeangry_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + eryeangry_frame0[self.snow][walkblit].get_height()
                )
                story = copy.copy(eryeangry_frame0[self.snow][walkblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (120 - eryeangry_frame0[self.snow][walkblit].get_width()),
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 11  # need change
            elif self.HP <= 120 and self.HP > 0 and not self.collide:
                self.walkindex += 0.8 / (self.snow + 1)
                walkblit = int(self.walkindex % len(eryenohead_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + eryenohead_frame0[self.snow][walkblit].get_height()
                )
                story = copy.copy(eryenohead_frame0[self.snow][walkblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (
                                120 - eryenohead_frame0[self.snow][walkblit].get_width()
                            ),
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 7
            elif self.HP > 720 and self.eating:
                self.eatindex += 0.2
                eatblit = int(self.eatindex % len(eryeeat_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + eryeeat_frame0[self.snow][eatblit].get_height()
                )
                story = copy.copy(eryeeat_frame0[self.snow][eatblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (120 - eryeeat_frame0[self.snow][eatblit].get_width()),
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 10

            elif self.HP <= 720 and self.HP > 120 and self.eating:
                self.angryeatindex += 0.8 / (self.snow + 1)
                angryeatblit = int(
                    self.angryeatindex % len(eryeangryeat_frame0[self.snow])
                )
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + eryeangryeat_frame0[self.snow][angryeatblit].get_height()
                )
                story = copy.copy(eryeangryeat_frame0[self.snow][angryeatblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (
                                120
                                - eryeangryeat_frame0[self.snow][
                                    angryeatblit
                                ].get_width()
                            ),
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.style = 10  # need change

            elif self.HP <= 120 and self.HP > 0 and self.collide:
                self.noheadeatindex += 0.8 / (self.snow + 1)
                noheadeatblit = int(
                    self.noheadeatindex % len(eryenoheadeat_frame0[self.snow])
                )
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + eryenoheadeat_frame0[self.snow][noheadeatblit].get_height()
                )
                story = copy.copy(eryenoheadeat_frame0[self.snow][noheadeatblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (
                                160
                                - rugbynoheadeat_frame0[self.snow][
                                    noheadeatblit
                                ].get_width()
                            ),
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
            if self.HP > 720:
                self.rect.x = self.x
                self.rect.y = screen_height - (self.y + self.image.get_height())
                screen.blit(
                    self.image, (self.rect.x - camera[0], self.rect.y - camera[1])
                )
            else:
                self.rect.x = self.x
                self.rect.y = screen_height - (self.y + self.image2.get_height())
                screen.blit(
                    self.image2, (self.rect.x - camera[0], self.rect.y - camera[1])
                )

        elif self.style == 5:  # 失败进家
            self.y = 200
            self.rect.x = self.x
            if self.HP > 720:
                self.walkindex += 0.1
                walkblit = int(self.walkindex % len(erye_frame0[self.snow]))
            else:
                self.walkindex += 0.8 / (self.snow + 1)
                walkblit = int(self.walkindex % len(eryeangry_frame0[self.snow]))
            self.y = screen_height - (
                self.y + erye_frame0[self.snow][walkblit].get_height()
            )
            if self.HP > 720:
                screen.blit(
                    erye_frame0[0][walkblit],
                    (self.x - camera[0], self.y - camera[1]),
                )
                self.image = erye_frame0[0][walkblit]
            else:
                screen.blit(
                    eryeangry_frame0[self.snow][walkblit],
                    (self.x - camera[0], self.y - camera[1]),
                )
                self.image2 = eryeangry_frame0[self.snow][walkblit]
        elif self.style == 6:  # 失败未进家但吃完脑子
            if self.dealing == 0:
                if self.HP > 720:
                    self.image = changecolor(self.image, 0.6, 0.6, 0.6)
                else:
                    self.image2 = changecolor(self.image2, 0.6, 0.6, 0.6)
                self.dealing = 1
            if self.HP > 720:
                screen.blit(
                    self.image, (self.rect.x - camera[0], self.rect.y - camera[1])
                )
            elif self.HP > 120 and self.HP <= 720:
                screen.blit(
                    self.image2, (self.rect.x - camera[0], self.rect.y - camera[1])
                )
        elif self.style == 7:  # 无头行走
            self.HP -= 0.5
            for planr in plant_list:
                if pygame.Rect(
                    self.rect.x
                    - camera[0]
                    + (120 - eryenohead_frame0[self.snow][0].get_width()),
                    self.rect.y - camera[1],
                    self.rect.width,
                    self.rect.height,
                ).colliderect(planr.rect):
                    self.collide = True
                    break
            if not self.collide:
                self.walkindex += 0.8 / (self.snow + 1)
                walkblit = int(self.walkindex % len(eryenohead_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + eryenohead_frame0[self.snow][walkblit].get_height()
                )
                screen.blit(
                    eryenohead_frame0[self.snow][walkblit],
                    (
                        self.rect.x
                        - camera[0]
                        + (120 - eryenohead_frame0[self.snow][walkblit].get_width()),
                        self.rect.y - camera[1],
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            else:
                self.noheadeatindex += 0.8 / (self.snow + 1)
                noheadeatblit = int(
                    self.noheadeatindex % len(eryenoheadeat_frame0[self.snow])
                )
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + eryenoheadeat_frame0[self.snow][noheadeatblit].get_height()
                )
                screen.blit(
                    eryenoheadeat_frame0[self.snow][noheadeatblit],
                    (
                        self.rect.x
                        - camera[0]
                        + (
                            120
                            - eryenoheadeat_frame0[self.snow][noheadeatblit].get_width()
                        ),
                        self.rect.y - camera[1],
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            if self.HP <= 0:
                self.style = 8
        elif self.style == 8:  # 尸体倒下
            self.fallindex += 0.1 / (self.snow + 1)
            fallblit = int(self.fallindex)
            if fallblit < len(eryefall_frame0[self.snow]):
                rect = eryefall_frame0[self.snow][fallblit].get_rect()
                screen.blit(
                    eryefall_frame0[self.snow][fallblit],
                    (
                        self.rect.x - camera[0] - rect.width + self.rect.width - 10,
                        self.rect.y - camera[1] - rect.height + self.rect.height - 22,
                        self.rect.width,
                        self.rect.height,
                    ),
                )
            elif fallblit >= len(eryefall_frame0[self.snow]):
                emg.zombie_list.remove(self)
                self.kill()
        elif self.style == 9:  # 尸体倒下后消失
            emg.zombie_list.remove(self)
            self.kill()
        elif self.style == 10:  # 吃植物
            if self.HP > 720 and not self.hit:
                self.eatindex += 0.2
                eatblit = int(self.eatindex % len(eryeeat_frame0[0]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + eryeeat_frame0[0][eatblit].get_height()
                )
                screen.blit(
                    eryeeat_frame0[self.snow][eatblit],
                    (
                        self.rect.x
                        - camera[0]
                        + (120 - eryeeat_frame0[0][eatblit].get_width()),
                        self.rect.y - camera[1],
                    ),
                )
                if not pygame.Rect(
                    player.rect.x
                    - camera[0]
                    + (60 - eryeeat_frame0[0][eatblit].get_width()),
                    player.rect.y - camera[1] - 10,
                    player.rect.width,
                    player.rect.height,
                ).colliderect(
                    pygame.Rect(
                        self.rect.x
                        - camera[0]
                        + (120 - eryeeat_frame0[0][eatblit].get_width()),
                        self.rect.y - camera[1],
                        self.rect.width // 2,
                        self.rect.height // 2,
                    )
                ):
                    self.style = 0
                    self.eating = False
            elif self.HP > 720 and self.hit:
                self.eatindex += 0.2
                eatblit = int(self.eatindex % len(eryeeat_frame0[0]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + eryeeat_frame0[0][eatblit].get_height()
                )
                story = copy.copy(eryeeat_frame0[0][eatblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (120 - eryeeat_frame0[0][eatblit].get_width()),
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.hit = False
            elif self.HP > 120 and not self.hit:
                self.eatindex += 0.8 / (self.snow + 1)
                eatblit = int(self.eatindex % len(eryeangryeat_frame0[self.snow]))
                screen.blit(
                    eryeangryeat_frame0[self.snow][eatblit],
                    (
                        self.rect.x
                        - camera[0]
                        + (120 - eryeangryeat_frame0[self.snow][eatblit].get_width()),
                        self.rect.y
                        - camera[1]
                        + (140 - eryeangryeat_frame0[self.snow][eatblit].get_height()),
                    ),
                )
                if not pygame.Rect(
                    player.rect.x
                    - camera[0]
                    + (60 - eryeangryeat_frame0[self.snow][eatblit].get_width()),
                    player.rect.y - camera[1] - (player.rect.width - 65) - 10,
                    player.rect.width,
                    player.rect.height,
                ).colliderect(
                    pygame.Rect(
                        self.rect.x
                        - camera[0]
                        + (120 - eryeangryeat_frame0[self.snow][eatblit].get_width()),
                        self.rect.y
                        - camera[1]
                        + (140 - eryeangryeat_frame0[self.snow][eatblit].get_height()),
                        self.rect.width // 2,
                        self.rect.height // 2,
                    )
                ):
                    self.style = 11
                    self.eating = False
            elif self.HP > 120 and self.hit:
                self.eatindex += 0.8 / (self.snow + 1)
                eatblit = int(self.eatindex % len(eryeangryeat_frame0[self.snow]))
                self.rect.x = self.x
                self.rect.y = screen_height - (
                    self.y + eryeangryeat_frame0[self.snow][eatblit].get_height()
                )
                story = copy.copy(eryeangryeat_frame0[self.snow][eatblit])
                if self.n < 3:
                    self.n += 1
                    screen.blit(
                        changecolor(story, 1.6, 1.6, 1.6),
                        (
                            self.rect.x
                            - camera[0]
                            + (
                                120
                                - eryeangryeat_frame0[self.snow][eatblit].get_width()
                            ),
                            self.rect.y - camera[1],
                            self.rect.width,
                            self.rect.height,
                        ),
                    )
                if self.n == 3:
                    self.n = 0
                    self.hit = False
            else:
                self.style = 7
        elif self.style == 11:  # 生气行走
            if self.dealing2 == 0:
                audio_player.play_sound("二爷生气2", 0, 0.5)
                self.dealing2 = 1
            self.walkindex += 0.8 / (self.snow + 1)
            walkblit = int(self.walkindex % len(eryeangry_frame0[self.snow]))
            self.rect.x = self.x
            self.rect.y = screen_height - (
                self.y + eryeangry_frame0[self.snow][walkblit].get_height()
            )
            screen.blit(
                eryeangry_frame0[self.snow][walkblit],
                (
                    self.rect.x
                    - camera[0]
                    + (120 - eryeangry_frame0[self.snow][walkblit].get_width()),
                    self.rect.y - camera[1],
                    self.rect.width,
                    self.rect.height,
                ),
            )
        elif self.style == 12:  # 掉报纸
            if self.dealing3 == 0:
                audio_player.play_sound("报纸破碎", 0, 0.5)
                self.dealing3 = 1
            self.HP = 720
            self.paperindex += 0.2 / (self.snow + 1)
            paperblit = int(self.paperindex)
            if paperblit < len(eryelosepaper_frame0[self.snow]):
                screen.blit(
                    eryelosepaper_frame0[self.snow][paperblit],
                    (
                        self.rect.x - camera[0],
                        self.rect.y
                        - camera[1]
                        + (
                            140
                            - eryelosepaper_frame0[self.snow][paperblit].get_height()
                        ),
                    ),
                )
            else:
                self.style = 11
        if self.HP <= 120:
            if self.dealing < 1:
                self.falltemp = (self.rect.x + 20, self.rect.y + 10)
                self.dealing = 1
            self.headindex += 0.4 / (self.snow + 1)
            headblit = int(self.headindex)
            if headblit < len(head_frame):
                head = Fallthing(
                    head_frame0[self.snow][headblit],
                    self.falltemp[0] + f(self.headindex),
                    self.falltemp[1] + g(self.headindex, 0.5),
                    50,
                    50,
                )
                head.draw(camera)
            if self.money >= 96:  # diamond
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)
                    audio_player.play_sound("产生钻石", 0, 0.5)
                self.moneyindex += 0.2
                moneyblit = int(self.moneyindex % 5) + 4
                if self.moneyindex < 15:
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        self.falltemp[0] - f(self.moneyindex),
                        self.falltemp[1] + g(self.moneyindex, 0.5),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 20:
                    x = self.falltemp[0] - f(15) + camera[0]
                    y = self.falltemp[1] + g(15, 0.5) + camera[1]
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        x - h(self.moneyindex - 15, self.falltemp[0] - 30),
                        y + h(self.moneyindex - 15, 630 - self.falltemp[1]),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 25:
                    player_money.add_money(1000)
                    self.moneyindex = 114514
                else:
                    pass
            elif self.money < 96 and self.money >= 85:  # goldcoin
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)
                    audio_player.play_sound("产生币", 0, 0.5)
                self.moneyindex += 0.2
                moneyblit = int(self.moneyindex % 2) + 2
                if self.moneyindex < 15:
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        self.falltemp[0] - f(self.moneyindex),
                        self.falltemp[1] + g(self.moneyindex, 0.5),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 20:
                    x = self.falltemp[0] - f(15) + camera[0]
                    y = self.falltemp[1] + g(15, 0.5) + camera[1]
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        x - h(self.moneyindex - 15, self.falltemp[0] - 30),
                        y + h(self.moneyindex - 15, 610 - self.falltemp[1]),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 25:
                    player_money.add_money(50)
                    self.moneyindex = 114514
                else:
                    pass
            elif self.money < 85 and self.money >= 50:  # coin
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)
                    audio_player.play_sound("产生币", 0, 0.5)
                self.moneyindex += 0.2
                moneyblit = int(self.moneyindex % 2)
                if self.moneyindex < 15:
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        self.falltemp[0] - f(self.moneyindex),
                        self.falltemp[1] + g(self.moneyindex, 0.5),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 20:
                    x = self.falltemp[0] - f(15) + camera[0]
                    y = self.falltemp[1] + g(15, 0.5) + camera[1]
                    diamond = Fallthing(
                        money_frame[moneyblit],
                        x - h(self.moneyindex - 15, self.falltemp[0] - 30),
                        y + h(self.moneyindex - 15, 610 - self.falltemp[1]),
                        40,
                        40,
                    )
                    diamond.draw(camera)
                elif self.moneyindex < 25:
                    player_money.add_money(10)
                    self.moneyindex = 114514
            else:
                if self.dealing1 == 0:
                    self.dealing1 = 1
                    audio_player.play_sound("头掉了", 0, 0.3)

    def move(self, default=0):
        if (
            self.style != 9
            and self.style != 1
            and self.style != 12
            and not (self.style == 3 and self.eating)
        ):
            if self.HP > 720:
                self.x -= self.move_speed + default
            elif self.HP > 0:
                self.x -= self.move_speed * 8 / (self.snow + 1) + default

    def is_fall(self):
        if self.HP <= 0:
            self.style = 8
            return True
        else:
            return False

    def is_end(self):
        if self.x <= 50 and (self.style == 0 or self.style == 11):
            if self.HP > 720:
                self.style = 1
            if self.HP <= 720:
                self.style = 11
            return True
        else:
            return False

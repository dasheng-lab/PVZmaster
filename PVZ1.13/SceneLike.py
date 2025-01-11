import pygame
import random
import sys
import time
import copy
from Event import *
from Creature import *
from Talk import *
from Battle import *
from Music import *
from Resources import *


def mouse():
    cursor_image_path = "images/OIP-C (1).png"
    cursor_image = pygame.image.load(cursor_image_path).convert_alpha()
    cursor_image = pygame.transform.scale(
        cursor_image, (cursor_image.get_width(), cursor_image.get_height())
    )
    cursor_size = cursor_image.get_size()
    cursor_surface = pygame.Surface(cursor_size, pygame.SRCALPHA)
    cursor_surface.blit(cursor_image, (0, 0))
    hotspot_x = cursor_size[0] // 2
    hotspot_y = cursor_size[1] // 2
    custom_cursor = pygame.cursors.Cursor((hotspot_x, hotspot_y), cursor_surface)
    pygame.mouse.set_cursor(custom_cursor)


class SceneLike(Listener):  # 场景的类，管理障碍物、角色、地图背景的描绘、刷新等

    def __init__(self, player, style=0, x=0, y=0):
        super().__init__()
        self.player = player  # 传递玩家的实例
        self.window_scale = (1000, 800)  # 显示窗口的大小
        self.map_range = (1500, 1000)  # 实际地图的大小
        self.carema = [0, 0]  # 镜头的初始位置
        self.carema1 = [0, 0]
        self.carema2 = [0, 0]
        self.style = style
        self.image = picture_list[style]
        self.rect = self.image.get_rect()
        self.battle_staus = 0
        self.level = 0
        self.ji = 0
        self.talk_staus = 0
        self.object = 0
        self.inout = 0
        self.judge = [0, 0]
        self.status = 0
        self.text = ""
        self.status1 = 0
        self.Pause = False
        self.reasontime = 0
        self.reasonpause = 0
        self.cheat = False
        self.goods = []
        self.counterror = 0
        self.buy = 0
        self.wincount = 0
        self.dealing = 0

    def listen(self, event: Event):  # 场景所监听的事件
        super().listen(event)
        self.Pause = pausemanager.pause
        button_15.is_draw = False
        if event.code == Event_kind.REQUEST_MOVE:  # 监听玩家的移动请求事件
            can_move = 1  # 一开始默认可以移动
            if can_move:  # 如果可以移动的话就发送允许移动事件
                self.post(Event(Event_kind.CAN_MOVE, event.body))

        if event.code == Event_kind.DRAW:
            # DRAW是每次游戏周期刷新时会被触发的事件
            if not self.Pause and self.style == 0:
                screen.blit(self.image, self.rect)
                button_1.draw()
                audio_player.play_sound("begin")
                if button_1.is_clicked():
                    self.post(
                        Event(Event_kind.CHANGE_BAKEGROUND, {"background": 1})
                    )  # 选关界面

            if not self.Pause and self.style == 1:
                screen.blit(self.image, self.rect)
                button_2.draw()
                button_3.draw()
                button_4.draw()
                button_5.draw()
                button_6.draw()
                button_7.draw()
                if button_2.is_clicked():
                    self.post(
                        Event(
                            Event_kind.CHANGE_BAKEGROUND,
                            {
                                "background": 2,
                                "x": -2600,
                                "y": 0,
                                "play_x": 200,
                                "play_y": 370,
                            },
                        )
                    )
                    audio_player.switch_sound("begin2")
                    self.player.place = 0

                if button_3.is_clicked() or button_4.is_clicked():
                    self.post(
                        Event(
                            Event_kind.CHANGE_BAKEGROUND,
                            {"background": 3, "x": 280, "y": 170},
                        )
                    )  # 帮助
                if button_6.is_clicked():
                    self.post(
                        Event(
                            Event_kind.CHANGE_BAKEGROUND,
                            {"background": 11},
                        )
                    )
                if button_5.is_clicked():
                    self.post(
                        Event(
                            Event_kind.CHANGE_BAKEGROUND,
                            {"background": 9, "x": 250, "y": 50},
                        )
                    )
                if button_7.is_clicked():
                    pygame.quit()
                    sys.exit()

            if not self.Pause and self.style == 2:  # 室外
                self.inout = 0
                screen.blit(
                    self.image,
                    (self.rect.x - self.carema[0], self.rect.y - self.carema[1]),
                )
                self.player.draw(self.carema, self.style)  # 描绘玩家图像
                for bullet in bulletlist_right:
                    bullet.draw(self.carema)
                for bullet in bulletlist_left:
                    bullet.draw(self.carema)
                for npc in NPCs:
                    npc.draw(self.carema)
                for zombie in emg.zombie_list:
                    zombie.draw(self.carema)
                for obstacle in obstacle_list0:
                    obstacle.draw(self.carema)
                front_door.draw(self.carema)
                if front_door.is_clicked():
                    self.post(
                        Event(
                            Event_kind.CHANGE_BAKEGROUND,
                            {
                                "background": 7,
                                "x": -1000,
                                "y": 0,
                                "play_x": 880,
                                "play_y": 600,
                            },
                        )
                    )
                    self.player.place = 1
                player_money.draw()
                button_11.draw()
                if button_11.is_clicked():
                    audio_player.switch_sound("begin3")
                    self.style = 6
                    global plant_list
                    plant_list.clear()
                    card_box.sunshine = card_box.initsunshine
                text3 = font.render(f"{the_level.level}", True, (0, 0, 0))
                screen.blit(text3, (920, 15))
                if the_level.hardness == 1:
                    text4 = font.render(f"简单", True, (0, 0, 0))
                elif the_level.hardness == 1.5:
                    text4 = font.render(f"普通", True, (0, 0, 0))
                elif the_level.hardness == 2:
                    text4 = font.render(f"困难", True, (0, 0, 0))
                elif the_level.hardness == 3:
                    text4 = font.render(f"作弊", True, (0, 0, 0))
                screen.blit(text4, (940, 15))
                the_level.reset()
                emg.zombie_list.clear()
                if the_level.level >= 4 or self.cheat:
                    ladder.draw(self.carema)
                    if ladder.is_clicked():
                        self.player.place = 2
                        self.post(
                            Event(
                                Event_kind.CHANGE_BAKEGROUND,
                                {
                                    "background": 8,
                                    "x": -250,
                                    "y": 0,
                                    "play_x": 500,
                                    "play_y": 520,
                                },
                            )
                        )
            if not self.Pause and self.style == 3:  # 敬请期待
                screen.blit(self.image, self.rect)
                button_8.draw()
                if button_8.is_clicked():
                    self.post(Event(Event_kind.CHANGE_BAKEGROUND, {"background": 1}))
                pygame.display.update()

            if not self.Pause and self.style == 4:  # 失败
                go2 = pygame.image.load("images/gameover2.png")
                go2 = pygame.transform.scale(go2, (400, 320))
                screen.blit(go2, (280, 170))
                restart.draw()
                button_15.draw()
                if restart.is_clicked():
                    self.ji = 0
                    self.post(
                        Event(Event_kind.RESTART, {"background": 2, "x": -2600, "y": 0})
                    )
                    player.hp = player.besthp
                    global lawn_avaible
                    for lawn in lawn_avaible.keys():
                        lawn_avaible[lawn] = True

            if self.style == 5 and not self.Pause:  # 对话界面
                screen.blit(self.image, self.rect)
                button_15.draw()
                if buttontalk_1.is_clicked():
                    talk1.update()
                    if self.player.place == 0:
                        self.post(
                            Event(
                                Event_kind.CHANGE_BAKEGROUND,
                                {"background": 2, "x": -2600, "y": 0},
                            )
                        )
                    elif self.player.place == 1:
                        self.post(
                            Event(
                                Event_kind.CHANGE_BAKEGROUND,
                                {"background": 7, "x": -1000, "y": 0},
                            )
                        )
                    elif self.player.place == 2:
                        self.post(
                            Event(
                                Event_kind.CHANGE_BAKEGROUND,
                                {"background": 8, "x": -250, "y": 0},
                            )
                        )
                if self.talk_staus == 0:
                    if buttontalk_2.is_clicked():
                        talk1.gen_text(self.object, self.talk_staus)  #
                    talk1.create_talk(self.object)  #
                    if buttontalk_3.is_clicked():
                        talk1.update()
                        self.talk_staus = 2
                if self.talk_staus == 2:
                    if button_10.is_clicked():
                        self.talk_staus = 0
                        talk1.update()
                    if self.object == 2:  # 戴夫
                        talk_ai.create_talk(0)
                        for event1 in pygame.event.get():
                            text1.get_text(event1)
                        text1.draw()
                        if buttontalk_2.is_clicked():
                            talk_ai.gen_text(0, self.talk_staus)
                    else:
                        talk1.create_talk(self.object)
                        if buttontalk_2.is_clicked():
                            talk1.help_text(self.object, self.talk_staus)
                buttontalk_1.draw()
                buttontalk_2.draw()
                if self.talk_staus != 2:
                    buttontalk_3.draw()
                else:
                    button_10.draw()

            if not self.Pause and self.style == 6:  # 战斗界面
                screen.blit(
                    self.image,
                    (self.rect.x - self.carema[0], self.rect.y - self.carema[1]),
                )
                self.player.draw(self.carema, self.style)
                card_box.draw()
                player_money.draw()
                add_hp.draw()
                shovel.draw()
                button_15.draw()
                key_pressed = pygame.key.get_pressed()
                if (
                    shovel.is_clicked() or key_pressed[pygame.K_3]
                ) and self.reasontime % 10 == 0:
                    self.reasontime += 1
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_buttons = pygame.mouse.get_pressed()
                    audio_player.play_sound("铲子", 0, 0.6)
                    if shovel.active:
                        if mouse_buttons[0]:
                            for plantx in plant_list:
                                if plantx.rect.collidepoint(mouse_pos):
                                    plant_list.remove(plantx)
                                    for lawn in lawn_dict.keys():
                                        if (
                                            lawn_dict[lawn].x == plantx.x
                                            and lawn_dict[lawn].y == plantx.y
                                        ):
                                            lawn_avaible[lawn] = True
                                            audio_player.play_sound("铲植物", 0, 0.6)
                                    break
                    shovel.active = not shovel.active
                if self.status1 > 0:
                    textn = font.render(f"{self.text}", True, (127, 255, 127))
                    screen.blit(textn, (50, 0))
                    self.status1 -= 1
                if self.reasontime % 10 != 0:
                    self.reasontime += 1
                for plant in plant_list:
                    plant.draw(self.carema)
                for zombie in emg.zombie_list:
                    zombie.draw(self.carema)
                for obstacle in obstacle_list0:
                    obstacle.draw(self.carema)
                for bullet in bulletlist_right:
                    bullet.draw(self.carema)
                for bullet in bulletlist_left:
                    bullet.draw(self.carema)
                the_level.level_start()
            if self.style == 7 and not self.Pause:  # 房子内
                self.inout = 1
                screen.blit(
                    self.image,
                    (self.rect.x - self.carema1[0], self.rect.y - self.carema1[1]),
                )
                for bullet in bulletlist_right:
                    bullet.draw(self.carema1)
                for bullet in bulletlist_left:
                    bullet.draw(self.carema1)
                for npc in NPCs_inhouse:
                    npc.draw(self.carema1)
                for zombie in emg.zombie_list:
                    zombie.draw(self.carema1)
                for obstacle in obstacle_list1:
                    obstacle.draw(self.carema1)
                player.draw(self.carema1, self.style)  # 描绘玩家图像
                front_door1.draw(self.carema1)
                player_money.draw()
                button_15.draw()
                machine1.draw(self.carema1)
                machine2.draw(self.carema1)
                if machine1.is_clicked() or machine2.is_clicked():
                    self.post(
                        Event(
                            Event_kind.CHANGE_BAKEGROUND,
                            {"background": 10, "goods": 4},
                        )
                    )
                if not self.cheat:
                    goods_shanghai.draw(self.carema1)
                    if goods_shanghai.is_clicked():
                        self.post(
                            Event(
                                Event_kind.CHANGE_BAKEGROUND,
                                {"background": 10, "goods": 0},
                            )
                        )
                    goods_gongsu.draw(self.carema1)
                    if goods_gongsu.is_clicked():
                        self.post(
                            Event(
                                Event_kind.CHANGE_BAKEGROUND,
                                {"background": 10, "goods": 1},
                            )
                        )
                    goods_shengming.draw(self.carema1)
                    if goods_shengming.is_clicked():
                        self.post(
                            Event(
                                Event_kind.CHANGE_BAKEGROUND,
                                {"background": 10, "goods": 2},
                            )
                        )
                    goods_sudu.draw(self.carema1)
                    if goods_sudu.is_clicked():
                        self.post(
                            Event(
                                Event_kind.CHANGE_BAKEGROUND,
                                {"background": 10, "goods": 3},
                            )
                        )
                if front_door1.is_clicked():
                    self.post(
                        Event(
                            Event_kind.CHANGE_BAKEGROUND,
                            {
                                "background": 2,
                                "x": -2600,
                                "y": 0,
                                "play_x": 200,
                                "play_y": 370,
                            },
                        )
                    )
                    self.player.place = 0
                # if self.status > 0:
                # text2 = font.render(
                #    f"我还需要 {100-player_money.money} 块钱", True, (127, 255, 127)
                # )
                # screen.blit(text2, (58, 600))
                # self.status -= 1
                if self.status1 > 0:
                    textn = font.render(f"{self.text}", True, (127, 255, 127))
                    screen.blit(textn, (50, 0))
                self.status1 -= 1

            if self.style == 8 and not self.Pause:  # 楼梯
                screen.blit(self.image, (self.rect.x - self.carema2[0], self.rect.y))
                self.player.draw(self.carema2, self.style)  # 描绘玩家图像
                for bullet in bulletlist_right:
                    bullet.draw(self.carema2)
                for bullet in bulletlist_left:
                    bullet.draw(self.carema2)
                for npc in NPCs_onroof:
                    npc.draw(self.carema2)
                ladder1.draw(self.carema2)
                player_money.draw()
                button_15.draw()
                if ladder1.is_clicked():
                    self.post(
                        Event(
                            Event_kind.CHANGE_BAKEGROUND,
                            {
                                "background": 2,
                                "x": -2600,
                                "y": 0,
                                "play_x": 200,
                                "play_y": 370,
                            },
                        )
                    )
                    self.player.place = 0

            if self.style == 9 and not self.Pause:  # 难度调控
                screen.blit(main_image, (0, 0))
                if self.status1 > 0:
                    textn = font.render(f"{self.text}", True, (127, 255, 127))
                    screen.blit(textn, (50, 0))
                self.status1 -= 1
                screen.blit(self.image, self.rect)
                easy.draw()
                normal.draw()
                hard.draw()
                cheat.draw()
                button_9.draw()
                if easy.is_clicked():
                    the_level.hardness = 1
                    self.cheat = False
                    self.post(Event(Event_kind.WORDS, {"text": "简单模式开启"}))
                    self.post(Event(Event_kind.CHEAT, {"cheat": False}))
                if normal.is_clicked():
                    the_level.hardness = 1.5
                    self.cheat = False
                    self.post(Event(Event_kind.WORDS, {"text": "普通模式开启"}))
                    self.post(Event(Event_kind.CHEAT, {"cheat": False}))
                if hard.is_clicked():
                    the_level.hardness = 2
                    self.cheat = False
                    self.post(Event(Event_kind.WORDS, {"text": "困难模式开启"}))
                    self.post(Event(Event_kind.CHEAT, {"cheat": False}))
                if cheat.is_clicked():
                    the_level.hardness = 3
                    self.cheat = True
                    self.post(Event(Event_kind.WORDS, {"text": "作弊模式开启"}))
                    self.post(Event(Event_kind.CHEAT, {"cheat": True}))
                if button_9.is_clicked():
                    self.post(Event(Event_kind.CHANGE_BAKEGROUND, {"background": 1}))

            if self.style == 10 and not self.Pause:  # 商店
                screen.blit(self.image, (280, 170, 400, 320))
                goods_list[self.goods].draw()
                textn = font1.render(str_list[self.goods], True, (255, 255, 127))
                screen.blit(textn, (405, 310))
                player_money.draw()
                button_15.draw()
                if goods_list[self.goods].is_clicked():
                    if self.goods == 0:
                        if player_money.money >= 100:
                            player.beat += 3
                            player.story[3] = player.beat
                            player_money.reduce_money(100)
                            self.buy = 100
                        else:
                            self.status = 100
                    elif self.goods == 1:
                        if player_money.money >= 100:
                            player.shoot_speed /= 1.1
                            player.story[4] = player.shoot_speed
                            player_money.reduce_money(100)
                            self.buy = 100
                        else:
                            self.status = 100
                    elif self.goods == 2:
                        if player_money.money >= 100:
                            player.besthp += 50
                            player.hp += 50
                            player.story[1] = player.hp
                            player.story[2] = player.besthp
                            player_money.reduce_money(100)
                            self.buy = 100
                        else:
                            self.status = 100
                    elif self.goods == 3:
                        if player_money.money >= 100:
                            player.speed += 0.25
                            player.speed = round(player.speed, 2)
                            player.story[0] = player.speed
                            player_money.reduce_money(100)
                            self.buy = 100
                        else:
                            self.status = 100
                    elif self.goods == 4:
                        if player_money.money >= 100:
                            self.wincount = random.randint(0, 1000)
                            player_money.reduce_money(100)
                            if self.wincount >= 999:
                                player_money.money += 10000
                            self.buy = 100
                        else:
                            self.status = 100
                if self.buy > 0:
                    if self.goods == 0:
                        text = font1.render(
                            f"现伤害为{player.beat}", True, (255, 255, 127)
                        )
                        screen.blit(text, (405, 350))
                        self.buy -= 1
                    elif self.goods == 1:
                        text = font1.render(
                            f"现攻速为{80/player.beat}%", True, (255, 255, 127)
                        )
                        screen.blit(text, (405, 350))
                        self.buy -= 1
                    elif self.goods == 2:
                        text = font1.render(
                            f"现最大血量为{player.besthp}", True, (255, 255, 127)
                        )
                        screen.blit(text, (405, 350))
                        self.buy -= 1
                    elif self.goods == 3:
                        text = font1.render(
                            f"现速度为{player.speed}", True, (255, 255, 127)
                        )
                        screen.blit(text, (405, 350))
                        self.buy -= 1
                    elif self.goods == 4:
                        if self.wincount < 998:
                            text = font1.render(f"谢谢惠顾", True, (255, 255, 127))
                        else:
                            text = font1.render(
                                f"感谢您中了万元大奖", True, (255, 255, 127)
                            )
                        screen.blit(text, (405, 350))
                        self.buy -= 1
                if self.status > 0:
                    text2 = font.render(
                        f"我还需要 {100-player_money.money} 块钱",
                        True,
                        (127, 255, 127),
                    )
                    screen.blit(text2, (58, 600))
                    self.status -= 1
                button_8.draw()
                if button_8.is_clicked():
                    self.post(
                        Event(
                            Event_kind.CHANGE_BAKEGROUND,
                            {
                                "background": 7,
                                "x": -1000,
                                "y": 0,
                            },
                        )
                    )
                    self.buy = 0
            if self.style == 11 and not self.Pause:
                screen.blit(self.image, self.rect)
                button_16.draw()
                if button_16.is_clicked():
                    self.post(Event(Event_kind.CHANGE_BAKEGROUND, {"background": 1}))

        if event.code == Event_kind.STEP and not self.Pause:
            # STEP是每次游戏周期刷新时会被触发的事件
            self.counterror += 1
            if self.style == 2 or self.style == 6 or self.style == 7 or self.style == 8:
                for bullet in bulletlist_right:
                    bullet.move()
                    bullet.crash_zombie()
                for bullet in bulletlist_left:
                    bullet.move()
                    bullet.crash_zombie()
                for plant in plant_list:
                    plant.func(self.carema)
                    plant.is_eaten(self.carema)
                for lawn in lawn_dict.keys():
                    lawn_dict[lawn].update(self.carema)
                if self.counterror >= 10:
                    if self.style == 2:
                        for npc in NPCs:
                            npc.is_clicked()
                    if self.style == 7:  #
                        for npc in NPCs_inhouse:  #
                            npc.is_clicked()
                    if self.style == 6:
                        card_box.is_clicked()
                        card_box.grow()
                    if self.style == 8:
                        for npc in NPCs_onroof:
                            npc.is_clicked()
                for zombie in emg.zombie_list:
                    if zombie.style != 10 and not (
                        zombie.style == 7 and zombie.collide
                    ):
                        zombie.move()
                    zombie.is_fall()
                    if zombie.is_end():
                        global end_zombie
                        end_zombie = zombie
                        self.post(
                            Event(
                                Event_kind.GAMEOVER,
                                {"background": 4, "x": -2600, "y": 0},
                            )
                        )
                        break
        if self.Pause:
            screen.blit(menu, (250, 50))
            button_9.draw()
            button_13.draw()
            button_14.draw()
        if pausemanager.func == 2:
            self.post(Event(Event_kind.CHANGE_BAKEGROUND, {"background": 1}))
            emg.zombie_list.clear()
            plant_list.clear()
            for bullet in bulletlist_right:
                bulletlist_right.remove(bullet)
            for bullet in bulletlist_left:
                bulletlist_left.remove(bullet)
            player.hp = player.besthp
            the_level.win_count = 0
            the_level.count = 0
            card_box.sunshine = card_box.initsunshine
            self.player.place = 0
            for lawn in lawn_dict.keys():
                lawn_avaible[lawn] = True

        if event.code == Event_kind.CHANGE_BAKEGROUND:
            self.style = event.body["background"]
            self.image = picture_list[self.style]
            self.rect = self.image.get_rect()
            if self.style == 10:
                self.goods = event.body["goods"]
            else:
                if len(event.body) >= 2 and len(event.body) < 4:
                    self.rect.x = event.body["x"]
                    self.rect.y = event.body["y"]
                if len(event.body) >= 4:
                    self.rect.x = event.body["x"]
                    self.rect.y = event.body["y"]
                    player.rect.x = event.body["play_x"]
                    player.rect.y = event.body["play_y"]
            self.counterror = 0

        if event.code == Event_kind.GAMEOVER and not self.ji:
            self.ji = 1
            if self.dealing == 0:
                self.dealing = 1
                audio_player.stop_sound()
                audio_player.play_sound("失败音效2", 0)
            pygame.time.delay(2000)
            self.carema = [0, 0]
            for i in range(99, -1, -1):
                screen.blit(long_image, (-2400 - i * 2, 0))
                for zx2 in emg.zombie_list:
                    zx2.style = 4
                    zx2.x += 2
                for plant in plant_list:
                    plant.x += 2
                    plant.draw(self.carema, 11)
                for bullet in bulletlist_right:
                    bullet.rect.x += 2
                    bullet.draw(self.carema)
                for bullet in bulletlist_left:
                    bullet.rect.x += 2
                    bullet.draw(self.carema)
                player.rect.x += 2
                emg.draw(self.carema)
                player.draw(self.carema, 11)
                pygame.display.update()
                pygame.time.delay(5)
            dayfail = pygame.image.load("images/dayfail.png")
            dayfail = pygame.transform.scale(dayfail, (4000, screen_height))
            end_zombie.style = 5
            end_zombie.x = 300
            for i in range(300):
                screen.blit(dayfail, (-2400, 0))
                end_zombie.move(0.3 - end_zombie.move_speed)
                emg.draw(self.carema)
                player.draw(self.carema, 11)
                for plant in plant_list:
                    plant.draw(self.carema, 11)
                for bullet in bulletlist_right:
                    bullet.draw(self.carema)
                for bullet in bulletlist_left:
                    bullet.draw(self.carema)
                pygame.display.update()
            go = pygame.image.load("images/gameover.png")
            dayfail2 = pygame.image.load("images/dayfail2.png")
            dayfail2 = pygame.transform.scale(dayfail2, (4000, screen_height))
            go2 = pygame.image.load("images/gameover2.png")
            go2 = pygame.transform.scale(go2, (400, 320))
            for zx3 in emg.zombie_list:
                if zx3.style != 5 and zx3.style != 9:
                    zx3.style = 6
            if self.dealing == 1:
                self.dealing = 2
                audio_player.stop_sound()
                audio_player.play_sound("失败音效3", 0)

            for i in range(1, 500, 10):
                screen.blit(dayfail2, (-2400, 0))
                for zx3 in emg.zombie_list:
                    if zx3.style == 6:
                        zx3.draw(self.carema)
                player.draw(self.carema, 12)
                for plant in plant_list:
                    plant.draw(self.carema, 12)
                for bullet in bulletlist_right:
                    bullet.draw(self.carema, 12)
                for bullet in bulletlist_left:
                    bullet.draw(self.carema, 12)
                goo = pygame.transform.scale(go, (i, i))
                screen.blit(goo, (500 - 0.5 * i, 350 - 0.5 * i))
                pygame.display.update()
                pygame.time.delay(10)
            pygame.time.delay(2000)
            screen.blit(dayfail2, (-2400, 0))
            for zx3 in emg.zombie_list:
                if zx3.style == 6:
                    zx3.draw(self.carema)
                    pygame.display.update()
            player.draw(self.carema, 12)
            for plant in plant_list:
                plant.draw(self.carema, 12)
            for bullet in bulletlist_right:
                bullet.draw(self.carema, 12)
            for bullet in bulletlist_left:
                bullet.draw(self.carema, 12)
            screen.blit(go2, (280, 170))
            pygame.display.update()
            self.style = 4

        if event.code == Event_kind.RESTART:
            the_level.win_count = 0
            self.ji = 0
            self.style = 2
            player.rect.x = 200
            player.rect.y = 200
            player.post(
                Event(Event_kind.REQUEST_MOVE, {"POS": (player.rect.x, player.rect.y)})
            )
            self.post(
                Event(
                    Event_kind.CHANGE_BAKEGROUND, {"background": 2, "x": -2600, "y": 0}
                )
            )
            emg.zombie_list = []
            for bullet in bulletlist_right:
                bulletlist_right.remove(bullet)
            for bullet in bulletlist_left:
                bulletlist_left.remove(bullet)
        if event.code == Event_kind.EATEN:
            if event.body["objecct"] == player:
                self.style = 4

        if event.code == Event_kind.TALK:
            self.style = 5
            self.object = event.body["object"]

        if event.code == Event_kind.WORDS:
            self.text = event.body["text"]
            self.status1 = 100

        if event.code == Event_kind.WIN:
            moneyindex = 0
            for winindex in range(1, 202):
                screen.blit(long_image, (self.carema[0] + 2600, self.carema[1]))
                player.draw(self.carema)
                emg.draw(self.carema)
                for plant in plant_list:
                    plant.draw(self.carema)
                for bullet in bulletlist_right:
                    bullet.draw(self.carema)
                white_trans = (255, 255, 255, min(2 * winindex, 255))
                semi_trans_surface = pygame.Surface((1000, 700), pygame.SRCALPHA)
                pygame.draw.rect(semi_trans_surface, white_trans, (0, 0, 1000, 700))
                screen.blit(semi_trans_surface, (0, 0))
                if winindex >= 1 and winindex <= 400:
                    wincupp = pygame.image.load("images/通关奖杯.png").convert_alpha()
                    if winindex == 1:
                        pass  # 这里放胜利的音效
                    if winindex <= 100:
                        wincupp = pygame.transform.scale(
                            wincupp, (166 + winindex, 136 + 0.82 * winindex)
                        )
                        screen.blit(
                            wincupp, (700 - 3.5 * winindex, 350 - 2.5 * winindex)
                        )
                    else:
                        wincupp = pygame.transform.scale(wincupp, (266, 218))
                        screen.blit(wincupp, (350, 100))
                moneyindex += 0.2
                moneyblit = int(moneyindex % 5) + 4
                if moneyindex < 15:
                    diamond1 = Fallthing(money_frame[moneyblit], 600, 280, 40, 40)
                    diamond2 = Fallthing(money_frame[moneyblit], 700, 280, 40, 40)
                    diamond3 = Fallthing(money_frame[moneyblit], 800, 280, 40, 40)
                    diamond1.draw([0, 0])
                    diamond2.draw([0, 0])
                    diamond3.draw([0, 0])
                elif moneyindex < 20:
                    diamond1 = Fallthing(
                        money_frame[moneyblit],
                        600 - h(moneyindex - 15, 600 - 30),
                        280 + h(moneyindex - 15, 630 - 280),
                        40,
                        40,
                    )
                    diamond2 = Fallthing(
                        money_frame[moneyblit],
                        700 - h(moneyindex - 15, 700 - 30),
                        280 + h(moneyindex - 15, 630 - 280),
                        40,
                        40,
                    )
                    diamond3 = Fallthing(
                        money_frame[moneyblit],
                        800 - h(moneyindex - 15, 800 - 30),
                        280 + h(moneyindex - 15, 630 - 280),
                        40,
                        40,
                    )
                    diamond1.draw([0, 0])
                    diamond2.draw([0, 0])
                    diamond3.draw([0, 0])
                elif moneyindex < 25:
                    player_money.add_money(3000)
                    moneyindex = 114514
                else:
                    pass
                if winindex > 200:
                    self.post(Event(Event_kind.CHANGE_BAKEGROUND, {"background": 1}))
                    moneyindex = 0
                    winindex = 0
                    the_level.ultimate = False
                    break
                pygame.time.delay(20)
                pygame.display.update()
            the_level.hardness = 1
            self.cheat = False
            self.post(Event(Event_kind.WORDS, {"text": "简单模式开启"}))
            self.post(Event(Event_kind.CHEAT, {"cheat": False}))
        pausemanager.detect()

        if event.code == Event_kind.CHEAT:
            if event.body["cheat"]:
                player.hp = 1000000
                player.besthp = 1000000
                player.beat = 1000000
                player.shoot_speed = 1
                player.speed = 15
                player_money.money = 10000
                card_box.initsunshine = 5000
            else:
                player.hp = player.story[1]
                player.besthp = player.story[2]
                player.beat = player.story[3]
                player.shoot_speed = player.story[4]
                player.speed = player.story[0]
                player_money.money = 200
                card_box.initsunshine = 50

import pygame
import random
import sys
import time
import copy
from Creature import *
from Openai import *
from Battle import *
from Resources import *


class Talk_content:  # NPC对话
    def __init__(self, font=font):
        self.dialog_surface = pygame.image.load("images/对话框.png")
        self.dialog_surface = pygame.transform.scale(self.dialog_surface, (1050, 400))
        self.dialog_rect = (-20, 500, 1050, 400)
        self._dialog_text = []  # 用于存储文本的内部变量
        self.text_surfaces = []
        self.font = font
        self.y_offset = 10 + font.get_height()
        self.count_text = 0
        # 初始化字体

    @property
    def dialog_text(self):
        return self._dialog_text

    @dialog_text.setter
    def dialog_text(self, str):
        self.text_surfaces.clear()
        self._dialog_text.append(str)
        self.y_offset = 50
        for line in self._dialog_text:
            text_surface = self.font.render(line, True, (255, 255, 255))  # 黑色文本
            # 水平居中应该使用 dialog_rect 的宽度
            text_rect = text_surface.get_rect(
                center=(text_surface.get_width() // 2 + 20, self.y_offset + 500)
            )
            self.text_surfaces.append((text_surface, text_rect))
            self.y_offset += font.get_height()
        if self.y_offset > 500:
            self.dialog_rect.height = self.y_offset - 500 + 200

    def create_talk(self, kind):
        self.image = pygame.image.load(NPC_picture[f"{kind}"]).convert_alpha()
        screen.blit(self.image, (40, 200))
        screen.blit(self.dialog_surface, self.dialog_rect)
        for text_surface, text_rect in self.text_surfaces:
            screen.blit(text_surface, text_rect)

    def update(self):
        self.count_text = 0
        self._dialog_text.clear()
        self.text_surfaces.clear()

    def gen_text(self, kind, talk_staus):
        if talk_staus == 0 or kind == 0:
            try:
                self.dialog_text = All_talk[f"{kind}"][self.count_text]
                self.count_text += 1
                if self.y_offset > 180:
                    self._dialog_text.clear()
                    self.y_offset = 50
            except:
                pass
        else:
            try:
                self.dialog_text = Help_talk[f"{kind}"][self.count_text]
                self.count_text += 1
                if self.y_offset > 180:
                    self._dialog_text.clear()
                    self.y_offset = 50
            except:
                pass

    def help_text(self, kind, talk_staus):
        global help_count
        if help_count[kind] <= len(Help_talk[f"{kind}"]):
            self.gen_text(kind, talk_staus)
            help_count[kind] += 1
        if help_count[kind] >= len(Help_talk[f"{kind}"]) + 1:
            if (
                player_money.money >= require_list[kind]
                and card_box.plant[kind] == False
            ):
                self.dialog_text = "帮助成功!你的卡槽里多了这个植物！"
                card_box.plant[kind] = True
                player_money.reduce_money(require_list[kind])
            elif card_box.plant[kind] == True:
                self.dialog_text = "你已经帮助过了，并且买下了这个植物"
            else:
                self.dialog_text = f"你需要{require_list[kind]}块钱才能帮助"


talk1 = Talk_content()
count0 = 0
talk_ai = Talk_content()


class Text(EntityLike):  # 文本框输入
    def __init__(self, surf, x, y, width, height, font):
        self.surf = surf
        self.font = font
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.list = []
        self.active = False
        self.cursor = False  # 光标
        self.count = 0  # 闪烁频率
        self.delete = False  # 是否删除

    def draw(self):
        pygame.draw.rect(self.surf, (0, 0, 0), self.rect, 1)
        tet_pic = self.font.render("".join(self.list), True, (0, 0, 0))
        self.surf.blit(tet_pic, (self.x + 5, self.y + 10))
        self.count += 1
        if self.count >= 30:
            self.count = 0
            self.cursor = not self.cursor
        if self.active and self.cursor:  # 画光标
            text_pic_rect = tet_pic.get_rect()
            x = self.rect.x + 5 + text_pic_rect.width
            pygame.draw.line(
                self.surf,
                (0, 0, 0),
                (x, self.y + 5),
                (x, self.y + self.rect.height - 5),
                1,
            )
        if self.delete:
            try:
                self.list.pop()
                self.delete = False
            except:
                pass

    def get_text(self, event):
        mouse_pos = pygame.mouse.get_pos()
        mouses = pygame.mouse.get_pressed()
        global count0
        if mouses[0]:
            if self.rect.collidepoint(mouse_pos):
                self.active = True
            else:
                self.active = False
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.delete = True
                elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    global All_talk
                    self.active = False
                    stay_list = []
                    for str in comb_str(self.list):
                        stay_list += AI_talk(str)
                    for str in stay_list:
                        All_talk["0"].append(str)
                    self.list.clear()
                else:
                    self.list.append(event.unicode)


text1 = Text(screen, 30, 630, 950, 50, font)

NPCs.append(NPC(190, 300, "images/player's wife/图层 1.png", 1))
NPCs.append(NPC(50, 600, "images/坚果/坚果图层-1.png", 3))
NPCs.append(NPC(-1300, 280, "images/双重射手/图层-1.png", 6))
NPCs_inhouse = []
NPCs_inhouse.append(NPC(200, 700, "images/戴夫/图层-2.png", 2))
NPCs_inhouse.append(NPC(-800, 800, "images/窝瓜/图层-2.png", 4))
NPCs_inhouse.append(NPC(30, 50, "images/寒冰射手/图层-2.png", 5))

NPCs_onroof = []
NPCs_onroof.append(NPC(300, 200, "images/机枪射手/图层-1.png", 7))

All_talk = {
    "0": [],
    "1": [
        "你好豌豆,我是一个可爱的向日葵，想和你一起守护家园",
        "(点击继续显示更多对话)",
        "僵尸很快会到来，你必须尽快做好准备。",
        "寻找植物来帮助你",
        "你得帮他们他们才会帮你",
        "(点击帮助进入帮助模式，再点击继续进行帮助)",
        "如果你想让自己变强，可以和房子中万能的戴夫谈谈。",
        "'提示：空格射击，进入房子靠鼠标点击门'",
    ],  # 向日葵
    "2": [
        "hello,i am dave",
        "i can sell you some amazing thing",
        "why do i have these things?",
        "because i am crazy",
        "man!what can i say?",
        "'看上去戴夫不会说中文'",
    ],  # 戴夫
    "3": [
        "呃呃。。",
        "你好。。",
        "我是坚果，你是坚果吗?",
        "我在草坪上只是想晒晒太阳。",
        "你问我脑袋为什么尖尖的",
        "那我问你，你是坚果还是窝瓜啊，那我问你",
    ],  # 坚果
    "4": [
        "小子，没事就别来找碴",
        "想当年，我可是非常强壮的",
        "我能在战场上大杀四方的",
        "你问我为什么成天坐在这里?",
        "....",
    ],
    "5": [
        "你好豌豆，我是寒冰射手",
        "你问我为什么拥有寒冰之力,是不是用了什么科技",
        "我不用科技，我纯自然。",
        "我连蛋白粉都不用的，连蛋白粉都不用的",
        "我最多也就用点鱼油啊，维生素啊，葡萄糖啊",
        "什么生长补剂，我最多也就用点蛋白粉",
        "什么氮泵啊，我都不用的",
    ],
    "6": [
        "你是豌豆家族的对吧",
        "不知你是否记得机枪射手",
        "它拥有强大的力量",
        "强于平庸的你我",
        "你问他是我什么关系，是不是我爸",
        "机枪是不是我爸？不是我爸，是我师傅",
        "....",
        "机枪是我什么关系？当然是我爸。",
    ],
    "7": [
        "你最终还是上来了吗",
        "我时常不明白年轻人前仆后继地奔向战场是为了什么",
        "打僵尸？，少年们，你们应该有自己的梦想",
        "不要认为自己的宿命就是死在这个战场上",
        "打完这场战斗就离开吧，去寻找自己的幸福",
    ],
}
Help_talk = {
    "1": [
        "不是所有的植物都会无偿帮助你",
        "但我会",
        "不管你帮不帮我",
        "(要表白吗?)",
        "'算了，那种事情不要啊'",
        "(你获得了向日葵卡,花了0块钱)",
    ],
    "3": [
        "什么，你想让我打僵尸？",
        "在那之前我想吃点东西",
        "哪里贵了，这么多年都是这个价格",
        "这么多年积蓄涨没涨，找找自己的问题",
        "(需要支付100块钱)",
    ],
    "4": [
        "小子，你还是太年轻了",
        "打僵尸这事不是儿戏",
        "可能会付出生命的",
        "如果你执意要去，我可以帮你，前提是你通过我的测验",
        "(提示：打僵尸攒积500块钱)",
    ],
    "5": [
        "你知道上战场意味着什么吗",
        "这意味着离开自己的老婆孩子",
        "一句话，得加钱",
        "(需要支付1000块钱)",
    ],
    "6": [
        "如果要打僵尸的话我一次可以射出两颗子弹",
        "所以啊",
        "所以你得给双倍的钱",
        "(需要支付2000块钱)",
    ],
    "7": [
        "孩子，既然你找到我了",
        "那你的忙我自然会帮",
        "至于什么时候会帮你，那要看你的本事了",
        "但是，我希望你考虑一下自己的未来",
    ],
}
require_list = [0, 0, 0, 100, 500, 1000, 2000, 0]

help_count = [0, 0, 0, 0, 0, 0, 0, 0]


def event_get(text):
    for event in pygame.event.get():
        text.get_text(event)
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            sys.exit()

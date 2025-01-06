import pygame
import random
import sys
import time
import copy
from Creature import *
from Openai import *
from Battle import *

NPC_picture = {
    "1": "images/player's wife/图层 1.png",
    "0": "images/戴夫/图层-1.png",
    "2": "images/戴夫/图层-1.png",
    "3": "images/坚果/坚果图层-1.png",
    "4": "images/窝瓜/图层-1.png",
}

pygame.font.init()
font = pygame.font.Font(f"word/pop.ttf", 30)
font1 = pygame.font.Font(f"word/pop.ttf", 15)


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
        # screen1 = pygame.display.get_surface()  # 获取当前屏幕
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
        if help_count[kind] <= len(Help_talk[f"{kind}"]) - 1:
            self.gen_text(kind, talk_staus)
            help_count[kind] += 1
        if help_count[kind] >= len(Help_talk[f"{kind}"]):
            if player_money.money >= require_list[kind]:
                self.dialog_text = "帮助成功"
                card_box.plant[kind] = True
                player_money.reduce_money(require_list[kind])
            else:
                self.dialog_text = f"你需要{require_list[kind]}块钱才能帮助"


talk1 = Talk_content()
count0 = 0
talk_ai = Talk_content(font1)


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
                    for str in comb_str(self.list):
                        stay_list = AI_talk(str)
                    for str in stay_list:
                        All_talk["0"].append(str)
                    self.list.clear()
                else:
                    self.list.append(event.unicode)


text1 = Text(screen, 30, 630, 950, 50, font)

NPCs.append(NPC(190, 300, "images/player's wife/图层 1.png", 1))
NPCs.append(NPC(50, 600, "images/坚果/坚果图层-1.png", 3))
NPCs_inhouse = []
NPCs_inhouse.append(NPC(200, 700, "images/戴夫/图层-2.png", 2))
NPCs_inhouse.append(NPC(-800, 800, "images/窝瓜/图层-2.png", 4))
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
        "(你获得了坚果卡,花了100块钱)",
    ],
    "4": [
        "小子，你还是太年轻了",
        "打僵尸这事不是儿戏",
        "可能会付出生命的",
        "如果你执意要去，我可以帮你，前提是你通过我的测验",
        "(提示：打僵尸攒积500块钱)",
        "(你获得了窝瓜卡，花了500块钱)",
    ],
}
require_list = [0, 0, 0, 100, 500]

help_count = [0, 0, 0, 0, 0]


def comb_str(string_list):
    result = []
    current_string = ""
    punctuation = re.compile(r"[,.?!]")
    for s in string_list:
        if not current_string:
            current_string = s
        else:
            if s=='' or s==' ' or s=='\n':
                continue
            else:
                if punctuation.search(s[-1]):
                    current_string += s
                    result.append(current_string)
                    current_string = ""
                else:
                    current_string += "" + s
    if current_string:
        result.append(current_string)
    return result


def event_get(text):
    for event in pygame.event.get():
        text.get_text(event)
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            sys.exit()

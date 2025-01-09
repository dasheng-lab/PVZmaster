import pygame
import copy
from Event import *

pygame.init()
screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
sunflower_image = pygame.image.load("images/向日葵卡.png")
sunflower_image = pygame.transform.scale(sunflower_image, (55, 80))
nut_image = pygame.image.load("images/坚果卡.png")
nut_image = pygame.transform.scale(nut_image, (55, 80))
melon_image = pygame.image.load("images/窝瓜卡.png")
melon_image = pygame.transform.scale(melon_image, (55, 80))
coldpea_image = pygame.image.load("images/寒冰射手卡.png")
coldpea_image = pygame.transform.scale(coldpea_image, (55, 80))
doubpea_image = pygame.image.load("images/双重射手卡.png")
doubpea_image = pygame.transform.scale(doubpea_image, (55, 80))
gunpea_image = pygame.image.load("images/机枪射手卡.png")
gunpea_image = pygame.transform.scale(gunpea_image, (55, 80))

plantcard_image = [
    0,
    sunflower_image,
    0,
    nut_image,
    melon_image,
    coldpea_image,
    doubpea_image,
    gunpea_image,
]


sunflower2_image = pygame.image.load("images/向日葵卡2.png")
sunflower2_image = pygame.transform.scale(sunflower2_image, (55, 80))
nut2_image = pygame.image.load("images/坚果卡2.png")
nut2_image = pygame.transform.scale(nut2_image, (55, 80))
melon2_image = pygame.image.load("images/窝瓜卡2.png")
melon2_image = pygame.transform.scale(melon2_image, (55, 80))
coldpea2_image = pygame.image.load("images/寒冰射手卡2.png")
coldpea2_image = pygame.transform.scale(coldpea2_image, (55, 80))
doubpea2_image = pygame.image.load("images/双重射手卡2.png")
doubpea2_image = pygame.transform.scale(doubpea2_image, (55, 80))
gunpea2_image = pygame.image.load("images/机枪射手卡2.png")
gunpea2_image = pygame.transform.scale(gunpea2_image, (55, 80))

plantcard_image2 = [
    0,
    sunflower2_image,
    0,
    nut2_image,
    melon2_image,
    coldpea2_image,
    doubpea2_image,
    gunpea2_image,
]


sunflower_coldimage = pygame.image.load("images/向日葵冷却.png")
sunflower_coldimage = pygame.transform.scale(sunflower_coldimage, (55, 80))
nut_coldimage = pygame.image.load("images/坚果冷却.png")
nut_coldimage = pygame.transform.scale(nut_coldimage, (55, 80))
melon_coldimage = pygame.image.load("images/窝瓜冷却.png")
melon_coldimage = pygame.transform.scale(melon_coldimage, (55, 80))
coldpea_coldimage = pygame.image.load("images/寒冰射手冷却.png")
coldpea_coldimage = pygame.transform.scale(coldpea_coldimage, (55, 80))
doubpea_coldimage = pygame.image.load("images/双重射手冷却.png")
doubpea_coldimage = pygame.transform.scale(doubpea_coldimage, (55, 80))
gunpea_coldimage = pygame.image.load("images/机枪射手冷却.png")
gunpea_coldimage = pygame.transform.scale(gunpea_coldimage, (55, 80))


shovelbank = pygame.image.load("images/铲槽.png")
shovelbank = pygame.transform.scale(shovelbank, (100, 100))
transistor = 0
picture_list = []
start_image = pygame.image.load("images/start.png")
start_image = pygame.transform.scale(start_image, (1000, 700))
picture_list.append(start_image)
main_image = pygame.image.load("images/main.png")
main_image = pygame.transform.scale(main_image, (1000, 700))
picture_list.append(main_image)
long_image = pygame.image.load("images/longbackground.png")
long_image = pygame.transform.scale(long_image, (4000, 700))
picture_list.append(long_image)
gameover3_image = pygame.image.load("images/gameover3.png")
gameover3_image = pygame.transform.scale(gameover3_image, (400, 320))
picture_list.append(gameover3_image)
dayfail = pygame.image.load("images/dayfail.png")
dayfail = pygame.transform.scale(dayfail, (4000, 700))
picture_list.append(dayfail)
dayfail2 = pygame.image.load("images/dayfail2.png")
dayfail2 = pygame.transform.scale(dayfail2, (4000, 700))
picture_list.append(dayfail2)
picture_list.append("0")
house_image = pygame.image.load("images/daifuhouse.png")
house_image = pygame.transform.scale(house_image, (2000, 1300))
picture_list.append(house_image)
roof_image = pygame.image.load("images/roof.jpg")
roof_image = pygame.transform.scale(roof_image, (1500, 700))
picture_list.append(roof_image)

menu = pygame.image.load("images/menu.png")
menu = pygame.transform.scale(menu, (500, 600))
moneyimage = pygame.image.load("images/钱数.png")
moneyimage = pygame.transform.scale(moneyimage, (150, 50))
finalwave = pygame.image.load("images/FinalWave.png").convert_alpha()
pygame.font.init()
font = pygame.font.Font(f"word/pop.ttf", 30)
font1 = pygame.font.Font(f"word/pop.ttf", 20)
font2 = pygame.font.Font(f"word/pop.ttf", 25)
font3 = pygame.font.Font(f"word/pop.ttf", 15)
FONTS = [
    pygame.font.Font(pygame.font.get_default_font(), font_size)
    for font_size in [48, 36, 24]
]
NPCs = []
jindut0 = pygame.image.load("images/进度条0.png")
jindut0 = pygame.transform.scale(jindut0, (150, 25))
jindut1 = pygame.image.load("images/进度条1.png")
jindut1 = pygame.transform.scale(jindut1, (150, 25))
jindut2 = pygame.image.load("images/进度条2.png")
jindut2 = pygame.transform.scale(jindut2, (150, 25))
melonjump_frame = []
for i in range(1, 5):
    for j in range(1, 3):
        picture = pygame.image.load(f"images/窝瓜跳跃/图层-{i}.png").convert_alpha()
        melonjump_frame.append(picture)

cold_dict = {
    "1": [sunflower_coldimage, 50],
    "3": [nut_coldimage, 50],
    "4": [melon_coldimage, 50],
    "5": [coldpea_coldimage, 175],
    "6": [doubpea_coldimage, 200],
    "7": [gunpea_coldimage, 200],
}
place_dict = {"1": 280, "3": 335, "4": 390, "5": 445, "6": 500, "7": 555}
camera_lack = 300
bulletlist_right = pygame.sprite.Group()
bulletlist_left = pygame.sprite.Group()
shooter_count = 0

player_frame = []
for i in range(1, 14):
    picture = pygame.image.load(f"images/shootermove/图层 {i}.png").convert_alpha()
    player_frame.append(picture)

sunflowernor_frame = []
for i in range(1, 19):
    picture = pygame.image.load(f"images/player's wife/图层 {i}.png").convert_alpha()
    sunflowernor_frame.append(picture)
daifu_frame = []
for i in range(1, 16):
    picture = pygame.image.load(f"images/戴夫/图层-{i}.png").convert_alpha()
    picture = pygame.transform.scale(picture, (120, 200))
    daifu_frame.append(picture)
nut_frame = []
for i in range(1, 9):
    picture = pygame.image.load(f"images/坚果/坚果图层-{i}.png").convert_alpha()
    nut_frame.append(picture)
melon_frame = []
for i in range(1, 18):
    picture = pygame.image.load(f"images/窝瓜/图层-{i}.png").convert_alpha()
    melon_frame.append(picture)
coldpea_frame = []
for i in range(1, 16):
    picture = pygame.image.load(f"images/寒冰射手/图层-{i}.png").convert_alpha()
    coldpea_frame.append(picture)
doubpea_frame = []
for i in range(1, 16):
    picture = pygame.image.load(f"images/双重射手/图层-{i}.png").convert_alpha()
    doubpea_frame.append(picture)
gunpea_frame = []
for i in range(1, 14):
    picture = pygame.image.load(f"images/机枪射手/图层-{i}.png").convert_alpha()
    gunpea_frame.append(picture)


frame = []
for i in range(1, 19):
    fm_cjs = pygame.image.load(f"images/commonjs/cjs{i}.png").convert_alpha()
    frame.append(fm_cjs)
cold_frame = []
for picture in frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    cold_frame.append(picture2)
frame0 = [frame, cold_frame]

cjsdiewalk_frame = []
for i in range(1, 19):
    picture = pygame.image.load(
        f"images/cjsdiewalk/cjsdiewalk图层-{i}.png"
    ).convert_alpha()
    cjsdiewalk_frame.append(picture)
cjsdiewalkcold_frame = []
for picture in cjsdiewalk_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    cjsdiewalkcold_frame.append(picture2)
cjsdiewalk_frame0 = [cjsdiewalk_frame, cjsdiewalkcold_frame]


head_frame = []
for i in range(1, 13):
    picture = pygame.image.load(f"images/掉头/头图层-{i}.png").convert_alpha()
    head_frame.append(picture)
headcold_frame = []
for picture in head_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    headcold_frame.append(picture2)
head_frame0 = [head_frame, headcold_frame]

cjsfall_frame = []
for i in range(1, 11):
    picture = pygame.image.load(f"images/僵尸死/僵尸死图层-{i}.png").convert_alpha()
    cjsfall_frame.append(picture)
cjsfallcold_frame = []
for picture in cjsfall_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    cjsfallcold_frame.append(picture2)
cjsfall_frame0 = [cjsfall_frame, cjsfallcold_frame]

cjseat_frame = []
for i in range(1, 22):
    picture = pygame.image.load(f"images/cjseat/cjseat图层-{i}.png").convert_alpha()
    cjseat_frame.append(picture)
cjseatcold_frame = []
for picture in cjseat_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    cjseatcold_frame.append(picture2)
cjseat_frame0 = [cjseat_frame, cjseatcold_frame]


cjsnoheadeat_frame = []
for i in range(1, 12):
    picture = pygame.image.load(
        f"images/cjsnoheadeat/cjsnoheadeat图层-{i}.png"
    ).convert_alpha()
    picture = pygame.transform.scale(picture, (83, 95))
    cjsnoheadeat_frame.append(picture)
cjsnoheadeatcold_frame = []
for picture in cjsnoheadeat_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 1, 1, 2)
    cjsnoheadeatcold_frame.append(picture2)
cjsnoheadeat_frame0 = [cjsnoheadeat_frame, cjsnoheadeatcold_frame]


money_frame = []
for i in range(1, 10):
    picture = pygame.image.load(f"images/钱/钱币{i}.png").convert_alpha()
    money_frame.append(picture)
sunflowerfunc_frame = []
for i in range(1, 7):
    picture = pygame.image.load(f"images/向日葵头亮/图层-{i}.png").convert_alpha()
    sunflowerfunc_frame.append(picture)

sunflower_frame = [sunflowernor_frame, sunflowerfunc_frame]

nuthurt1_frame = []
for i in range(1, 9):
    picture = pygame.image.load(f"images/坚果1/图层-{i}.png").convert_alpha()
    nuthurt1_frame.append(picture)
nuthurt2_frame = []
for i in range(1, 9):
    picture = pygame.image.load(f"images/坚果2/图层-{i}.png").convert_alpha()
    nuthurt2_frame.append(picture)
nut_set = [nut_frame, nuthurt1_frame, nuthurt2_frame]
roadblock_frame = []
for i in range(1, 22):
    picture = pygame.image.load(f"images/路障僵尸/路障僵尸图层-{i}.png").convert_alpha()
    roadblock_frame.append(picture)
roadblockcold_frame = []
for picture in roadblock_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    roadblockcold_frame.append(picture2)
roadblock_frame0 = [roadblock_frame, roadblockcold_frame]

roadblockeat_frame = []
for i in range(1, 12):
    picture = pygame.image.load(
        f"images/路障僵尸啃食/路障僵尸啃食图层-{i}.png"
    ).convert_alpha()
    roadblockeat_frame.append(picture)
roadblockeatcold_frame = []
for picture in roadblockeat_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    roadblockeatcold_frame.append(picture2)
roadblockeat_frame0 = [roadblockeat_frame, roadblockeatcold_frame]

bucket_frame = []
for i in range(1, 16):
    picture = pygame.image.load(f"images/铁桶僵尸/铁桶僵尸图层-{i}.png").convert_alpha()
    bucket_frame.append(picture)
bucketcold_frame = []
for picture in bucket_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    bucketcold_frame.append(picture2)
bucket_frame0 = [bucket_frame, bucketcold_frame]

bucketeat_frame = []
for i in range(1, 12):
    picture = pygame.image.load(
        f"images/铁桶僵尸啃食/铁桶僵尸啃食图层-{i}.png"
    ).convert_alpha()
    bucketeat_frame.append(picture)
bucketeatcold_frame = []
for picture in bucketeat_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    bucketeatcold_frame.append(picture2)
bucketeat_frame0 = [bucketeat_frame, bucketeatcold_frame]

rugby_frame = []
for i in range(1, 12):
    picture = pygame.image.load(
        f"images/橄榄球僵尸/橄榄球僵尸图层-{i}.png"
    ).convert_alpha()
    rugby_frame.append(picture)
rugbycold_frame = []
for picture in rugby_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    rugbycold_frame.append(picture2)
rugby_frame0 = [rugby_frame, rugbycold_frame]


rugbynocap_frame = []
for i in range(1, 12):
    picture = pygame.image.load(
        f"images/橄榄球僵尸掉帽子/橄榄球僵尸掉帽子图层-{i}.png"
    ).convert_alpha()
    rugbynocap_frame.append(picture)
rugbynocapcold_frame = []
for picture in rugbynocap_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    rugbynocapcold_frame.append(picture2)
rugbynocap_frame0 = [rugbynocap_frame, rugbynocapcold_frame]

rugbynocapeat_frame = []
for i in range(1, 11):
    picture = pygame.image.load(
        f"images/橄榄球僵尸掉帽子啃食/橄榄球僵尸掉帽子啃食图层-{i}.png"
    ).convert_alpha()
    rugbynocapeat_frame.append(picture)
rugbynocapeatcold_frame = []
for picture in rugbynocapeat_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    rugbynocapeatcold_frame.append(picture2)
rugbynocapeat_frame0 = [rugbynocapeat_frame, rugbynocapeatcold_frame]

rugbyeat_frame = []
for i in range(1, 11):
    picture = pygame.image.load(
        f"images/橄榄球僵尸啃食/橄榄球僵尸啃食图层-{i}.png"
    ).convert_alpha()
    rugbyeat_frame.append(picture)
rugbyeatcold_frame = []
for picture in rugbyeat_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    rugbyeatcold_frame.append(picture2)
rugbyeat_frame0 = [rugbyeat_frame, rugbyeatcold_frame]

rugbyfall_frame = []
for i in range(1, 8):
    picture = pygame.image.load(
        f"images/橄榄球僵尸死/橄榄球僵尸死图层-{i}.png"
    ).convert_alpha()
    rugbyfall_frame.append(picture)
rugbyfallcold_frame = []
for picture in rugbyfall_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    rugbyfallcold_frame.append(picture2)
rugbyfall_frame0 = [rugbyfall_frame, rugbyfallcold_frame]

rugbynohead_frame = []
for i in range(1, 11):
    picture = pygame.image.load(
        f"images/橄榄球僵尸无头/橄榄球僵尸无头图层-{i}.png"
    ).convert_alpha()
    rugbynohead_frame.append(picture)
rugbynoheadcold_frame = []
for picture in rugbynohead_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    rugbynoheadcold_frame.append(picture2)
rugbynohead_frame0 = [rugbynohead_frame, rugbynoheadcold_frame]

rugbynoheadeat_frame = []
for i in range(1, 11):
    picture = pygame.image.load(
        f"images/橄榄球僵尸无头啃食/橄榄球僵尸无头啃食图层-{i}.png"
    ).convert_alpha()
    rugbynoheadeat_frame.append(picture)
rugbynoheadeatcold_frame = []
for picture in rugbynoheadeat_frame:
    picture1 = copy.copy(picture)
    picture2 = changecolor(picture1, 0.8, 0.8, 2)
    rugbynoheadeatcold_frame.append(picture2)
rugbynoheadeat_frame0 = [rugbynoheadeat_frame, rugbynoheadeatcold_frame]


NPC_picture = {
    "1": "images/player's wife/图层 1.png",
    "0": "images/戴夫/图层-1.png",
    "2": "images/戴夫/图层-1.png",
    "3": "images/坚果/坚果图层-1.png",
    "4": "images/窝瓜/图层-1.png",
    "5": "images/寒冰射手/图层-1.png",
    "6": "images/双重射手/图层-1.png",
    "7": "images/机枪射手/图层-1.png",
}
NPC_list = []
NPC_list.append(daifu_frame)
NPC_list.append(sunflowernor_frame)
NPC_list.append(daifu_frame)
NPC_list.append(nut_frame)
NPC_list.append(melon_frame)
NPC_list.append(coldpea_frame)
NPC_list.append(doubpea_frame)
NPC_list.append(gunpea_frame)
lawn_avaible = {}
lawn_dict = {}


class Rect1:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height

    def update(self, camera):
        self.rect.x = self.x - camera[0]
        self.rect.y = self.y - camera[1]


for i in range(9):
    for j in range(5):
        lawn_dict["lawn_rect" + str(i) + str(j)] = Rect1(
            162 + i * 84.5, 184 + j * 98, 86.5, 98
        )
        lawn_avaible["lawn_rect" + str(i) + str(j)] = True

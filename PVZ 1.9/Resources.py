import pygame
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
sunflower2_image = pygame.image.load("images/向日葵卡2.png")
sunflower2_image = pygame.transform.scale(sunflower2_image, (55, 80))
nut2_image = pygame.image.load("images/坚果卡2.png")
nut2_image = pygame.transform.scale(nut2_image, (55, 80))
melon2_image = pygame.image.load("images/窝瓜卡2.png")
melon2_image = pygame.transform.scale(melon2_image, (55, 80))
sunflower_coldimage = pygame.image.load("images/向日葵冷却.png")
sunflower_coldimage = pygame.transform.scale(sunflower_coldimage, (55, 80))
nut_coldimage = pygame.image.load("images/坚果冷却.png")
nut_coldimage = pygame.transform.scale(nut_coldimage, (55, 80))
melon_coldimage = pygame.image.load("images/窝瓜冷却.png")
melon_coldimage = pygame.transform.scale(melon_coldimage, (55, 80))
shovelbank=pygame.image.load("images/铲槽.png")
shovelbank=pygame.transform.scale(shovelbank,(100,100))
transistor=0
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
menu=pygame.image.load("images/menu.png")
menu=pygame.transform.scale(menu,(500,600))
moneyimage = pygame.image.load("images/钱数.png")
moneyimage = pygame.transform.scale(moneyimage, (150, 50))
finalwave=pygame.image.load("images/FinalWave.png").convert_alpha()
pygame.font.init()
font = pygame.font.Font(f"word/pop.ttf", 30)
font1 = pygame.font.Font(f"word/pop.ttf", 20)
font2 = pygame.font.Font(f"word/pop.ttf", 25)
font3 = pygame.font.Font(f"word/pop.ttf", 15)
FONTS = [pygame.font.Font(pygame.font.get_default_font(), font_size) for font_size in [48, 36, 24]]
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
}
place_dict = {"1": 280, "3": 335, "4": 390}
camera_lack = 300
bulletlist_right = pygame.sprite.Group()
bulletlist_left = pygame.sprite.Group()
shooter_count = 0
frame = []
for i in range(1, 19):
    fm_cjs = pygame.image.load(f"images/commonjs/cjs{i}.png").convert_alpha()
    frame.append(fm_cjs)

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
cjsdiewalk_frame = []
for i in range(1, 19):
    picture = pygame.image.load(
        f"images/cjsdiewalk/cjsdiewalk图层-{i}.png"
    ).convert_alpha()
    cjsdiewalk_frame.append(picture)
head_frame = []
for i in range(1, 13):
    picture = pygame.image.load(f"images/掉头/头图层-{i}.png").convert_alpha()
    head_frame.append(picture)
cjsfall_frame = []
for i in range(1, 11):
    picture = pygame.image.load(f"images/僵尸死/僵尸死图层-{i}.png").convert_alpha()
    cjsfall_frame.append(picture)
cjseat_frame = []
for i in range(1, 22):
    picture = pygame.image.load(f"images/cjseat/cjseat图层-{i}.png").convert_alpha()
    cjseat_frame.append(picture)
cjsnoheadeat_frame=[]
for i in range(1,12):
    picture=pygame.image.load(f"images/cjsnoheadeat/cjsnoheadeat图层-{i}.png").convert_alpha()
    picture=pygame.transform.scale(picture,(83,95))
    cjsnoheadeat_frame.append(picture)
money_frame=[]
for i in range(1,10):
    picture=pygame.image.load(f"images/钱/钱币{i}.png").convert_alpha()
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
roadblockeat_frame = []
for i in range(1, 12):
    picture = pygame.image.load(f"images/路障僵尸啃食/路障僵尸啃食图层-{i}.png").convert_alpha()
    roadblockeat_frame.append(picture)
bucket_frame = []
for i in range(1, 16):
    picture = pygame.image.load(f"images/铁桶僵尸/铁桶僵尸图层-{i}.png").convert_alpha()
    bucket_frame.append(picture)
bucketeat_frame = []
for i in range(1, 12):
    picture = pygame.image.load(f"images/铁桶僵尸啃食/铁桶僵尸啃食图层-{i}.png").convert_alpha()
    bucketeat_frame.append(picture)
NPC_picture = {
    "1": "images/player's wife/图层 1.png",
    "0": "images/戴夫/图层-1.png",
    "2": "images/戴夫/图层-1.png",
    "3": "images/坚果/坚果图层-1.png",
    "4": "images/窝瓜/图层-1.png",
}
NPC_list = []
NPC_list.append(daifu_frame)
NPC_list.append(sunflowernor_frame)
NPC_list.append(daifu_frame)
NPC_list.append(nut_frame)
NPC_list.append(melon_frame)
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
            162 + i * 84.5, 184 + j * 98, 86.5, 98)
        lawn_avaible["lawn_rect" + str(i) + str(j)] = True
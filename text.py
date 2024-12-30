import pygame
import sys
import random
import time
from block import Block
import Car
from enemy import EnemyManager
C, R = 11, 20  # 11列， 20行
CELL_SIZE = 40  # 格子尺寸
#test
FPS=60  # 游戏帧率
WIN_WIDTH = CELL_SIZE * C  # 窗口宽度
WIN_HEIGHT = CELL_SIZE * R  # 窗口高度

MOVE_SPACE=5
frame_count=0

running=False

pygame.init() # pygame初始化，必须有，且必须在开头
# 创建主窗体
clock = pygame.time.Clock() # 用于控制循环刷新频率的对象
win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
# 大中小三种字体，48,36,24
FONTS = [
    pygame.font.Font(pygame.font.get_default_font(), font_size) for font_size in [48, 36, 24]
]

class Block(pygame.sprite.Sprite):
    def __init__(self, c, r, color):
        super().__init__()

        self.cr = [c, r]
        self.x = c * CELL_SIZE
        self.y = r * CELL_SIZE

        self.image  = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.move_ip(self.x, self.y)

    def move_cr(self, c, r):
        self.cr[0] = c
        self.cr[1] = r
        self.x = c * CELL_SIZE
        self.y = r * CELL_SIZE
        self.rect.left = self.x
        self.rect.top = self.y
    def move(self, direction):
        dc, dr = DIRECTIONS[direction]
        next_c, next_r = self.cr[0] + dc, self.cr[1] + dr
        self.move_cr(next_c, next_r)
    def check_move(self, direction=""):
        move_c, move_r = DIRECTIONS[direction]
        next_c, next_r = self.cr[0] + move_c, self.cr[1] + move_r
        if 0 <= next_c < C and 0 <= next_r < R:
            return True
        return False
    def is_out(self):
        if 0 <= self.cr[0] < C and 0 <= self.cr[1] < R:
            return False
        return True
class Car(pygame.sprite.Group):
    def __init__(self, c, r, car_kind, car_color):
        super().__init__()
        for ri, row in enumerate(CARS[car_kind]):
            for ci, cell in enumerate(row):
                if cell == 1:
                    block = Block(c+ci, r+ri, car_color)
                    self.add(block)
    def move(self, direction=""):
        if all(block.check_move(direction) for block in self.sprites()):
            self.free_move(direction)
    def free_move(self, direction=""):
        for block in self.sprites():
            block.move(direction)
    def is_out(self):
        return all(block.is_out() for block in self.sprites())
    def check_collide(self, other_car):
        for block in self.sprites():
            bcr1 = tuple(block.cr)
            for other_block in other_car.sprites():
                bcr2 = tuple(other_block.cr)
                if bcr1 == bcr2:
                    return True
        return False
    def change(self, color):
        for block in self.sprites():
            block.image.fill(color)

DIRECTIONS = {
    "UP": (0, -1),  # (dc, dr)
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}
CARS = {  # 车的形状，即格子位置
    "player": [
        [0, 1, 0],
        [1, 1, 1],
        [1, 0, 1],
    ],
    "enemy": [
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 0],
    ]
}
pygame.display.set_caption('Car Racing by Sunshq')
def changecolor():
    randomnumR=random.randint(0, 255)
    randomnumG=random.randint(0, 255)
    randomnumB=random.randint(0, 255)
    enemy_color = (randomnumR, randomnumG, randomnumB)
    return enemy_color
randomnumR=random.randint(0, 255)
randomnumG=random.randint(0, 255)
randomnumB=random.randint(0, 255)
bg_color = (100, 100, 100)
enemy_color = (randomnumR, randomnumG, randomnumB)
class EnemyManager():

    def __init__(self):
        self.enemies = []
        self.move_count = 0
    def gen_new_enemies(self):  # 生成敌人赛车
        # 设置敌人赛车的生成间隔， 隔两倍的敌人赛车行数+1
        if self.move_count % (3 * len(CARS["enemy"]) + 1) == 1:

            ec = random.randint(1, C - len(CARS["enemy"][0]))
            enemy = Car(ec, 0, "enemy", changecolor())

            self.enemies.append(enemy)

    def move(self):  # 自动向下移动敌人赛车
        # 超出边界后，自动清理掉
        to_delete = []
        for i, enemy in enumerate(self.enemies):
            enemy.free_move("DOWN")
            if enemy.is_out():
                to_delete.append(i)

        for di in to_delete[::-1]:  # 倒着按序号来删除
            self.enemies.pop(di)

        self.move_count += 1

        self.gen_new_enemies()

    def draw(self, master):
        # 绘制敌人赛车
        for enemy in self.enemies:
            enemy.draw(master)
        return False
    def check_collide(self, player):
        for enemy in self.enemies:
            if enemy.check_collide(player):
                return True

        return False
player_color = (65, 105, 225)  # RoyalBlue
bottom_center_c = (C - len(CARS["player"][0])) // 2
bottom_center_r = R - len(CARS["player"])
car = Car(bottom_center_c, bottom_center_r, "player", player_color)
emg = EnemyManager()
score_color = (0,128,0) #提醒玩家开始游戏
start_info = FONTS[2].render("Press any key to start game", True, score_color)
text_rect = start_info.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))
win.blit(start_info, text_rect)
inventible = False
#invblock=Block(0,0,(0,0,0))
while True:
    frame_count += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 判断当前事件是否为点击右上角退出键
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if running:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    car.move("LEFT")
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    car.move("RIGHT")
                if event.key == pygame.K_UP or event.key == ord('w'):
                    car.move("UP")
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    car.move("DOWN")
            else: # 游戏结束后，响应任意按键，开始游戏
                # reset game， 重置变量和游戏状态
                time.sleep(1)
                car = Car(bottom_center_c, bottom_center_r, "player", player_color)
                frame_count = 0
                emg = EnemyManager()
                running =True

    if running:
        win.fill(bg_color)
        if frame_count % MOVE_SPACE == 0:
            emg.move()
        emg.draw(win)
        car.draw(win)
        text_info = FONTS[2].render("Scores: %d" % (frame_count / FPS), True, score_color)
        win.blit(text_info, dest=(0, 0))
        #win.blit(car.image, car.rect)
        if emg.check_collide(car):
            car.change((255,100,100))
            car.draw(win)
            running = False
            over_color = (255,0,0)
            texts = ["Game Over", "Scores: %d" % (frame_count / FPS), "Press Any Key to Restart game"]
            for ti, text in enumerate(texts):
                over_info = FONTS[ti].render(text, True, over_color)
                text_rect = over_info.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2 + 48 * ti))
                win.blit(over_info, text_rect)
    clock.tick(FPS) # 控制循环刷新频率,每秒刷新FPS对应的值的次数
    pygame.display.update()

import pygame
import random
import sys
import time
import copy
from Event import *
from Creature import *
from SceneLike import *
from Picture import *

# 初始化 pygame
pygame.init()
pygame.mixer.init()
FPS=120
# 设置窗口标题
pygame.display.set_caption("植物大战僵尸射击版")

# 加载背景图像

if __name__ == "__main__":
    plant = Player()  # 生成角色实例
    scene = SceneLike(plant)  # 生成场景实例
    listeners = [plant, scene]  # 将角色和场景加入监听者列表
    mouse()
    
    while True:
        event_get(text1)
        add_event(Event(pygame.KEYDOWN))  # 在while循环中，每轮都添加周期事件STEP
        for event in pygame.event.get():  # 将pygame默认事件如键盘等转换到自己的队列中
            add_event(Event(event.type))
        add_event(Event(Event_kind.STEP))  # 在while循环中，每轮都添加周期事件STEP
        add_event(Event(Event_kind.DRAW))  # 在while循环中，每轮都添加描绘事件DRAW
        while get_event_queue:  # 依次将事件队列中的事件取出并处理
            event = get_event_queue.pop(0)  # 取出一个事件
            for l in listeners:  # 遍历所有监听者
                l.listen(event)  # 调用监听者的listen方法来尝试对该事件进行响应
        
        pygame.time.Clock().tick(FPS)
        pygame.display.update()  # 缓冲绘制到屏幕上
import pygame
from Pautton import *
from Resources import *


class Money:
    def __init__(self):
        self.money = 0
        self.image = moneyimage

    def add_money(self, num):
        self.money += num

    def reduce_money(self, num):
        self.money -= num

    def draw(self):
        screen.blit(self.image, (0, 650))
        text1 = font.render(f"{self.money}", True, (127, 255, 127))
        screen.blit(text1, (58, 665))


player_money = Money()

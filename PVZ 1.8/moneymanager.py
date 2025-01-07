import pygame
from ppause import *
pygame.init()
font = pygame.font.Font(f"word/pop.ttf", 30)
font1 = pygame.font.Font(f"word/pop.ttf", 20)
moneyimage = pygame.image.load("images/钱数.png")
moneyimage = pygame.transform.scale(moneyimage, (150, 50))
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
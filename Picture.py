import pygame
import random
import sys
import time
import copy


'''bg_night = pygame.image.load("images/Nightfrontyard.png")
bg_night = pygame.transform.scale(bg_night, (screen_width, screen_height))
help=pygame.image.load("images/help.png")
help=pygame.transform.scale(help,(1000,700))
'''
def changecolor(image, R, G, B):
    width,height=image.get_size()
    for x in range(width):
        for y in range(height):
            r,g,b,a = image.get_at((x, y))
            r0 = min(int(r * R),254)
            g0 = min(int(g * G),254)
            b0 = min(int(b * B),254)
            image.set_at((x, y), (r0, g0, b0, a))
    return image
import pygame
import random
import sys
import time
import copy
import math

get_event_queue = []


def add_event(event):
    global get_event_queue
    get_event_queue.append(event)


class Event:
    def __init__(self, code: int, body={}):
        self.code = code
        self.body = body


class Listener:
    def __init__(self): ...
    def post(self, event):
        add_event(event)

    def listen(self, event):
        pass


class EntityLike(Listener):
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect

    def listen(self, event): ...
    def draw(self): ...


def changecolor(image, R, G, B):
    width, height = image.get_size()
    for x in range(width):
        for y in range(height):
            r, g, b, a = image.get_at((x, y))
            r0 = min(int(r * R), 254)
            g0 = min(int(g * G), 254)
            b0 = min(int(b * B), 254)
            image.set_at((x, y), (r0, g0, b0, a))
    return image


def f(x):
    return 60 * (1 / (1 + 2.71828 ** (-x)) - 0.5)
def g(y, a=1):
    if y <= 5:
        return -25 * math.sin(0.5 * y) - 25
    elif y <= 9:
        return a * y**2 + (35 / 2 - 14 * a) * y - 255 / 2 + 45 * a
    else:
        return g(9)
def h(x,a=1):
    return (a/5)*math.sqrt(10*x-x**2)



class Event_kind:
    DRAW = 1
    STEP = 2
    REQUEST_MOVE = 3
    CAN_MOVE = 4
    CAN_SHOOT = 5
    CHANGE_BAKEGROUND = 6
    GAMEOVER = 7
    RESTART = 8
    EATEN = 9
    TALK = 10
    WORDS = 11
    BOOM = 12

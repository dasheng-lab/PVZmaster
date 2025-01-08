import pygame
from Event import *
from Resources import *
screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
class Button:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(
            pygame.image.load(image).convert_alpha(), (width, height)
        )
        self.image2 = changecolor(
            pygame.transform.scale(
                pygame.image.load(image).convert_alpha(), (width, height)
            ),
            1.2,
            1.2,
            1.2,
        )
        self.rect = pygame.Rect(x, y, width, height)
        self.clicked = 20
        self.is_draw =False

    def draw(self):
        self.is_draw = True
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.image2, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if (
            self.clicked >= 20
            and self.rect.collidepoint(mouse_pos)
            and mouse_buttons[0]
        ):
            self.clicked = 0
            return self.rect.collidepoint(mouse_pos) and mouse_buttons[0]
        else:
            self.clicked += 1
            return False
class Button2:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(
            pygame.image.load(image).convert_alpha(), (width, height)
        )
        self.image2 = changecolor(
            pygame.transform.scale(
                pygame.image.load(image).convert_alpha(), (width, height)
            ),
            1.2,
            1.2,
            1.2,
        )
        self.rect = pygame.Rect(x, y, width, height)
        self.clicked = 20

    def draw(self, camera):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x = self.x - camera[0]
        self.rect.y = self.y - camera[1]
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.image2, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if (
            self.clicked >= 20
            and self.rect.collidepoint(mouse_pos)
            and mouse_buttons[0]
        ):
            self.clicked = 0
            return self.rect.collidepoint(mouse_pos) and mouse_buttons[0]
        else:
            self.clicked += 1
            return False
button_1 = Button(320, 580, 300, 100, "images/button1.png")
button_2 = Button(570, 103, 320, 140, "images/button2.jpg")
button_3 = Button(570, 245, 308, 140, "images/button3.jpg")
button_4 = Button(38, 153, 255, 45, "images/button4.jpg")
button_5 = Button(730, 544, 78, 76, "images/button5.jpg")
button_6 = Button(810, 585, 55, 60, "images/button6.jpg")
button_7 = Button(877, 580, 60, 52, "images/button7.jpg")
button_8 = Button(350, 400, 260, 50, "images/button8.png")
button_9 = Button(300, 525, 390, 100, "images/button9.png")
button_11 = Button(730, 0, 270, 60, "images/button11.png")
button_12 = Button(730, 0, 270, 60, "images/button12.png")
button_13=Button(355,400,280,55,"images/button13.png")
button_14=Button(355,450,280,50,"images/button14.png")
button_15=Button(850,0,150,50,"images/button15.png")
restart = Button(340, 400, 270, 60, "images/restart.png")
buttontalk_1 = Button(740, 470, 260, 50, "images/button8.png")
buttontalk_2 = Button(470, 470, 260, 50, "images/button9.png")
buttontalk_3 = Button(200, 470, 260, 50, "images/button10.png")
front_door = Button2(5, 340, 60, 170, "images/frontdoor.png")
behind_door = Button2(-1178, 278, 81, 240, "images/behinddoor.png")
front_door1 = Button2(950, 600, 50, 50, "images/箭头.png")
behind_door1 = Button2(-1000, 600, 50, 50, "images/箭头 左.png")
goods_shanghai = Button2(-100, 1200, 50, 50, "images/伤害.png")
goods_gongsu = Button2(-500, 1200, 50, 50, "images/攻速.png")
goods_shengming = Button2(-100, 980, 50, 50, "images/最大生命.png")
goods_sudu = Button2(-500, 980, 50, 50, "images/速度.png")
moneybox = Button(700, 350, 75, 75, "images/钱袋.png")
add_hp = Button(130, 0, 50, 50, "images/加号.png")
class Pause:
    def __init__(self):
        self.pause=False
        self.reasonpause=0  
        self.func=0
    def detect(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_2] and self.reasonpause%2==0:
            self.reasonpause+=1 
            self.pause=not self.pause
        if self.reasonpause%2!=0 and not keys[pygame.K_2]:
            self.reasonpause+=1
        if not self.pause:
            if (keys[pygame.K_2] or (button_15.is_clicked() and button_15.is_draw)) and self.reasonpause%2==0:
                self.pause=True
        else:
            if (button_9.is_clicked() or keys[pygame.K_2]) and self.reasonpause%2==0:
                self.pause=False
            if  button_13.is_clicked() and self.reasonpause%2==0:
                self.pause=False
                self.func=1
        if self.func!=0:
            self.func+=1
        if self.func==10:
            self.func=0
pausemanager=Pause()
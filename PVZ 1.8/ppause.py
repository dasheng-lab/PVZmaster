import pygame
from Event import *
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

button_9 = Button(300, 525, 390, 100, "images/button9.png")
button_13=Button(355,400,280,55,"images/button13.png")
button_14=Button(355,450,280,50,"images/button14.png")
button_15=Button(850,0,150,50,"images/button15.png")
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
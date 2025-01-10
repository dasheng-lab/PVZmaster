import pygame
import random
import sys
import time

get_event_queue=[]
def add_event(event):
    global get_event_queue
    get_event_queue.append(event)
DRAW=1
class Event():
    def __init__(self,code):
        self.code=code

class Listener():
    def __init__(self,code):
        self.code=code
    def post(self,event):
        add_event(event)
    def listen(self,event):
        pass

class EntityLike(Listener):
    def __init__(self,image,rect):
        self.image=image
        self.rect=rect
    def listen(self,event):
        if event.code==DRAW:
            self.draw()

# 初始化 pygame
pygame.init()
FPS=120
# 设置窗口大小
screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
# 设置窗口标题
pygame.display.set_caption("植物大战僵尸射击版")

# 加载背景图像
bg_day = pygame.image.load("images/longbackground.png")
# 缩放背景图像以适应窗口大小
bg_day = pygame.transform.scale(bg_day, (4000, screen_height))
bg_night = pygame.image.load("images/Nightfrontyard.png")
bg_night = pygame.transform.scale(bg_night, (screen_width, screen_height))
bg_start=pygame.image.load("images/start.png")
bg_start=pygame.transform.scale(bg_start,(1000,700))
bg_main=pygame.image.load("images/main.png")
bg_main=pygame.transform.scale(bg_main,(1000,700))
go3=pygame.image.load("images/gameover3.png")
go3=pygame.transform.scale(go3,(400,320))
help=pygame.image.load("images/help.png")
help=pygame.transform.scale(help,(1000,700))

frame=[]
for i in range(1,19):
    fm_cjs=pygame.image.load(f"images/commonjs/cjs{i}.png").convert_alpha()
    frame.append(fm_cjs)

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

pygame.font.init()
FONTS = [pygame.font.Font(pygame.font.get_default_font(), font_size) for font_size in [48, 36, 24]]
class ZombieManager(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.zombie_list=[]
        self.move_speed=0.1
        self.dealing=0
    def gen_new_zombie(self):
        gen=random.choice([425,315,230,125,25])
        if self.zombie_list==[]:
            self.zombie_list.append(Zombie(100,gen))
        else:
            if self.zombie_list[-1].x<750:
                self.zombie_list.append(Zombie(1000,gen))
    def move(self):
        for js in self.zombie_list:
            js.move()
    def draw(self):
        for jsd in self.zombie_list:
            jsd.draw()
class Zombie(ZombieManager):
    def __init__(self,x,y):
        super().__init__()
        self.style=0
        self.x=x
        self.y=y
        self.HP=270
        self.move_speed=0.1
        self.cjsindex=0
        self.image=pygame.image.load("images/commonjs/cjs1.png").convert_alpha()
    def draw(self):
        if self.style==0 and not over:
            self.cjsindex+=0.05
            cjsblit=int(self.cjsindex%len(frame))
            screen.blit(frame[cjsblit],(self.x,screen_height-(self.y+frame[cjsblit].get_height())))
            zombie_rect = fm_cjs.get_rect()
            zombie_rect.x = self.x
            zombie_rect.y = self.y
            self.image=frame[cjsblit]
        elif self.style==0 and over:
            screen.blit(self.image,(self.x,screen_height-(self.y+self.image.get_height())))
        elif self.style==1 and over:
            self.y=200
            self.cjsindex+=0.05
            cjsblit=int(self.cjsindex%len(frame))
            screen.blit(frame[cjsblit],(self.x,screen_height-(self.y+frame[cjsblit].get_height())))
            zombie_rect = fm_cjs.get_rect()
            zombie_rect.x = self.x
            zombie_rect.y = self.y
            self.image=frame[cjsblit]
        elif self.style==2 and over:
            if self.dealing==0:
                self.image = changecolor(self.image, 0.5,0.5,0.5)
                self.dealing=1
            screen.blit(self.image,(self.x,screen_height-(self.y+self.image.get_height())))
    def move(self):
        self.x-=self.move_speed
    def is_dead(self):
        if self.HP<=0:
            return True
        else:
            return False
    def is_end(self):
        if self.x<=70:
            self.style=1
            return True
        else:
            return False

class Button():
    def __init__(self,x,y,width,height,image):
        self.x=x
        self.y=y
        self.image=pygame.transform.scale(pygame.image.load(image).convert_alpha(),(width,height))
        self.image2=changecolor(pygame.transform.scale(pygame.image.load(image).convert_alpha(),(width,height)), 1.2,1.2,1.2)
        self.rect=pygame.Rect(x,y,width,height)
    def draw(self):
        mouse_pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.image2,(self.x,self.y))
        else:
            screen.blit(self.image,(self.x,self.y))
    def is_clicked(self):
        mouse_pos=pygame.mouse.get_pos()
        mouse_buttons=pygame.mouse.get_pressed()
        return self.rect.collidepoint(mouse_pos) and mouse_buttons[0]
button_1=Button(320,580,300,100,"images/button1.png")
button_2=Button(570,103,320,140,"images/button2.jpg")
button_3=Button(570,245,308,140,"images/button3.jpg")
button_4=Button(38,153,255,45,"images/button4.jpg")
button_5=Button(730,544,78,76,"images/button5.jpg")
button_6=Button(810,585,55,60,"images/button6.jpg")
button_7=Button(877,580,60,52,"images/button7.jpg")
button_8=Button(350,400,260,50,"images/button8.png")

cursor_image_path = "images/OIP-C (1).png"
cursor_image = pygame.image.load(cursor_image_path).convert_alpha()
cursor_image = pygame.transform.scale(cursor_image, (cursor_image.get_width(), cursor_image.get_height()))
cursor_size = cursor_image.get_size()
cursor_surface = pygame.Surface(cursor_size, pygame.SRCALPHA)
cursor_surface.blit(cursor_image, (0, 0))
hotspot_x = cursor_size[0] // 2
hotspot_y = cursor_size[1] // 2
custom_cursor = pygame.cursors.Cursor((hotspot_x, hotspot_y), cursor_surface)
pygame.mouse.set_cursor(custom_cursor)


over=False
enter=False
fight=False
insert=False
Help=False
ji=0
n=0


emg=ZombieManager()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if not enter:
        screen.blit(bg_start,(0,0))
        button_1.draw()
        if button_1.is_clicked():
            enter=True
    if enter and not fight and not insert:
        screen.blit(bg_main,(0,0))
        button_2.draw()
        button_3.draw()
        button_4.draw()
        button_5.draw()
        button_6.draw()
        button_7.draw()
    if button_2.is_clicked() and not insert and not Help:
        fight=True
    if (button_3.is_clicked() or button_4.is_clicked() or button_5.is_clicked()) and not insert and not Help:
        insert=True
    if button_6.is_clicked() and not insert and not Help:
        Help=True
    if button_7.is_clicked() and not insert and not Help:
        pygame.quit()
        sys.exit()
    if Help and not fight:
        screen.blit(help,(0,0))
        button_8=Button(350,600,260,50,"images/button8.png")
        button_8.draw()
        if button_8.is_clicked():
            Help=False
            button_8=Button(350,400,260,50,"images/button8.png")
    if insert and not fight:
        screen.blit(bg_main,(0,0))
        screen.blit(go3,(280,170))
        button_8.draw()
        if button_8.is_clicked():
            insert=False
    if fight:
        n+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    screen.blit(bg_day,(-200,0))
                if event.key == pygame.K_2:
                    screen.blit(bg_night,(0,0))
        if not over:
            screen.blit(bg_day,(-2600,0))
            if n>200:
                emg.gen_new_zombie()
                emg.move()
                emg.draw()
            for zx1 in emg.zombie_list:
                if zx1.is_end():
                    over=True
                    zx1.style=1
                    break
                

        if ji<1 and over:
            pygame.time.delay(2000)
            for i in range(99,-1,-1):
                screen.blit(bg_day,(-2400-i*2,0))
                for zx2 in emg.zombie_list:
                    zx2.x+=2
                emg.draw()
                pygame.display.update()
                pygame.time.delay(5)
            ji+=1
            dayfail=pygame.image.load("images/dayfail.png")
            dayfail=pygame.transform.scale(dayfail,(4000, screen_height))
            for i in range(500):
                screen.blit(dayfail,(-2400,0))
                zx1.move()
                emg.draw()
                pygame.display.update()
            go=pygame.image.load("images/gameover.png")
            dayfail2=pygame.image.load("images/dayfail2.png")
            dayfail2=pygame.transform.scale(dayfail2,(4000, screen_height))
            go2=pygame.image.load("images/gameover2.png")
            go2=pygame.transform.scale(go2,(400,320))
            for zx3 in emg.zombie_list:
                if zx3.style!=1:
                    zx3.style=2
            for i in range(1,500,10):
                screen.blit(dayfail2,(-2400,0))
                for zx3 in emg.zombie_list:
                    if zx3.style==2:
                        zx3.draw()
                goo=pygame.transform.scale(go,(i,i))
                screen.blit(goo,(500-0.5*i,350-0.5*i))
                pygame.display.update()
                pygame.time.delay(10)
            pygame.time.delay(2000)
            screen.blit(dayfail2,(-2400,0))
            for zx3 in emg.zombie_list:
                if zx3.style!=1:
                    zx3.draw()
                    pygame.display.update()
            screen.blit(go2,(280,170))
            pygame.display.update()
        
        # 更新屏幕
    pygame.time.Clock().tick(FPS)
    pygame.display.update()

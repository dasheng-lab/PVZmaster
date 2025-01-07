import pygame
import random
import sys
import time
import copy

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
bg_night = pygame.image.load("images/Nightfrontyard.png")
bg_night = pygame.transform.scale(bg_night, (screen_width, screen_height))
help=pygame.image.load("images/help.png")
help=pygame.transform.scale(help,(1000,700))

picture_list=[]
start_image=pygame.image.load("images/start.png")
start_image=pygame.transform.scale(start_image,(1000,700))
picture_list.append(start_image)
main_image=pygame.image.load("images/main.png")
main_image=pygame.transform.scale(main_image,(1000,700))
picture_list.append(main_image)
long_image=pygame.image.load("images/longbackground.png")
long_image=pygame.transform.scale(long_image,(4000, screen_height))
picture_list.append(long_image)
gameover3_image=pygame.image.load("images/gameover3.png")
gameover3_image=pygame.transform.scale(gameover3_image,(400,320))
picture_list.append(gameover3_image)

frame=[]
for i in range(1,19):
    fm_cjs=pygame.image.load(f"images/commonjs/cjs{i}.png").convert_alpha()
    frame.append(fm_cjs)

player_frame=[]
for i in range(1,14):
    picture=pygame.image.load(f"images/shootermove/图层 {i}.png").convert_alpha()
    player_frame.append(picture)

DRAW = 1
STEP = 2
REQUEST_MOVE = 3
CAN_MOVE = 4
CAN_SHOOT=5
CHANGE_BAKEGROUND=6

pygame.font.init()
FONTS = [pygame.font.Font(pygame.font.get_default_font(), font_size) for font_size in [48, 36, 24]]

bullet_list=pygame.sprite.Group()
shooter_count=0

get_event_queue=[]
def add_event(event):
    global get_event_queue
    get_event_queue.append(event)

class Event():
    def __init__(self,code:int,body={}):
        self.code=code
        self.body=body

class Listener():
    def __init__(self):...
    def post(self,event):
        add_event(event)
    def listen(self,event):
        pass

class EntityLike(Listener):
    def __init__(self,image,rect):
        self.image=image
        self.rect=rect
    def listen(self,event):...
    def draw(self):...

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

camera_lack=300

class Player(EntityLike):
    def __init__(self):
        self.image=pygame.image.load("images/shootermove/图层 1.png").convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.x=200
        self.rect.y=200
        self.speed=5
        self.pic_diex=0
        self.hp=200

    def listen(self, event: Event):  # 玩家类所响应的事件
        if event.code == pygame.KEYDOWN:  # 键盘按下事件
            self.keydown()
        elif event.code == CAN_MOVE:  # 响应场景发出的允许移动事件
            self.rect.x = event.body["POS"][0]
            self.rect.y = event.body["POS"][1]
        super().listen(event)  # 继承原有的响应事件内容，如对DRAW的响应

    def keydown(self):  # 键盘按下事件的响应
        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y>150:
            self.rect.y-=self.speed
        if keys[pygame.K_DOWN] and self.rect.y+self.rect.height<screen_height:
            self.rect.y+=self.speed
        if keys[pygame.K_LEFT] and self.rect.x>-2600:
            self.rect.x-=self.speed
        if keys[pygame.K_RIGHT] and self.rect.x+self.rect.width<1400:
            self.rect.x+=self.speed
        self.post(Event(REQUEST_MOVE, {"POS": (self.rect.x, self.rect.y)}))

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        if keys[pygame.K_SPACE]:
            global shooter_count 
            shooter_count=min(shooter_count+1,30)
            if shooter_count==30:
                bullet_list.add(Bullet(self))
                shooter_count=0
                self.post(Event(CAN_SHOOT))

    def draw(self,camera):
        self.pic_diex+=0.2
        player_blit=int(self.pic_diex%len(player_frame))
        player_image=player_frame[player_blit]
        if camera[0]+500-self.rect.x>camera_lack and camera[0]>-2600:
            camera[0]=self.rect.x-500+camera_lack
        if -camera[0]-500+self.rect.x>camera_lack and camera[0]<400:
            camera[0]=self.rect.x-500-camera_lack
        screen.blit(player_image,pygame.Rect(self.rect.x-camera[0],self.rect.y-camera[1],self.rect.width,self.rect.height))

class Bullet(pygame.sprite.Sprite):
    def __init__(self,shooter):
        super().__init__()
        self.image=pygame.image.load("images/bullet.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(22,22))
        self.rect=self.image.get_rect()
        self.rect.x=shooter.rect.x+50
        self.rect.y=shooter.rect.y+2.5
        self.speed=5
    def draw(self,camera):
        screen.blit(self.image, pygame.Rect(self.rect.x-camera[0],self.rect.y-camera[1],self.rect.width,self.rect.height)) 
    def move(self):
        #7 在屏幕范围内，实现往右移动
        if self.rect.x < 1000:
            self.rect.x += self.speed
        elif self.rect.x >= 1000:#8 子弹飞出屏幕，从精灵组删除
            self.kill()
                #9 遍历所有僵尸，判断是否碰撞
    def crash_zombie(self):
        for zombie in emg.zombie_list:
            if self.rect.colliderect(zombie.rect):
                zombie.HP-=20
                zombie.style=3
                self.kill()
                break

count_zombie=0

class ZombieManager(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.zombie_list=[]
        self.move_speed=0.5
        self.dealing=0
    def gen_new_zombie(self):
        gen=random.choice([425,315,230,125,25])
        if self.zombie_list==[]:
            self.zombie_list.append(Zombie(1000,gen))
        else:
            if self.zombie_list[-1].x<100:
                self.zombie_list.append(Zombie(100,gen))
    def move(self):
        for js in self.zombie_list:
            js.move()
    def draw(self):
        for jsd in self.zombie_list:
            jsd.draw()

class Zombie():
    def __init__(self,x,y):
        super().__init__()
        self.style=0
        self.x=x
        self.y=y
        self.HP=270
        self.move_speed=0.3
        self.cjsindex=0
        self.image=pygame.image.load("images/commonjs/cjs1.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(100,100))
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
    def draw(self,camera):
        if self.style==0 and not over:
            self.cjsindex+=0.1
            cjsblit=int(self.cjsindex%len(frame))
            self.rect.x=self.x
            self.rect.y=screen_height-(self.y+frame[cjsblit].get_height())
            screen.blit(frame[cjsblit],pygame.Rect(self.rect.x-camera[0],self.rect.y-camera[1],self.rect.width,self.rect.height))
        elif self.style==3 and not over:
            self.cjsindex+=0.1
            cjsblit=int(self.cjsindex%len(frame))
            self.rect.x=self.x
            self.rect.y=screen_height-(self.y+frame[cjsblit].get_height())
            story=copy.copy(frame[cjsblit])
            screen.blit(changecolor(story,1.6,1.6,1.6),pygame.Rect(self.rect.x-camera[0],self.rect.y-camera[1],self.rect.width,self.rect.height))
            self.style=0
        elif self.style==0 and over:
            self.rect.x=self.x
            self.rect.y=screen_height-(self.y+self.image.get_height())
            screen.blit(self.image,pygame.Rect(self.rect.x-camera[0],self.rect.y-camera[1],self.rect.width,self.rect.height))
        elif self.style==1 and over:
            self.rect.x=self.x
            self.y=screen_height-(self.y+frame[cjsblit].get_height())
            self.cjsindex+=0.1
            cjsblit=int(self.cjsindex%len(frame))
            screen.blit(frame[cjsblit],pygame.Rect(self.rect.x-camera[0],self.rect.y-camera[1],self.rect.width,self.rect.height))
        elif self.style==2 and over:
            self.rect.x=self.x
            self.rect.y=(self.x,screen_height-(self.y+self.image.get_height()))
            if self.dealing==0:
                self.image = changecolor(self.image, 0.5,0.5,0.5)
                self.dealing=1
            screen.blit(self.image,pygame.Rect(self.rect.x-camera[0],self.rect.y-camera[1],self.rect.width,self.rect.height))
    def move(self):
        if self.HP<=70:
            emg.zombie_list.remove(self)
        self.x-=self.move_speed

    def is_dead(self):
        if self.HP<=0:
            emg.zombie_list.remove(self)
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

def tuple_sub(a, b):
    return (a[0] - b[0], a[1] - b[1])
    # 有一种更好的写法是 return tuple(i - j for i, j in zip(a, b))，不同的运算只要修改中间的符号即可


def tuple_mul(a, b):
    return (a[0] * b, a[1] * b)


def tuple_min(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]))


def tuple_max(a, b):
    return (max(a[0], b[0]), max(a[1], b[1]))


class SceneLike(Listener):  # 场景的类，管理障碍物、角色、地图背景的描绘、刷新等

    def __init__(self, player,style=0,x=0,y=0):
        super().__init__()
        self.player = player  # 传递玩家的实例
        self.window_scale = (1000, 800)  # 显示窗口的大小
        self.map_range = (1500, 1000)  # 实际地图的大小
        self.carema = [0, 0]  # 镜头的初始位置
        self.style=style
        self.image=picture_list[style]
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def listen(self, event: Event):  # 场景所监听的事件
        super().listen(event)
        if event.code == REQUEST_MOVE:  # 监听玩家的移动请求事件
            can_move = 1  # 一开始默认可以移动
            if can_move:  # 如果可以移动的话就发送允许移动事件
                self.post(Event(CAN_MOVE, event.body))

        if event.code == STEP:  # STEP是每次游戏周期刷新时会被触发的事件
            for bullet in bullet_list:
                bullet.move()
                bullet.crash_zombie()
            for zombie in emg.zombie_list:
                zombie.move()
                if zombie.is_dead():
                    emg.zombie_list.remove(zombie)
            global count_zombie
            count_zombie+=1
            if count_zombie==120:
                emg.gen_new_zombie()
                count_zombie=0

        if event.code == DRAW:  # DRAW事件，用于描绘场景中的实体
            if self.style!=2:
                screen.blit(self.image,self.rect)
                if self.style==0:
                    button_1.draw()
                    if button_1.is_clicked():
                        self.post(Event(CHANGE_BAKEGROUND,{"background":1}))#选关界面
                if self.style==1:
                    button_2.draw()
                    button_3.draw()
                    button_4.draw()
                    button_5.draw()
                    button_6.draw()
                    button_7.draw()
                    if button_2.is_clicked():
                        self.post(Event(CHANGE_BAKEGROUND,{"background":2,"x":-2600,"y":0}))#开始战斗
                    if (button_3.is_clicked() or button_4.is_clicked() or
                        button_5.is_clicked() or button_6.is_clicked()):
                        self.post(Event(CHANGE_BAKEGROUND,{"background":3,"x":280,"y":170}))#帮助
                    if button_7.is_clicked():
                        pygame.quit()
                if self.style==3:
                    button_8.draw()
                    if button_8.is_clicked():
                        self.post(Event(CHANGE_BAKEGROUND,{"background":1}))
            if self.style==2:
                screen.blit(self.image,(self.rect.x-self.carema[0],self.rect.y-self.carema[1]))
                self.player.draw(self.carema)  # 描绘玩家图像
                for bullet in bullet_list:
                    bullet.draw(self.carema)
                for zombie in emg.zombie_list:
                    zombie.draw(self.carema)

        
        if event.code==CAN_SHOOT:
            for bullet in bullet_list:
                bullet.draw(self.carema)
        
        if event.code==CHANGE_BAKEGROUND:
            self.style=event.body["background"]
            self.image=picture_list[self.style]
            self.rect=self.image.get_rect()
            if len(event.body)>=2:
                self.rect.x=event.body["x"]
                self.rect.y=event.body["y"]


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

player=Player()
emg=ZombieManager()

if __name__ == "__main__":
    mob = Player()  # 生成角色实例
    scene = SceneLike(player)  # 生成场景实例
    listeners = [player, scene]  # 将角色和场景加入监听者列表

    while True:
        add_event(Event(pygame.KEYDOWN))  # 在while循环中，每轮都添加周期事件STEP
        for event in pygame.event.get():  # 将pygame默认事件如键盘等转换到自己的队列中
            add_event(Event(event.type))
        add_event(Event(STEP))  # 在while循环中，每轮都添加周期事件STEP
        add_event(Event(DRAW))  # 在while循环中，每轮都添加描绘事件DRAW
        while get_event_queue:  # 依次将事件队列中的事件取出并处理
            event = get_event_queue.pop(0)  # 取出一个事件
            for l in listeners:  # 遍历所有监听者
                l.listen(event)  # 调用监听者的listen方法来尝试对该事件进行响应
        pygame.time.Clock().tick(FPS)
        pygame.display.flip()  # 缓冲绘制到屏幕上
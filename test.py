import pygame
from moviepy import VideoFileClip
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
player_image = pygame.image.load("c:/Users/pc/Desktop/ppt/xiazai.png").convert_alpha()
player_rect = player_image.get_rect()
player_rect.x = 100
player_rect.y = 100
speed = 5  
current_level=0
current_frame_index=0# 记录当前显示的帧索引
end=0
count=0
group_of_Zombie=[]

# 加载背景图片，假设背景图片名为background.jpg，根据实际情况替换文件名及路径
level0_background_image = pygame.image.load("c:/Users/pc/Desktop/ppt/kaishi.png").convert()
level0_background_image = pygame.transform.scale(level0_background_image, (800, 600))
level1_background_image = pygame.image.load("c:/Users/pc/Desktop/ppt/day1.jpg").convert()
level1_background_image = pygame.transform.scale(level1_background_image, (800, 600))
level2_background_image = pygame.image.load("c:/Users/pc/Desktop/ppt/Nightfrontyard.png").convert()
level2_background_image = pygame.transform.scale(level2_background_image, (800, 600))
# 获取背景图片的矩形区域，初始坐标设为 (0, 0)
level0_background_rect = level0_background_image.get_rect()
level1_background_rect = level1_background_image.get_rect()
level2_background_rect = level2_background_image.get_rect()

cursor_image_path = "c:/Users/pc/Desktop/ppt/OIP-C (1).png"
cursor_image = pygame.image.load(cursor_image_path).convert_alpha()
cursor_size = cursor_image.get_size()
cursor_surface = pygame.Surface(cursor_size, pygame.SRCALPHA)
cursor_surface.blit(cursor_image, (0, 0))

hotspot_x = cursor_size[0] // 2
hotspot_y = cursor_size[1] // 2
custom_cursor = pygame.cursors.Cursor((hotspot_x, hotspot_y), cursor_surface)
pygame.mouse.set_cursor(custom_cursor)

class Button:
    def __init__(self,x,y,width,height,text,color,hover_color,size):
        self.rect=pygame.Rect(x,y,width,height)
        self.text=text
        self.color=color
        self.hover_color=hover_color
        self.font=pygame.font.Font(None,size)
    def draw(self,screen):
        mouse_pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen,self.hover_color,self.rect)
        text_surface=self.font.render(self.text,True,(0,0,0))
        text_rect=text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface,text_rect)
    def is_clicked(self):
        mouse_pos=pygame.mouse.get_pos()
        mouse_buttons=pygame.mouse.get_pressed()
        return self.rect.collidepoint(mouse_pos) and mouse_buttons[0]
button_0 = Button(425, 140, 290, 70, "Start", (128, 128, 128), (128, 128, 128),36)

class Zombie:
    def __init__(self,y,style):
        self.place_x=700
        self.place_y=y*100-35
        self.style=style    
    def draw(self,screen):
        if self.style==0:
            zombie_image = pygame.image.load("c:/Users/pc/Desktop/ppt/transparent_zombie1.gif").convert_alpha()
            zombie_image = pygame.transform.scale(zombie_image, (100, 100))
            zombie_rect = zombie_image.get_rect()
            zombie_rect.x = self.place_x
            zombie_rect.y = self.place_y
            screen.blit(zombie_image, zombie_rect)
        elif self.style==1:
            zombie_image = pygame.image.load("c:/Users/pc/Desktop/ppt/transparent_zombie1.gif").convert_alpha()
            zombie_image = pygame.transform.scale(zombie_image, (100, 100))
            zombie_rect = zombie_image.get_rect()
            zombie_rect.x = self.place_x
            zombie_rect.y = self.place
    def move(self):
        self.place_x-=2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running = False
            if event.key==pygame.K_0:
                 if current_level == 1:
                      current_level = 2
                 elif current_level == 2:
                      current_level = 1
       #if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
    if  current_level == 0:
        screen.blit(level0_background_image, level0_background_rect)
        button_0.draw(screen) 
    if current_level == 1 or current_level == 2:
        if current_level == 1:
            screen.blit(level1_background_image, level1_background_rect)
        elif current_level == 2:
            screen.blit(level2_background_image, level2_background_rect)
        if end==0 and count==180:
            group_of_Zombie.append(Zombie(random.randint(1,5),0))
    if button_0.is_clicked():
            current_level = 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
             player_rect.y -= speed  # 向上移动矩形
    if keys[pygame.K_DOWN]:
             player_rect.y += speed  # 向下移动矩形
    if keys[pygame.K_LEFT]:
             player_rect.x -= speed  # 向左移动矩形
    if keys[pygame.K_RIGHT]:
             player_rect.x += speed  # 向右移动矩形
    #button_0.draw(screen)
    for i in range(len(group_of_Zombie)):
        group_of_Zombie[i].draw(screen)
        group_of_Zombie[i].move()
    screen.blit(player_image, player_rect)
    if count<180:
        count+=1
    else:
        count=0
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
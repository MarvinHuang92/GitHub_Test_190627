# Escape The Dragon Game
# Chapter 7

import sys, time, random, math, pygame
from pygame.locals import *

class MySprite(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self) #extend the base Sprite class
        self.master_image = None
        self.frame = 0  # 当前帧序号
        self.old_frame = -1  # 上一帧序号
        self.frame_width = 1  # 每帧图像宽度
        self.frame_height = 1
        self.first_frame = 0  # 第一帧序号
        self.last_frame = 0  # 最后一帧序号
        self.columns = 1  # 主图中的列数
        self.last_time = 0  # 上一帧的时间

    # 这里相当于self.X  self.Y  self.position，不用特别关心
    #X property
    def _getx(self): return self.rect.x
    def _setx(self,value): self.rect.x = value
    X = property(_getx,_setx)
    # property函数四个默认参数，fget, fset, fdel, 说明文字
    # 对应的用法为：直接使用self.X, 给它赋值self.X = X1, 删除del self.X，直接使用即可
    # 更多参考：http://www.runoob.com/python/python-func-property.html


    #Y property
    def _gety(self): return self.rect.y
    def _sety(self,value): self.rect.y = value
    Y = property(_gety,_sety)

    #position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self,pos): self.rect.topleft = pos
    position = property(_getpos,_setpos)

    # 定义load方法，这个是以后可以通用的
    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0,0,width,height)
        self.columns = columns
        #try to auto-calculate total frames
        # 这里可以制动获取图像中的帧数，不需要手动输入
        # 但当主图的最后一行不满时，还是要手动输入！可以看caveman这个图
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    # 刷新下一帧的延时。同样是一个很通用的方法，注意rate的单位是毫秒
    def update(self, current_time, rate=30):
        #update animation frame number
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        #build current frame only if it changed
        # 只在frame序号改变的时候才刷新，而不是每一次while循环都刷新
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    # 替换掉原有的str(sprite)功能，如果这里没有双下划綫，调用方法就是sprite.str()。其实一样的。
    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
               "," + str(self.last_frame) + "," + str(self.frame_width) + \
               "," + str(self.frame_height) + "," + str(self.columns) + \
               "," + str(self.rect)

# 注意以下两个def是在class之外哦！
def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))

# 在最右边随机生成新的火箭
def reset_arrow():
    y = random.randint(250,350)
    arrow.position = 800,y
    global arrow_vel
    arrow_vel = random.randint(8, 14)

#main program begins
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Escape The Dragon Game")
font = pygame.font.Font(None, 18)
framerate = pygame.time.Clock()

#load bitmaps
bg = pygame.image.load("background.png").convert_alpha()

#create a sprite group
# 创建精灵类（容器），以后的add, draw和update方法是这个类自己携带的，可以直接使用
group = pygame.sprite.Group()
# 这个类下面没有赋予任何属性，因为它是系统自带的类，很多属性和方法都已经有了

#create the dragon sprite
dragon = MySprite(screen)
dragon.load("dragon.png", 260, 150, 3)  # 分别是：文件名，单帧的宽度和高度，而不是总共的，最后是列数，用来做除法的分母。行数是不需要的
dragon.position = 100, 230  # 定义初始位置
group.add(dragon)
# 这里就用到了group类自带的方法，这也就是使用group的好处

#create the player sprite
player = MySprite(screen)
player.load("caveman.png", 50, 64, 8)
player.first_frame = 1
player.last_frame = 7  # 注意这张主图的最后一行没有填满，所以没有自动获取帧数，而是手动输入
player.position = 400, 303
group.add(player)

#create the arrow sprite
arrow = MySprite(screen)
arrow.load("flame.png", 40, 16, 1)  # 只有1列，1帧
arrow.position = 800,320
group.add(arrow)

arrow_vel = 8.0
acc = 0.9
game_over = False
you_win = False
player_jumping = False
jump_vel = 0.0
player_start_y = player.Y

#repeating loop
while True:
    # 这里的数字是帧率，单位秒的倒数，这个数值和上面class里面的update的rate（毫秒）两者更慢的那一个在起作用
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]: sys.exit()
    elif keys[K_SPACE]:
        acc = 0.3  # 持续按下空格，就可以跳高一些
        if not player_jumping:  # 只在没有起跳时可以起跳一次，不允许二段跳
            player_jumping = True
            jump_vel = -8.0  # 初始起跳速度
    else: acc = 0.9  # 不按下空格时，加速度较大



    #update the arrow
    if not game_over:
        arrow.X -= arrow_vel
        if arrow.X < -40: reset_arrow()

    #did arrow hit player?
    # 无论是人还是龙撞上了火箭，都会被击退10像素
    if pygame.sprite.collide_rect(arrow, player):
        # Q: 场上一次只有一个arrow，可以直接使用碰撞功能，如果有多个arrow怎么办？
        reset_arrow()
        player.X -= 10

    #did arrow hit dragon?
    if pygame.sprite.collide_rect(arrow, dragon):
        reset_arrow()
        dragon.X -= 10

    #did dragon eat the player?
    if pygame.sprite.collide_rect(player, dragon):
        game_over = True

    #did the dragon get defeated?
    if dragon.X < -100:
        you_win = True
        game_over = True  # 这个是不能少的，不能因为win了就不gameover，因为所有动作都是基于not gameover循环的

    #is the player jumping?
    if player_jumping:
        player.Y += jump_vel
        jump_vel += acc  # 减速度
        if player.Y > player_start_y:
            player_jumping = False
            player.Y = player_start_y  # 要重置位置，不然有可能由于误差，让人越来越靠下
            jump_vel = 0.0


    #draw the background
    screen.blit(bg, (0,0))

    #update sprites
    if not game_over:
        group.update(ticks, 50)  # 这个的单位也是毫秒。。。而且也能够决定最终刷新率

    #draw sprites
    group.draw(screen)  # 这里的draw是针对所有精灵，那么有先后顺序吗？互相遮挡怎么办？

    print_text(font, 350, 560, "Press SPACE to jump!")

    if game_over:
        print_text(font, 360, 100, "G A M E   O V E R")
        if you_win:
            print_text(font, 330, 130, "YOU BEAT THE DRAGON!")
        else:
            print_text(font, 330, 130, "THE DRAGON GOT YOU!")

    
    pygame.display.update()
    


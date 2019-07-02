#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' Flappy_bird ver 0.2 '

__author__ = 'Marvin Huang'


import sys, random, pygame
from pygame.locals import *


class MySprite(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)  # extend the base Sprite class
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
    # X property
    def _getx(self):
        return self.rect.x

    def _setx(self, value):
        self.rect.x = value

    X = property(_getx, _setx)

    # property函数四个默认参数，fget, fset, fdel, 说明文字
    # 对应的用法为：直接使用self.X, 给它赋值self.X = X1, 删除del self.X，直接使用即可
    # 更多参考：http://www.runoob.com/python/python-func-property.html

    # Y property
    def _gety(self):
        return self.rect.y

    def _sety(self, value):
        self.rect.y = value

    Y = property(_gety, _sety)

    # position property
    def _getpos(self):
        return self.rect.topleft

    def _setpos(self, pos):
        self.rect.topleft = pos

    position = property(_getpos, _setpos)

    # 定义load方法，这个是以后可以通用的(主图文件名，每一帧的宽度高度，列数)
    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0, 0, width, height)
        self.columns = columns
        # try to auto-calculate total frames
        # 这里可以制动获取图像中的帧数，不需要手动输入
        # 但当主图的最后一行不满时，还是要手动输入！可以看caveman这个图
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    # 刷新下一帧的延时。同样是一个很通用的方法，注意rate的单位是毫秒
    def update(self, current_time, rate=30):
        # update animation frame number
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        # build current frame only if it changed
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
def print_text(font, x, y, text, color=(255, 255, 255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))


# 在最右边随机生成新的柱子（实质是生成缝隙）
def reset_pipe():
    y1 = random.randint(200, 460)  # 缝隙左上角的位置
    pipe_u1.position = 1774, y1 - 683
    pipe_d1.position = 1774, y1 + 232


# main program begins
pygame.init()
screen = pygame.display.set_mode((1774, 1000), FULLSCREEN, 32)
pygame.display.set_caption("Flappy Bird v0.2")
font = pygame.font.Font(None, 40)
framerate = pygame.time.Clock()

# load bitmaps
sky = pygame.image.load("sky.png").convert_alpha()

# create a sprite group
# 创建精灵类（容器），以后的add, draw和update方法是这个类自己携带的，可以直接使用
group = pygame.sprite.Group()
# 这个类下面没有赋予任何属性，因为它是系统自带的类，很多属性和方法都已经有了

# create the bird sprite
bird = MySprite(screen)
bird.load("bird.png", 94, 67, 1)  # 分别是：文件名，单帧的宽度和高度，而不是总共的，最后是列数，用来做除法的分母。行数是不需要的
bird.position = 355, 300  # 定义初始位置
group.add(bird)
# 这里就用到了group类自带的方法，这也就是使用group的好处

# create the pipe sprite
pipe_u1 = MySprite(screen)
pipe_u1.load("pipe_u.png", 127, 683, 1)  # 只有1列，1帧
pipe_u1.position = 1774, 218 - 683
group.add(pipe_u1)

pipe_d1 = MySprite(screen)
pipe_d1.load("pipe_d.png", 127, 683, 1)  # 下
pipe_d1.position = 1774, 218 + 232
group.add(pipe_d1)


# create the ground
ground = MySprite(screen)
ground.load("ground.png", 1774, 109, 1)
ground.position = 0, 891  # 定义初始位置
group.add(ground)

pipe_vel = 16.0
gravity = 1.0
game_over = False
drop_vel = 0.0
scored = False
score = 0

# repeating loop
while True:
    # 这里的数字是帧率，单位秒的倒数，这个数值和上面class里面的update的rate（毫秒）两者更慢的那一个在起作用
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    # 让pygame完全控制鼠标，鼠标不会显示，也不会超出窗口范围，但无法用鼠标退出游戏
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    elif keys[K_SPACE]:
        drop_vel -= 1.8  # 按下空格时，小鸟向上加速
    else:
        drop_vel += gravity  # 不按下空格时，自由落体

    if not game_over:
        bird.Y += drop_vel

    # update the pipes
    if not game_over:
        pipe_u1.X -= pipe_vel
        pipe_d1.X -= pipe_vel
        if pipe_u1.X < -127:
            reset_pipe()
            scored = False

    # did bird hit a pipe?
    if pygame.sprite.collide_rect(pipe_u1, bird):
        # Q: 场上一次只有一个pipe，可以直接使用碰撞功能，如果有多个pipe怎么办？
        game_over = True
    elif pygame.sprite.collide_rect(pipe_d1, bird):
        game_over = True

    # did bird hit the ground?
    elif pygame.sprite.collide_rect(ground, bird):
        game_over = True

    # did bird cross the pipes?
    if not scored and not game_over:
        if pipe_u1.X < 355 - 127:
            scored = True
            score += 1

    # draw the background
    screen.blit(sky, (0, 0))

    # update sprites (包括地面)
    if not game_over:
        group.update(ticks, 50)  # 这个的单位也是毫秒。。。而且也能够决定最终刷新率

    # draw sprites
    group.draw(screen)  # 这里的draw是针对所有精灵，那么有先后顺序吗？互相遮挡怎么办？

    print_text(font, 5, 5, "Score:  " + str(score))

    if game_over:
        print_text(font, 5, 60, "GAME OVER")

    pygame.display.update()



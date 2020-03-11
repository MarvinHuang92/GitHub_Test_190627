#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' Flappy_bird ver 0.1 '

__author__ = 'Marvin Huang'

import pygame
import time
from pygame.locals import *
from random import randint, choice
from Vec2d import Vec2d

SCREEN_SIZE = (1360, 768)
W = SCREEN_SIZE[0]
H = SCREEN_SIZE[1]

# 鸟所在基线的x坐标
BASELINE = 500
# 柱子的速度
PIPE_SPEED = 510
# 柱子的宽度
PIPE_WIDTH = 120
# 单个柱子的高度
PIPE_HEIGHT = 600
# 柱子的缝隙
PIPE_GAP = 240
PIPE_ITER = 800
# 鸟的尺寸
BIRD_SIZE = 50

alive = True
# 存活条件
Score = 0
Click_times = 0
next_pipe_id = 0


class Bird(object): 
	# 属性：location, speed(只在y方向定义)
	# 方法：render、collision、fly
	# render就是绘画自身	
    # collision检查是否碰撞
	# process接受用户指令移动
    def __init__(self):
        self.location = int(H/2)
        self.speed = 0
    def render(self, surface, image):
        x = BASELINE - BIRD_SIZE/2
        y = self.location - BIRD_SIZE/2
        surface.blit(image, (x, int(y)))
    def collision(self, gap_y):
        # 碰撞判定，传入参数:柱子的缝隙中心线y值
        # 当柱子在可能碰撞的x范围内时
        global alive
        global PIPE_GAP
        if not gap_y - (PIPE_GAP - BIRD_SIZE)/2 < self.location < gap_y + (PIPE_GAP - BIRD_SIZE)/2:
            alive = False
        else:
            PIPE_GAP -= 0.006
    def move(self, time_passed): # time_passed是以秒为单位
        global Click_times
        self.speed += time_passed * 700. # 重力加速度（注意向下为正）
        pressed_mouse = pygame.mouse.get_pressed()
        if pressed_mouse[0]:
            self.speed -= 100.
            Click_times += 1
        # 增加屏幕边缘限制（上边缘不能超出，下边缘会死）
        if self.location < 0 + BIRD_SIZE/2:
            self.location = 0 + BIRD_SIZE/2
            self.speed = 0
        if self.location > H + BIRD_SIZE/2:
            alive = False
        # 每一步都要让移动的东西继续移动
        self.location += time_passed * self.speed

class Pipe(object): 
	# 属性：location, speed(只在x方向定义), gap_y, id(因为柱子有很多个)
	# 方法：render、next_collision、move
    def __init__(self):
        self.location = 0
        self.speed = 0
        self.gap_y = 0
        self.id = 0
    def render(self, surface, image1, image2):
        x = self.location - PIPE_WIDTH/2
        y1 = self.gap_y - PIPE_GAP/2 - PIPE_HEIGHT # 上柱子的y值
        y2 = self.gap_y + PIPE_GAP/2 # 下柱子的y值
        surface.blit(image1, (int(x), int(y1)))
        surface.blit(image2, (int(x), int(y2)))
    def move(self, time_passed):
        self.speed = PIPE_SPEED
        self.location -= time_passed * self.speed
    def next_collision(self):
    # 给出下一个可能碰撞的柱子
        if BASELINE - (BIRD_SIZE + PIPE_WIDTH)/2 < self.location < BASELINE + (BIRD_SIZE + PIPE_WIDTH)/2:
            return self
        return None
    def get_score(self):
    # 计分
        global Score
        if BASELINE - (BIRD_SIZE + PIPE_WIDTH)/2 - 20 < self.location < BASELINE - (BIRD_SIZE + PIPE_WIDTH)/2:
            Score = self.id + 1


# 游戏主进程
def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    clock = pygame.time.Clock()

    # 让pygame完全控制鼠标，鼠标不会显示，也不会超出窗口范围，但无法用鼠标退出游戏
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    
    bird1_image = pygame.image.load("bird1.png").convert_alpha()
    #bird2_image = pygame.image.load("bird2.png").convert_alpha()
    pipe_up = pygame.image.load("pipe_up.png").convert_alpha()
    pipe_down = pygame.image.load("pipe_down.png").convert_alpha()

    bird = Bird()
    # 建立一个bird实例

    pipes = {}

    def add_pipe(pipe):
        # 增加一个新的柱子(这里只添加柱子，而不添加鸟)
        global next_pipe_id
        pipes[next_pipe_id] = pipe
        pipe.id = next_pipe_id
        next_pipe_id += 1
    
    for n in range(500):
        # 用之前定义的方法添加1000个柱子
        pipe = Pipe()
        pipe.location = W + PIPE_WIDTH/2 + 20 + PIPE_ITER * n
        pipe.gap_y = randint(PIPE_GAP/2 + 20, H - PIPE_GAP/2 - 20)
        add_pipe(pipe)
 
    while alive:
        for event in pygame.event.get():
            pass

        time_passed_ms = clock.tick(60)
        time_passed = time_passed_ms / 1000.0
		# 可以改变帧率
        background = pygame.surface.Surface(SCREEN_SIZE).convert()
        background.fill((255, 255, 255))

     
        for pipe in pipes.values():
            pipe.move(time_passed)
            if - PIPE_WIDTH/2 < pipe.location < W + PIPE_WIDTH/2:
                pipe.render(background, pipe_up, pipe_down)
            next_pipe = pipe.next_collision()
            if next_pipe is not None:
                bird.collision(next_pipe.gap_y)
            pipe.get_score()
        bird.move(time_passed)
        bird.render(background, bird1_image)

        font = pygame.font.SysFont("arial", 36)
        text_surface1 = font.render('CLICK TIMES: %d' % Click_times, True, (0, 0, 0))
        text_surface2 = font.render('SCORE: %d' % Score, True, (0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(text_surface1, (5, 5))
        screen.blit(text_surface2, (5, 45))
 
        pygame.display.update()
    
    time.sleep(0.2)
    while True:
        background = pygame.surface.Surface(SCREEN_SIZE).convert()
        background.fill((0, 0, 0))
        font = pygame.font.SysFont("arial", 72)
        text_surface3 = font.render('GAME OVER! your score: %d' % Score, True, (255, 255, 255))
        text_surface4 = font.render('press ESC to exit', True, (255, 255, 255))
        screen.blit(background, (0, 0))
        screen.blit(text_surface3, (270, 200))
        screen.blit(text_surface4, (410, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            # 由于鼠标失效，需要按Esc则退出游戏
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()

if __name__ == "__main__":
    run()


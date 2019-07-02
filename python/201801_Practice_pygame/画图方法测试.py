#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' draw方法测试 '

__author__ = 'Marvin Huang'

background_image_filename = 'D:\py\pygame\sushiplate.jpg'

import pygame
from pygame.locals import *
from sys import exit
from math import pi
# 由于角度采用弧度制，需要引用pi

pygame.init()

screen = pygame.display.set_mode((640, 480), 0, 32)
# 创建了一个窗口
background = pygame.image.load(background_image_filename).convert()
# 加载并转换图像

while True:
    # 游戏主循环

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
		    # 接收到退出事件后退出程序
    
    screen.blit(background, (0, 0))
    # 将背景图画上去
    x, y = pygame.mouse.get_pos()
    # 获得鼠标位置    

    if event.type == KEYDOWN:
        if event.key == K_r:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, 100, 50))
			# 第三个tuple的前两个参数表示Rect左上角位置
			# 后两个参数表示Rect的长宽（相对位移），而不是右下角位置
	
    if event.type == KEYDOWN:
        if event.key == K_p:
            pygame.draw.polygon(screen, (255, 0, 0), [(x, y), (x+100, y), (x+100, y+50)])
			# list里面是每个点的绝对坐标，这一点与Rect不同
			# 不用回到起点，会自动封闭

    if event.type == KEYDOWN:
        if event.key == K_c:
            pygame.draw.circle(screen, (255, 0, 0), (x, y), 50)
			# 第三个tuple是圆心，第四个是半径

    if event.type == KEYDOWN:
        if event.key == K_a:
            pygame.draw.arc(screen, (255, 0, 0), (x, y, 100, 50), 0, pi/3.0, 3)
			# 第三个tuple是圆心，第四个是半径

    
    pygame.display.update()
    # 刷新一下画面
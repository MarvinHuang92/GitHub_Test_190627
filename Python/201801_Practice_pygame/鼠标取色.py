#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 读取鼠标位置的颜色和RGB值 '

__author__ = 'Marvin Huang'

background_image_filename = 'D:\py\pygame\sushiplate.jpg'

import pygame
from pygame.locals import *
from sys import exit

pygame.init()

screen = pygame.display.set_mode((640, 520), 0, 32)
# 创建了一个窗口 (y方向多出的40像素用来显示取色框和文字)
pygame.display.set_caption('读取鼠标位置的颜色')
# 设置窗口标题

background = pygame.image.load(background_image_filename).convert()
# 加载并转换图像
color_surface = pygame.Surface((640, 40), 0, 32)
# 生成取色框

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
    
    color = screen.get_at((x, y))
	# 获取鼠标位置的颜色值

    color_surface.fill(color)
    screen.blit(color_surface, (0, 480))
	# 显示取色框
	
    c_avg = (color[0] + color[1] + color[2]) / 3
    if c_avg < 127:
        c = 255
    else:
        c = 0
	# 如果color颜色较暗，则显示文字用白色，否则用黑色
    
    font = pygame.font.SysFont("arial", 28)
    text_surface = font.render(str(color), True, (c, c, c))
    screen.blit(text_surface, (10, 480))
	# 显示color的数值

    pygame.display.update()
    # 刷新一下画面
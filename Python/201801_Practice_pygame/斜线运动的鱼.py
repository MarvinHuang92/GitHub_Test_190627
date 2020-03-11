#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' description of this module '

__author__ = 'Marvin Huang'

background_image_filename = 'D:\\py\\pygame\\sushiplate.jpg'
sprite_image_filename = 'D:\\py\\pygame\\fugu.png'
 
import pygame
from pygame.locals import *
from sys import exit
 
pygame.init()
 
screen = pygame.display.set_mode((640, 480), 0, 32)
 
background = pygame.image.load(background_image_filename).convert()
sprite = pygame.image.load(sprite_image_filename).convert_alpha()
 
clock = pygame.time.Clock()
 
x, y = 100., 100.
t = 0.
speed_x, speed_y = 133., 170.
#速度的单位是每秒多少个像素

while True:
 
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
 
    time_passed = clock.tick(60)
	# clock.tick会返回一个数字，表示距离上一次tick过去了多少毫秒
	# 括号里的是帧率FPS
    time_passed_seconds = time_passed / 1000.0
	# 把毫秒换算成秒
    fps = 1000.0 / time_passed
	# 计算实际帧率
    t += time_passed_seconds
	# 计算总时间

    font = pygame.font.SysFont("arial", 16)
    text_surface1 = font.render('TIME INTERVAL: %.3fs' % time_passed_seconds, True, (0, 0, 0))
    text_surface3 = font.render('FPS: %.4f' % fps, True, (0, 0, 0))
    text_surface2 = font.render('TOTAL TIME: %.3fs' % t, True, (0, 0, 0))

    screen.blit(background, (0,0))
    screen.blit(sprite, (x, y))
    screen.blit(text_surface1, (5, 5))
    screen.blit(text_surface2, (5, 25))
    screen.blit(text_surface3, (5, 45))
 
    x += speed_x * time_passed_seconds
    y += speed_y * time_passed_seconds    
 
    # 到达边界则把速度反向
    if x > 640 - sprite.get_width():
        speed_x = -speed_x
        x = 640 - sprite.get_width()
		# 一定要有这个重置命令，不然x>640可能会多次触发上面的条件，让鱼一直在边界附近来回转身
    elif x < 0:
        speed_x = -speed_x
        x = 0.
		# 重置的道理同上
 
    if y > 480 - sprite.get_height():
        speed_y = -speed_y
        y = 480 - sprite.get_height()
    elif y < 0:
        speed_y = -speed_y
        y = 0
 
    pygame.display.update()
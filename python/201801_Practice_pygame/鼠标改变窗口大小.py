#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' description of this module '

__author__ = 'Marvin Huang'

background_image_filename = 'D:\py\pygame\sushiplate.jpg'
 
import pygame
from pygame.locals import *
from sys import exit
 
SCREEN_SIZE = (640, 480)
 
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
 
background = pygame.image.load(background_image_filename).convert()
 
while True:
 
    event = pygame.event.wait()
    if event.type == QUIT:
        exit()
    if event.type == VIDEORESIZE:
		# 这个是改变窗口大小的事件名
        SCREEN_SIZE = event.size
        screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
        pygame.display.set_caption("Window resized to "+str(event.size))
		# 窗口标题会跟着改变，显示当前的分辨率
 
    screen_width, screen_height = SCREEN_SIZE
    # 这里需要重新填满窗口
    for y in range(0, screen_height, background.get_height()):
		# 在窗口高度范围内，每隔一个图片高度blit一个新图片（平铺模式）
        for x in range(0, screen_width, background.get_width()):
            screen.blit(background, (x, y))
 
    pygame.display.update()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' description of this module '

__author__ = 'Marvin Huang'

import pygame
pygame.init()
 
all_colors = pygame.Surface((4096,4096), depth=24)
 
for r in range(0, 256):
    print (r+1, "out of 256")
    x = (r&15)*256
	# &按位运算（求余数），如15的二进制是111，所以&15的结果是只保留最后3位，也就是除以16的余数
	# 运算达到的效果：让x每16列换一次行，而y同时加一
    y = (r>>4)*256
	# >>n是右移计算，相当于除以16并且不保留余数（2的n次方），同理<<n左移相当于乘以2的n次方
    for g in range(0, 256):
        for b in range(0, 256):
            all_colors.set_at((x+g, y+b), (r, g, b))

pygame.image.save(all_colors, "D:\py\pygame\\allcolors.bmp")


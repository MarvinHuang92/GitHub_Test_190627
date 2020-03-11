#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 坦克大战复刻版 ver 0.15 '

__author__ = 'Marvin Huang'

import pygame
import copy
from pygame.locals import *
from sys import exit
from random import randint, choice
from Vec2d import Vec2d
from math import *


SCREEN_SIZE = (1000, 624)
W = SCREEN_SIZE[0]
H = SCREEN_SIZE[1]

# 战场尺寸
BATTLEFIELD = (624, 624) 
Bx = BATTLEFIELD[0]
By = BATTLEFIELD[1]

#计分板尺寸
BB_SIZE = (W - Bx, By)
BW = BB_SIZE[0]
BH = BB_SIZE[1]

# TR地形最小单位边长（像素）
# TK坦克和基地边长
# CN炮弹长和宽
TR = 12
TK = 4*TR
# 基地位置
BASE_POSITION = (Bx/2 - TK/2, By - TK)
BASEx = BASE_POSITION[0]
BASEy = BASE_POSITION[1]
# 敌人的数量
ENEMY_COUNT = 30
ENEMY_COUNT2 = int(0.003*randint(0, 100)*ENEMY_COUNT)
ENEMY_COUNT3 = int(0.003*randint(0, 100)*ENEMY_COUNT)
ENEMY_COUNT4 = int(0.003*randint(0, 100)*ENEMY_COUNT)
ENEMY_COUNT1 = ENEMY_COUNT - ENEMY_COUNT2 - ENEMY_COUNT3 - ENEMY_COUNT4

# 游戏主进程
def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

    clock = pygame.time.Clock()
    tank_user_image = pygame.image.load("tank_user.png").convert_alpha()
    wall_image = pygame.image.load("wall.jpg").convert()
    iron_image = pygame.image.load("iron.jpg").convert()
    forrest_image = pygame.image.load("forrest.png").convert_alpha()
    river_image = pygame.image.load("river.jpg").convert()
    border_image = pygame.image.load("border.png").convert_alpha()
    tank_enemy1_image = pygame.image.load("tank_enemy1.png").convert_alpha()
    tank_enemy2_image = pygame.image.load("tank_enemy2.png").convert_alpha()
    tank_enemy3_image = pygame.image.load("tank_enemy3.png").convert_alpha()
    tank_enemy4_image = pygame.image.load("tank_enemy4.png").convert_alpha()
    canon_image = pygame.image.load("canon.png").convert_alpha()
    base_image = pygame.image.load("base.png").convert_alpha()


    tank = tank_user_image
    rotation_direction = 0.
    tank_pos = Vec2d(Bx/3 - TK/2, By - TK/2)  # 初始位置
    tank_speed = 24.  # 每秒前进的像素数（速度）

    canon_exist = False
    canon_pos = Vec2d(0. ,0.)
    canon_speed = Vec2d(0., -tank_speed)
    virtual_speed = canon_speed
    canon_speed_scalar = 80.

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
				# 让ESC也可以退出程序
        fps = 60
        time_passed = clock.tick(fps)
		# 可以改变帧率

        background = pygame.surface.Surface(SCREEN_SIZE).convert()
        background.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        # 画背景
        billboard = pygame.surface.Surface(BB_SIZE).convert()
        billboard.fill((255, 255, 255))
        screen.blit(billboard, (W, 0))


        pressed_keys = pygame.key.get_pressed()
        # 获取按键情况

        # 更改角度
        if pressed_keys[K_LEFT]:
            rotation_direction = 90.
            speed = Vec2d (-tank_speed,0.)
            virtual_speed = speed
        elif pressed_keys[K_RIGHT]:
            rotation_direction = 270.
            speed = Vec2d (tank_speed,0.)
            virtual_speed = speed
        elif pressed_keys[K_UP]:
            rotation_direction = 0.
            speed = Vec2d (0.,-tank_speed)
            virtual_speed = speed
        elif pressed_keys[K_DOWN]:
            rotation_direction = 180.
            speed = Vec2d (0.,tank_speed)
            virtual_speed = speed
        else:
            speed = Vec2d (0.,0.)

        if canon_exist:
            canon_draw_pos = Vec2d(canon_pos.x - TR / 2, canon_pos.y - TR / 2)
            screen.blit(canon_image, canon_draw_pos)
            canon_pos += canon_speed / tank_speed * canon_speed_scalar * time_passed_seconds
        else:
            canon_speed = virtual_speed
            if pressed_keys[K_SPACE]:
                canon_pos = canon_speed / tank_speed * (TK) + tank_pos
                canon_exist = True


        # 获得一条转向后的鱼
        rotated_tank = pygame.transform.rotate(tank, rotation_direction)

        # 获得绘制图片的左上角（感谢pltc325网友的指正）
        tank_draw_pos = Vec2d(tank_pos.x - TK / 2, tank_pos.y - TK / 2)
        screen.blit(rotated_tank, tank_draw_pos)

        time_passed = clock.tick()
        time_passed_seconds = time_passed * 30 / 1000.0

        tank_pos += speed * time_passed_seconds

        # 防止小鱼超出边框范围
        if tank_pos.x < 0 + TK / 2:
            tank_pos.x = 0 + TK / 2
        if tank_pos.x > Bx - TK / 2:
            tank_pos.x = Bx - TK / 2
        if tank_pos.y < 0 + TK / 2:
            tank_pos.y = 0 + TK / 2
        if tank_pos.y > By - TK / 2:
            tank_pos.y = By - TK / 2

        if canon_pos.x < 0 + TR / 2:
            canon_exist = False
        if canon_pos.x > Bx - TR / 2:
            canon_exist = False
        if canon_pos.y < 0 + TR / 2:
            canon_exist = False
        if canon_pos.y > By - TR / 2:
            canon_exist = False

        pygame.display.update()


if __name__ == "__main__":
    run()
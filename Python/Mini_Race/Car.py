#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 操作说明：支持键盘WASD或者方向键控制 '

__author__ = 'Marvin Huang'

background_image_filename = 'track.jpg'
sprite_image_filename = 'red-car-small.png'

W = 1440
H = 900

import pygame
from pygame.locals import *
from sys import exit
from Vec2d import Vec2d
from math import *

pygame.init()

screen = pygame.display.set_mode((W, H), 0, 32)

background = pygame.image.load(background_image_filename).convert()
sprite = pygame.image.load(sprite_image_filename).convert_alpha()

clock = pygame.time.Clock()

# 让pygame完全控制鼠标，鼠标不会显示，也不会超出窗口范围，但无法用鼠标退出游戏
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

sprite_pos = Vec2d(W/2, H/2)  # 初始位置
direction = 0.                # 初始角度
velocity = 0.                 # 初始速度（每秒多少像素）

acc_limit = 120.              # 最大加速度/减速度（路面附着系数）
power = 8000.                 # 等效最大功率
resistance = 0.12             # 阻力系数
steering_angle_limit = 2.50   # 等效方向盘最大转角（转向死区）
acc_coefficient = 1.1         # 横向加速度系数

sensitivity_thr = 1.8         # 油门灵敏度（每秒钟踏板移动速度）
sensitivity_brk = 1.8         # 刹车灵敏度
sensitivity_str = 2.0         # 转向灵敏度
spring_back = 2.1             # 回弹系数
limitation_thr = 0.9          # 油门死区（考虑到车子功率，即使小于1依然可能起步打滑）
limitation_brk = 0.8          # 刹车死区（大于1允许抱死打滑，小于1不会打滑）
steering_middle_pos = 0.1     # 方向盘中心虚位

throttle_pos = 0.             # 油门初始值
break_pos = 0.                # 刹车初始值
steering_pos = 0.             # 方向盘初始值

reverse = False  # 按住R键挂倒挡，需要先减速到0（容差正负1.5）

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        # 由于鼠标失效，需要按Esc则退出游戏
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()

    pressed_keys = pygame.key.get_pressed()

    time_passed = clock.tick()
    time_passed_seconds = time_passed / 1000.0
    
    # 转向(按下转向，放开回弹，两个一起按没有用)
    turn_left = False
    turn_right = False
    if pressed_keys[K_LEFT] or pressed_keys[K_a]:
        turn_left = True
    if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
        turn_right = True
    # 计算方向盘位置
    if turn_left and not turn_right:
        steering_pos += sensitivity_str * time_passed_seconds
    elif turn_right and not turn_left:
        steering_pos -= sensitivity_str * time_passed_seconds
    else:  # 回弹
        if steering_pos >= steering_middle_pos:
            steering_pos -= spring_back * sensitivity_str * time_passed_seconds
        elif steering_pos <= -steering_middle_pos:
            steering_pos += spring_back * sensitivity_str * time_passed_seconds
        else:  # 中心虚位内部直接归零
            steering_pos = 0.
    # 设置死区（不同于油门刹车，默认为1）
    if steering_pos > 1.:
        steering_pos = 1.
    elif steering_pos < -1.:
        steering_pos = -1.

    # 加减速（按下油门或刹车，全松开自然减速，两个一起按则效果累加）
    throttle = False
    breaking = False
    if velocity < 1.5:
        reverse = False  # 倒挡，必须减速到0才能挂倒挡
        
    if pressed_keys[K_UP] or pressed_keys[K_w]:
        throttle = True
    if pressed_keys[K_DOWN] or pressed_keys[K_s]:
        breaking = True
    if velocity > -1.5 and pressed_keys[K_r]:
        reverse = True
    # 计算踏板位置
    if throttle:
        if throttle_pos < limitation_thr:
            throttle_pos += sensitivity_thr * time_passed_seconds
        else:  # 死区
            throttle_pos = limitation_thr
    else:
        if throttle_pos > 0.:
            throttle_pos -= spring_back * sensitivity_thr * time_passed_seconds
        else:
            throttle_pos = 0.
    if breaking:
        if break_pos < limitation_brk:
            break_pos += sensitivity_brk * time_passed_seconds
        else:  # 死区
            break_pos = limitation_brk
    else:
        if break_pos > 0.:
            break_pos -= spring_back * sensitivity_brk * time_passed_seconds
        else:
            break_pos = 0.

    # 计算可用加速度
    velocity_non_zero = 0.1  # 防止出现除零错误
    if abs(velocity) > 0.1:
        velocity_non_zero = abs(velocity)
    
    acc_real = throttle_pos * power / velocity_non_zero
    if acc_real > acc_limit:
        acc_real = acc_limit
    
    dec_real = acc_limit * break_pos
    if dec_real > acc_limit:
        dec_real = acc_limit
    # 计算可以用于转向的剩余加速度
    acc_storage = acc_limit - max(acc_real, dec_real)
    if steering_pos != 0.:
        acc_steer = abs(steering_pos) * acc_coefficient * steering_angle_limit * abs(velocity)  # 实际转向需要的加速度
        if acc_steer > acc_storage:
            steering_angle = acc_storage / (acc_coefficient * velocity_non_zero)  # 如果超出限制，则相应的减小转向角度
        else:
            steering_angle = steering_angle_limit * abs(steering_pos)
    else:
        acc_steer = 0.
        steering_angle = 0.

    # 控制车速(方向翻转，因为屏幕下方为正方向)
    if not reverse:
        velocity -= acc_real * time_passed_seconds
        velocity += dec_real * time_passed_seconds
        # 模拟自然减速
        velocity += resistance * velocity_non_zero * time_passed_seconds
        # 限制速度不为负
        if velocity > 0:
            velocity = 0
    else:  # 倒挡时
        velocity += acc_real * time_passed_seconds
        velocity -= dec_real * time_passed_seconds
        # 模拟自然减速
        velocity -= resistance * velocity_non_zero * time_passed_seconds
        # 限制速度不为负
        if velocity < 0:
            velocity = 0

    # 打印背景
    screen.blit(background, (0,0))

    # 获得一条转向后的鱼
    rotated_sprite = pygame.transform.rotate(sprite, direction)
    # 转向后，图片的长宽会变化，因为图片永远是矩形，为了放得下一个转向后的矩形，外接的矩形势必会比较大
    w1, h1 = sprite.get_size()
    w, h = rotated_sprite.get_size()
    # 获得绘制图片的左上角（感谢pltc325网友的指正）
    sprite_draw_pos = Vec2d(sprite_pos.x-w/2, sprite_pos.y-h/2)
    screen.blit(rotated_sprite, sprite_draw_pos)

    # 图片的转向速度也需要和行进速度一样，通过时间来控制
    rotation_speed = steering_angle * (-velocity)  # 每秒转动的角度数（转速）
    if steering_pos != 0.: # 避免除零
        direction += (steering_pos/abs(steering_pos)) * rotation_speed * time_passed_seconds

    # 获得前进（x方向和y方向），这两个需要一点点三角的知识
    heading_x = sin(direction*pi/180.)
    heading_y = cos(direction*pi/180.)
    # 转换为单位速度向量
    heading = Vec2d(heading_x, heading_y)

    # 确定当前图片位置
    sprite_pos += heading * velocity * time_passed_seconds

    # 防止小鱼超出边框范围
    if sprite_pos.x < 0 + w1/2:
        sprite_pos.x = 0 + w1/2
        velocity = 0.
    elif sprite_pos.x > W - w1/2:
        sprite_pos.x = W - w1/2
        velocity = 0.
    if sprite_pos.y < 0 + h1/2:
        sprite_pos.y = 0 + h1/2
        velocity = 0.
    elif sprite_pos.y > H - h1/2 :
        sprite_pos.y = H - h1/2
        velocity = 0.
    
    # 显示信息
    font = pygame.font.SysFont("courier new", 24)  # 准备字号
    white = (255, 255, 255)
    red = (255, 30, 30)
    green = (30, 255, 30)
    blue = (60, 60, 255)
    orange = (255, 150, 30)
    # 显示车速
    text1 = font.render("SPEED: %d" % -velocity, True, white)
    # 显示纵向加速度
    if acc_real < acc_limit:
        text2 = font.render("ACC_LONGITUDE: %d" % max(acc_real, dec_real), True, white)
    else:
        text2 = font.render("ACC_LONGITUDE: %d" % max(acc_real, dec_real), True, red)
    # 显示横向加速度
    if acc_steer > acc_storage:
        if acc_steer >= acc_limit:
            text7 = font.render("ACC_LATERAL: %d" % acc_steer, True, red)
        else:
            text7 = font.render("ACC_LATERAL: %d" % acc_steer, True, orange)
    else:
        text7 = font.render("ACC_LATERAL: %d" % acc_steer, True, white)
    # 显示方向盘转角
    if steering_angle < steering_angle_limit:
        text8 = font.render("STEERING_ANGLE: %.2f" % steering_angle, True, white)
    else:
        text8 = font.render("STEERING_ANGLE: %.2f" % steering_angle, True, red)
    screen.blit(text1, (5, 5))
    screen.blit(text2, (175, 5))
    screen.blit(text7, (455, 5))
    screen.blit(text8, (715, 5))
    
    text3 = font.render("Thtottle: %.3f" % abs(throttle_pos), True, green)  # 显示油门状态
    text4 = font.render("Break:    %.3f" % abs(break_pos), True, red)  # 显示刹车状态
    text5 = font.render("Steering: %.3f" % -steering_pos, True, blue)  # 显示方向盘位置
    screen.blit(text3, (5, 35))
    screen.blit(text4, (5, 65))
    screen.blit(text5, (5, 95))
    
    # 显示倒挡
    if reverse:
        text_r = font.render("REVERSE", True, orange)
        screen.blit(text_r, (5, 125))

    pygame.display.update()
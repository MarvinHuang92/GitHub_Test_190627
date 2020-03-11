#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' description of this module '

__author__ = 'Marvin Huang'

background_image_filename = 'sushiplate.jpg'
sprite_image_filename = 'fugu.png'
 
import pygame
from pygame.locals import *
from sys import exit
from Vec2d import Vec2d
 
pygame.init()

global angle
angle = 0

screen = pygame.display.set_mode((640, 480), 0, 32)
 
background = pygame.image.load(background_image_filename).convert()
sprite = pygame.image.load(sprite_image_filename).convert_alpha()
rotated_sprite = pygame.transform.rotate(sprite, angle)
 
clock = pygame.time.Clock()
 
sprite_pos = Vec2d(200, 150)
sprite_speed = 300.
min_grid = 20.
 
while True:
 
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
 
    pressed_keys = pygame.key.get_pressed()
 
    key_direction = Vec2d(0, 0)
    if pressed_keys[K_LEFT]:
        angle = 90
        sprite_pos.y = int(sprite_pos.y / min_grid) * min_grid
        key_direction.x = -1
    elif pressed_keys[K_RIGHT]:
        angle = -90
        sprite_pos.y = int(sprite_pos.y / min_grid) * min_grid
        key_direction.x = +1
    if pressed_keys[K_UP]:
        angle = 0
        sprite_pos.x = int(sprite_pos.x / min_grid) * min_grid
        key_direction.y = -1
    elif pressed_keys[K_DOWN]:
        angle = 180
        sprite_pos.x = int(sprite_pos.x / min_grid) * min_grid
        key_direction.y = +1
 
    key_direction.normalize()
 
    screen.blit(background, (0,0))
    screen.blit(rotated_sprite, sprite_pos)
 
    time_passed = clock.tick(30)
    time_passed_seconds = time_passed / 1000.0
 
    sprite_pos += key_direction * sprite_speed * time_passed_seconds
 
    pygame.display.update()
# Drawing Rectangles
# Python 3.2

import pygame
from pygame.locals import *
from random import randint
pygame.init()
screen = pygame.display.set_mode((600,500))
pygame.display.set_caption("Drawing Rectangles")

pos_x = 300
pos_y = 250
vel_x = 0.
vel_y = 0.
acc = 0.0005
gravity = 0.0001

color = 200, 200, 255

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()

    screen.fill((0,0,200))
    
    # move the rectangle
    pos_x += vel_x
    pos_y += vel_y

    vel_y += gravity  # Gravity

    key = pygame.key.get_pressed()  # Controlled by user
    if key[K_LEFT]:
        vel_x -= acc
    if key[K_RIGHT]:
        vel_x += acc
    if key[K_UP]:
        vel_y -= acc
    if key[K_DOWN]:
        vel_y += acc

    
    # keep rectangle on the screen (rebound at border)
    if pos_x > 500 or pos_x < 0:
        vel_x = -vel_x
        new_color = randint(180, 255), randint(180, 255), randint(180, 255)
        color = new_color
    if pos_y > 400 or pos_y < 0:
        vel_y = -vel_y
        new_color = randint(180, 255), randint(180, 255), randint(180, 255)
        color = new_color
    
    # draw the rectangle
    width = 0  # solid fill
    pos = pos_x, pos_y, 100, 100
    pygame.draw.rect(screen, color, pos, width)
    
    pygame.display.update()


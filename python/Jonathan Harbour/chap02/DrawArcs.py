# Drawing Arcs
# Python 3.2

import math
import pygame
from pygame.locals import *
from random import randint


pygame.init()
screen = pygame.display.set_mode((600,500))
pygame.display.set_caption("Drawing Arcs")

screen.fill((0, 0, 0))

# draw the arc
for n in range(0,100):
    color = randint(0, 255), randint(0, 255), randint(0, 255)
    position = randint(0, 500), randint(0, 400), randint(50, 100), randint(50, 100)
    start_angle = math.radians(0)
    end_angle = math.radians(360)
    width = 2
    pygame.draw.arc(screen, color, position, start_angle, end_angle, width)

while True:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            sys.exit()

    
    pygame.display.update()


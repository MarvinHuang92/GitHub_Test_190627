# Bomb Catcher Game
# Chapter 4

import sys, random, time, pygame, math
from pygame.locals import *
from random import randint

def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))
    

#main program begins
pygame.init()
screen = pygame.display.set_mode((600,500))
pygame.display.set_caption("Bomb Catching Game")
font1 = pygame.font.Font(None, 24)
pygame.mouse.set_visible(True)
white = 255,255,255
red = 220, 50, 50
yellow = 230,230,50
black = 0,0,0

lives = 3
score = 0
clock_start = 0
game_over = True
mouse_x = mouse_y = 0

boom_time_set = False
boom_happened = False
time_boom_interval = 3
time_start = 0
time_current = 0

pos_x = 300
pos_y = 460

bomb_x = random.randint(0,500)
bomb_y = -50
vel_y = 0.7
vel_x = 0.

#repeating loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse_x,mouse_y = event.pos
            move_x,move_y = event.rel
        elif event.type == MOUSEBUTTONUP:
            if game_over:
                game_over = False
                lives = 3
                score = 0

    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()

    screen.fill((0,0,100))

    if game_over:
        print_text(font1, 100, 200, "<Click to Play, ESC to Exit>")
    else:
        #move the bomb
        bomb_y += vel_y
        bomb_x += vel_x

        if bomb_x < 0:
            vel_x = - vel_x
        elif bomb_x > 600-60:
            vel_x = - vel_x

        #has the player missed the bomb?
        if bomb_y > 500 and not boom_time_set:
            time_start = time.clock()
            boom_time_set = True

        elif bomb_y > 500 and boom_time_set and not boom_happened:
            time_current = time.clock() - time_start
            vel_x = 0.
            print_text(font1, bomb_x + 20, 500 - 130, "BOOM!")
            print_text(font1, bomb_x, 500 - 100, str(int(time_boom_interval - time_current)) + "s to restart")
            if time_current > time_boom_interval:
                boom_happened = True

        elif bomb_y > 500 and boom_happened:
            bomb_x = random.randint(0, 500)
            bomb_y = -50
            vel_x = randint(-5, 5) / 10
            lives -= 1
            if lives == 0:
                game_over = True
            boom_time_set = False
            boom_happened = False

        #see if player has caught the bomb
        elif bomb_y > pos_y:
            if bomb_x > pos_x and bomb_x < pos_x + 120:
                score += 10
                bomb_x = random.randint(0, 500)
                bomb_y = -50
                vel_x = randint(-5, 5) / 10


        #draw the bomb
        pygame.draw.circle(screen, black, (int(bomb_x)-4,int(bomb_y)-4), 30, 0)
        pygame.draw.circle(screen, yellow, (int(bomb_x),int(bomb_y)), 30, 0)
        #画引线
        random_color = randint(0,255), randint(0,255), randint(0,255)
        position = int(bomb_x), int(bomb_y)-50, 40, 40
        # angle = math.radians(90), math.radians(180) 这个是不好用的！两个角度必须分开，不能合成写作一个tuple
        pygame.draw.arc(screen, random_color, position, math.radians(90), math.radians(180), 3)

        #set basket position
        pos_x = mouse_x
        if pos_x < 0:
            pos_x = 0
        elif pos_x > 500:
            pos_x = 500
        #draw basket
        pygame.draw.rect(screen, black, (pos_x-4,pos_y-4,120,40), 0)
        pygame.draw.rect(screen, red, (pos_x,pos_y,120,40), 0)

    #print # of lives
    print_text(font1, 0, 0, "LIVES: " + str(lives))

    #print score
    print_text(font1, 500, 0, "SCORE: " + str(score))
    
    pygame.display.update()

    


import pygame, sys, time, random, math
from pygame.locals import *
class MySprite(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self) #基类的init方法
        self.target_surface = target
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0

    def _getx(self): return self.rect.x
    def _setx(self, value): self.rect.x =value
    X = property(_getx, _setx)

    def _gety(self): return self.rect.y
    def _sety(self, value): self.rect.y =value
    Y = property(_gety, _sety)



    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = 0,0,width,height
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=60):
        #更新动画帧
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = ( frame_x, frame_y, self.frame_width, self.frame_height )
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame


pygame.init()
screen = pygame.display.set_mode((850, 400), 0, 32)
pygame.display.set_caption("DMC9")
font = pygame.font.Font(None, 18)
framerate = pygame.time.Clock()

man = MySprite(screen)
man.load("HERM.png", 946, 400, 7)



group = pygame.sprite.Group()
group.add(man)

white = (255, 255, 255)
black = (0, 0, 0)
myfont = pygame.font.Font(None, 60)
image = myfont.render("Attack: J", True, white)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    '''screen.fill(black)
    screen.blit(image, (350, 200))
    pygame.display.update()'''

    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        exit()
    if key[pygame.K_j]:
        i = 1
        while i < 7:
            framerate.tick(10)
            ticks = pygame.time.get_ticks()
            group.update(ticks)
            group.draw(screen)
            pygame.display.update()
            i += 1






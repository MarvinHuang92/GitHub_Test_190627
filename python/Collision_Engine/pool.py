#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 桌球 ver 0.1 '

__author__ = 'Marvin Huang'

import pygame
import copy
from pygame.locals import *
from random import randint, choice
from Vec2d import Vec2d

SCREEN_SIZE = (1360, 768)
W = SCREEN_SIZE[0]
H = SCREEN_SIZE[1]
# 物体的数量
BALL_COUNT = 15
# 最大速度
S = 320

No_collision = 0 # 碰撞计数器
No_rebound = 0 # 边缘反弹计数器（这两个是全局变量，在内部引用时需要加global）

class World(object): # 世界地图
    def __init__(self):
        self.entities = {} # Store all the entities
        self.entity_id = 0 # Last entity id assigned
        # 画绿色背景
        self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill((30, 100, 0))
    def add_entity(self, entity):
        # 增加一个新的实体
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1
    def remove_entity(self, entity):
		# 删除一个实体
        del self.entities[entity.id]
    def get(self, entity_id):
        # 通过id给出实体，没有的话返回None
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None
    def process(self, time_passed):
        # 处理世界中的每一个实体
        time_passed_seconds = time_passed / 1000.0
        self.entities2 = copy.copy(self.entities)
		# 先把dict复制一份，对后者迭代，不然会改变原dict长度，导致报错
        for entity in self.entities2.values():
            entity.process(time_passed_seconds)
    def render(self, surface):
        # 绘制背景和每一个实体
        surface.blit(self.background, (0, 0))
        self.entities2 = copy.copy(self.entities)
        for entity in self.entities2.values():
            entity.render(surface)
    def collision(self, location, size, no, collision):
        # 碰撞判定，最后一个参数是碰撞体积是否开启
        self.entities2 = copy.copy(self.entities)
        for entity in self.entities2.values():
			# 先检查【对方不是自己】
            if no != entity.no:
                # 再检查是否有碰撞体积
                # if collision and entity.collision:
                # 获得自身到对方的距离向量
                vec_distance = entity.location - location
				# 获得距离向量的长度
                distance = vec_distance.get_length()
                if distance < (size + entity.size)/2:
                    return entity
        return None

class GameEntity(object): 
	# 游戏中所有对象基类
	# 具有若干通用属性（在init里面）
	# 只有两个通用方法：render和process
	# render就是绘画自身	
	# process就是一边think，一边移动
    def __init__(self, world, no):
        self.world = world
        self.no = no
        self.color = (0, 0, 0)
        self.location = Vec2d(0, 0)
        self.velocity = Vec2d(0.0, 0.0)
        self.collision = True # 默认有碰撞体积
        self.mass = 10
        self.size = 60
        self.id = 0
    def render(self, surface):
        x, y = self.location
        w = h = self.size
        pygame.draw.circle(surface, self.color, (int(x), int(y)), int(self.size/2))
    def process(self, time_passed):
        global No_collision
        other_ball = self.world.collision(self.location, self.size, self.no, self.collision)
		# 搜索可能的碰撞对象
        # 发生碰撞后，两个球的速度发生相应改变
        if other_ball is not None:
            vec_distance = other_ball.location - self.location
            d0 = vec_distance.x
            d1 = vec_distance.y
            v00 = self.velocity.x - other_ball.velocity.x
            v01 = self.velocity.y - other_ball.velocity.y

            r = (self.size**2)*0.95 # 最后的数字是补充碰撞时粘连带来的莫名其妙的速度损失
           
            #r = (vec_distance.get_length())**2
 
            # v10 = (d0**2*v00 - d0**2*v00 + d1**2*v00 + d1**2*v00 - 2.0*d0*d1*v01)/((d0**2 + d1**2)*2.0)
            #v10 = (d0**2*v00 - d0**2*v00 + d1**2*v00 + d1**2*v00 - 2.0*d0*d1*v01)/1000
            #v11 = (d0**2*v01 + d0**2*v01 + d1**2*v01 - d1**2*v01 - 2.0*d0*d1*v00)/1000
            #v20 = (2.0*d0*(d0*v00 + d1*v01))/1000
            #v21 = (2.0*v01*d1**2 + 2.0*d0*v00*d1)/1000
            
            v10 = (v00*d1*d1 - d0*v01*d1)/r
            v11 = (v01*d0*d0 - d1*v00*d0)/r
            v20 = (d0*d0*v00 + d0*d1*v01)/r
            v21 = (v01*d1*d1 + d0*v00*d1)/r


            self.location -= vec_distance*0.08 # 这个数字是为了防止两个球粘连，在碰撞时强制反向弹跳，数值越小越容易粘连
            other_ball.location += vec_distance*0.08
            self.velocity += Vec2d(v10 - v00, v11 - v01)
            other_ball.velocity += Vec2d(v20, v21)

            No_collision += 1

        # 增加屏幕边缘反弹
        global No_rebound
        if self.location.x < 0 + self.size/2:
            self.location.x = 0 + self.size/2
            self.velocity.x = - self.velocity.x
            No_rebound += 1
        if self.location.x > W - self.size/2:
            self.location.x = W - self.size/2
            self.velocity.x = - self.velocity.x
            No_rebound += 1
        if self.location.y < 0 + self.size/2:
            self.location.y = 0 + self.size/2
            self.velocity.y = - self.velocity.y
            No_rebound += 1
        if self.location.y > H - self.size/2:
            self.location.y = H - self.size/2
            self.velocity.y = - self.velocity.y
            No_rebound += 1
        # 每一步都要让移动的东西继续移动
        self.location += time_passed * self.velocity

# 游戏主进程
def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    world = World()
	# 这里定义的小写world变量名是一个实例，用来在后面传递给其他类
	# 当然，World类只有这一个实例
    w, h = SCREEN_SIZE
    clock = pygame.time.Clock()
    image = pygame.image.load("ball.png").convert_alpha()

    for ball_no in range(BALL_COUNT):
        ball = GameEntity(world, ball_no + 1)
        ball.location = Vec2d(randint(0, w), randint(0, h))
        ball.velocity = Vec2d(randint(-S, S), randint(-S, S))
        ball.color = (randint(180, 255), randint(120, 255), randint(180, 255))
        # ball.mass = randint(10, 200)
        # ball.size = randint(10, 50)
        # ball.brain.set_state("moving")
        world.add_entity(ball)
 
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
				# 让ESC也可以退出程序
        time_passed = clock.tick(60)
		# 可以改变帧率
 
        world.process(time_passed)
        world.render(screen)
        font = pygame.font.SysFont("arial", 16)
        text_surface1 = font.render('Total Collision: %d' % No_collision, True, (255, 255, 255))
        text_surface2 = font.render('Total Rebound: %d' % No_rebound, True, (255, 255, 255))
        screen.blit(text_surface1, (5, 5))
        screen.blit(text_surface2, (5, 25))
 
        pygame.display.update()

if __name__ == "__main__":
    run()
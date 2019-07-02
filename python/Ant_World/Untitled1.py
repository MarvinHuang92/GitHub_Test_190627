#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' description of this module '

__author__ = 'Marvin Huang'

import pygame
import copy
from pygame.locals import *
from random import randint, choice
from Vec2d import Vec2d

SCREEN_SIZE = (640, 480)
W = SCREEN_SIZE[0]
H = SCREEN_SIZE[1]
NEST_POSITION = (int(W/2) + randint(-int(W/3), int(W/3)), int(H/2) + randint(-int(H/3), int(H/3)))
ANT_COUNT = 20
NEST_SIZE = 80.

class State(): # 状态基类，空白（新的状态会成为它的子类）
    def __init__(self, name):
        self.name = name
    def do_actions(self): # 当前动作
        pass
    def check_conditions(self): # 状态转移关系
        pass
    def entry_actions(self): # 进入状态的动作
        pass
    def exit_actions(self): # 退出状态的动作
        pass

class StateMachine(): # 状态机
    def __init__(self):
        self.states = {}    # 存储状态
        self.active_state = None    # 当前有效状态
    def add_state(self, state):
        # 增加状态
        self.states[state.name] = state
    def think(self):
        if self.active_state is None:
            return
        # 所谓think包括两个部分：1执行有效状态的动作，2随时做转移状态检查
        self.active_state.do_actions()
        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)
    def set_state(self, new_state_name):
        # 更改状态，执行进入/退出动作
        if self.active_state is not None:
            self.active_state.exit_actions()
        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()

class World(object): # 世界地图
    def __init__(self):
        self.entities = {} # Store all the entities
        self.entity_id = 0 # Last entity id assigned
        # 画一个圈作为蚁穴
        self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill((200, 255, 200))
        pygame.draw.circle(self.background, (100, 255, 100), NEST_POSITION, int(NEST_SIZE))
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
    def get_close_entity(self, name, location, range=100.):
        # 通过一个范围寻找之内的所有实体
        location = Vec2d(*location)
        self.entities2 = copy.copy(self.entities)
        for entity in self.entities2.values():
            if entity.name == name:
                distance = location.get_distance(entity.location)
                if distance < range:
                    return entity
        return None

class GameEntity(object): 
	# 游戏中所有对象基类
	# 具有若干通用属性（在init里面）
	# 只有两个通用方法：render和process
	# render就是绘画自身，	# process就是一边think，一边向目标移动
	# ps：这里的process基本是描述的蚂蚁的动作，蜘蛛的process在它自己的类下重新定义了
    def __init__(self, world, name, image):
        self.world = world
        self.name = name
        self.image = image
        self.location = Vec2d(0, 0)
        self.destination = Vec2d(0, 0)
        self.speed = 0.
        self.brain = StateMachine()
        self.id = 0
    def render(self, surface):
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x-w/2, y-h/2))
    def process(self, time_passed):
        self.brain.think()
        if self.speed > 0 and self.location != self.destination:
            vector_to_destination = self.destination - self.location
            distance_to_destination = vector_to_destination.get_length()
            heading = vector_to_destination.normalized()
            travel_distance = min(distance_to_destination, time_passed * self.speed)
            self.location += travel_distance * heading

class Ant(GameEntity):
	# 第一个对象：蚂蚁
	# 具有1个新属性：carry_image，4个状态，3个方法：carry, drop, render
	# （这个render是通用的，可以不写，直接用基类里的，但是这里加强了一些）
	# 蚂蚁有4个状态，每个状态的速度不同，所以速度在状态里设置，而不在这里
    def __init__(self, world, image):
        # 执行基类构造方法
        GameEntity.__init__(self, world, "ant", image)
        # 创建各种状态
        exploring_state = AntStateExploring(self)
        seeking_state = AntStateSeeking(self)
        delivering_state = AntStateDelivering(self)
        hunting_state = AntStateHunting(self)
        self.brain.add_state(exploring_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(delivering_state)
        self.brain.add_state(hunting_state)
		# 新属性：搬运的那个东西
        self.carry_image = None
    def carry(self, image):
        self.carry_image = image
    def drop(self, surface):
        # 放下carry图像
        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x-w/2, y-h/2))
            self.carry_image = None
    def render(self, surface):
        # 先调用基类的render方法
        GameEntity.render(self, surface)
        # 额外绘制carry_image
        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x-w/2, y-h/2))

class Leaf(GameEntity): # 对象：叶子，没有任何新的状态和方法，毕竟不会动
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "leaf", image)
 
class Spider(GameEntity): 
	# 对象：蜘蛛，它没有状态，所以速度在这里直接设置好了
	# 具有生命值属性，速度是随机的
	# 具有bitten方法（被咬）
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "spider", image)
        self.dead_image = pygame.transform.flip(image, 0, 1)
        self.health = 25
        self.speed = 50. + randint(-20, 20)
 
    def bitten(self):
        self.health -= 1
        if self.health <= 0:
            self.speed = 0.
            self.image = self.dead_image
        self.speed = 140.
		# 一旦被咬，速度会加快
 
    def render(self, surface):
        GameEntity.render(self, surface)
        x, y = self.location
        w, h = self.image.get_size()
        bar_x = x - 12
        bar_y = y + h/2
        surface.fill( (255, 0, 0), (bar_x, bar_y, 25, 4))
        surface.fill( (0, 255, 0), (bar_x, bar_y, self.health, 4))
		# 具有生命槽
 
    def process(self, time_passed):
		# 部分修改了基类中的process
        x, y = self.location
        if x > SCREEN_SIZE[0] + 2:
            self.world.remove_entity(self)
			# 一旦超出屏幕，认为它消失了
            return
        GameEntity.process(self, time_passed)
		# 其余部分继承基类

# 下面是蚂蚁的4种State
# 每个State都包括当前动作、进出状态的动作、转移关系

# 蚂蚁的搜索
class AntStateExploring(State):
    def __init__(self, ant):
        State.__init__(self, "exploring")
        self.ant = ant
 
    def random_destination(self):
        w, h = SCREEN_SIZE
        self.ant.destination = Vec2d(randint(0, w), randint(0, h))    
		# 随机的目的地
 
    def do_actions(self):
        if randint(1, 20) == 1:
            self.random_destination()
			# 目的地刷新概率为20分之一，而不是随时刷新
 
    def check_conditions(self):
	# 状态转移条件
        leaf = self.ant.world.get_close_entity("leaf", self.ant.location)
		# 搜索所有名叫leaf的对象，范围是蚂蚁自身周围，半径取默认值100（在world里定义的）
        if leaf is not None:
            self.ant.leaf_id = leaf.id
			# 传递叶子的id
            return "seeking"
			# 发现叶子，进入seeking状态（外界信息以world属性输入）
        spider = self.ant.world.get_close_entity("spider", NEST_POSITION, NEST_SIZE)
		# 搜索所有名叫spider的对象，范围是NEST圆心周围，半径为NEST自身半径（而不是默认值）
        if spider is not None:
            if self.ant.location.get_distance(spider.location) < 100.:
				# 如果蚂蚁在距离蜘蛛100以内，才会去攻击蜘蛛
                self.ant.spider_id = spider.id
                return "hunting"
        return None
 
    def entry_actions(self):
		# 进入搜索状态时，设定一个速度
        self.ant.speed = 120. + randint(-30, 30)
        self.random_destination()

		# 没有退出状态的动作
 
# 蚂蚁的找叶子状态
class AntStateSeeking(State):
    def __init__(self, ant):
        State.__init__(self, "seeking")
        self.ant = ant
        self.leaf_id = None
		# 初始时没有叶子id，在上一个状态转入这个状态时，叶子id会被传递过来
 
    def check_conditions(self):
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf is None:
		# 必须一直检查叶子的id，才能发现叶子“不见了”
            return "exploring"
        if self.ant.location.get_distance(leaf.location) < 5.0:
			# 距离小于5px时认为可以carry一个叶子
            self.ant.carry(leaf.image)
            self.ant.world.remove_entity(leaf)
			# leaf被蚂蚁carry后就在world中消失了
            return "delivering"
        return None
 
    def entry_actions(self):
		# 发现叶子后，蚂蚁的的目的地会被锁定，速度也会增加
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf is not None:
            self.ant.destination = leaf.location
			# 锁定目的地
            self.ant.speed = 160. + randint(-20, 20)
			# 速度

# 蚂蚁的搬运
class AntStateDelivering(State):
    def __init__(self, ant):
        State.__init__(self, "delivering")
        self.ant = ant
 
    def check_conditions(self):
        if Vec2d(*NEST_POSITION).get_distance(self.ant.location) < NEST_SIZE:
			# 如果蚂蚁在NEST之内，有10分之一的概率会放下叶子（并不是一定会放下！）
            if (randint(1, 10) == 1):
                self.ant.drop(self.ant.world.background)# 括号里是目标surface
                return "exploring"
        return None
 
    def entry_actions(self):
		# 同样是速度和目的地两个因素的改变
        self.ant.speed = 60.
		# 搬东西会降低速度
        random_offset = Vec2d(randint(-20, 20), randint(-20, 20))
        self.ant.destination = Vec2d(*NEST_POSITION) + random_offset
		# 目的地：并不是直线回巢，有随机路线干扰
 
# 蚂蚁的狩猎
class AntStateHunting(State):
    def __init__(self, ant):
        State.__init__(self, "hunting")
        self.ant = ant
        self.got_kill = False
		# 这只蚂蚁是否击杀了蜘蛛
 
    def do_actions(self):
        spider = self.ant.world.get(self.ant.spider_id)
		# 获得蜘蛛的id，随时检查蜘蛛是否还存在着
        if spider is None:
            return
        self.ant.destination = spider.location
		# 锁定蜘蛛为目的地
        if self.ant.location.get_distance(spider.location) < 15.:
			# 距离低于15视为开战
            if randint(1, 5) == 1:
				# 蜘蛛被咬的概率5分之一
                spider.bitten()
                if spider.health <= 0:
                    self.ant.carry(spider.image)
					# 搬运蜘蛛尸体
                    self.ant.world.remove_entity(spider)
					# 从地图上删除蜘蛛
                    self.got_kill = True
					# 是这只蚂蚁杀死了蜘蛛，只有它会搬运尸体，其他的不会
 
    def check_conditions(self):
        if self.got_kill:
            return "delivering"
			# 击杀者负责搬运
        spider = self.ant.world.get(self.ant.spider_id)
		# 需要搬运对象的id
        if spider is None:
			# 蜘蛛丢失了（离开地图或被其他蚂蚁杀死），回到搜索
            return "exploring"
        if spider.location.get_distance(NEST_POSITION) > NEST_SIZE * 3:
			# 蜘蛛离开了NEST足够远
            return "exploring"
        return None
 
    def entry_actions(self):
        self.speed = 160. + randint(0, 50)
		# 只需要改变速度，目的地已经在上面定义过了
 
    def exit_actions(self):
        self.got_kill = False
		# 退出状态时，去掉击杀标志

# 游戏主进程
def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    world = World()
	# 这里定义的小写world变量名是一个实例，用来在后面传递给其他类
	# 当然，World类只有这一个实例
    w, h = SCREEN_SIZE
    clock = pygame.time.Clock()
    ant_image = pygame.image.load("ant.png").convert_alpha()
    leaf_image = pygame.image.load("leaf.png").convert_alpha()
    spider_image = pygame.image.load("spider.png").convert_alpha()
 
    for ant_no in range(ANT_COUNT):
        ant = Ant(world, ant_image)
        ant.location = Vec2d(randint(0, w), randint(0, h))
		# 随机放置每只蚂蚁的位置
        ant.brain.set_state("exploring")
		# 默认是搜索状态
        world.add_entity(ant)
		# 一个一个添加蚂蚁们
 
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
				# 让ESC也可以退出程序
        time_passed = clock.tick(30)
		# 可以改变帧率
 
        if randint(1, 10) == 1:
            leaf = Leaf(world, leaf_image)
            leaf.location = Vec2d(randint(0, w), randint(0, h))
            world.add_entity(leaf)
			# 10分之一概率掉落新的叶子（是不是概率太大了？）
 
        if randint(1, 100) == 1:
            spider = Spider(world, spider_image)
            spider.location = Vec2d(-50, randint(0, h))
            spider.destination = Vec2d(w+50, randint(0, h))
            world.add_entity(spider)
			# 100分之一概率产生蜘蛛
			# 蜘蛛总是从屏幕左侧-50处出发，走向屏幕右侧
 
        world.process(time_passed)
        world.render(screen)
 
        pygame.display.update()
 
if __name__ == "__main__":
    run()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""坦克大战复刻版 ver 0.2"""

__author__ = 'Marvin Huang'

import pygame
import time
import copy
from pygame.locals import *
from sys import exit
from random import randint
from Vec2d import Vec2d

SCREEN_SIZE = (900, 624)
W = SCREEN_SIZE[0]
H = SCREEN_SIZE[1]

# 战场尺寸
BATTLEFIELD = (624, 624)
Bx = BATTLEFIELD[0]
By = BATTLEFIELD[1]

# 计分板尺寸
BB_SIZE = (W - Bx, By)
BW = BB_SIZE[0]
BH = BB_SIZE[1]

# TR地形最小单位边长（像素）
# TK坦克和基地边长
TR = 12
TK = 48

# 基地位置
BASE_POSITION = (Bx/2 - TK/2, By - TK)
BASEx = BASE_POSITION[0]
BASEy = BASE_POSITION[1]

# 敌人的数量
ENEMY_COUNT = 16
ENEMY_COUNT2 = int(0.003*randint(0, 100)*ENEMY_COUNT)
ENEMY_COUNT3 = int(0.003*randint(0, 100)*ENEMY_COUNT)
ENEMY_COUNT4 = int(0.003*randint(0, 100)*ENEMY_COUNT)
ENEMY_COUNT1 = ENEMY_COUNT - ENEMY_COUNT2 - ENEMY_COUNT3 - ENEMY_COUNT4

# 奖励出现的概率
bonus_prob = 1000

# 记分牌的内容（全局变量）
GAMEOVER = False
ENEMY_NUMBER = ENEMY_COUNT  # 剩余敌人的数目
TIME = 0.
CANON_AMOUNT = 0

# 以下State和StateMachine两个类是不变的，只改变后续的就可以


class State:  # 状态基类，空白（新的状态会成为它的子类）
    def __init__(self, name):
        self.name = name

    def do_actions(self):  # 当前动作
        pass

    def check_conditions(self):  # 状态转移关系
        pass

    def entry_actions(self):  # 进入状态的动作
        pass

    def exit_actions(self):  # 退出状态的动作
        pass


class StateMachine:  # 状态机
    def __init__(self):
        self.states = {}    # 存储状态，这是一个目录dict
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
            self.active_state.exit_actions()  # 如果有当前动作，执行它的后摇
        self.active_state = self.states[new_state_name]  # 然后将当前动作更改
        self.active_state.entry_actions()  # 执行新动作的前摇


class World(object):  # 世界地图
    def __init__(self):
        self.entities = {}  # 存储所有的实例
        self.entities2 = {}  # 备用目录
        self.entity_id = 0  # 上一个实例的编号
        # 画黑色背景
        self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill((0, 0, 0))
        # 画计分板
        pygame.draw.rect(self.background, (180, 180, 180), (Bx, 0, BB_SIZE[0], BB_SIZE[1]))
        # 画基地的【位置】，但并没有添加真正的基地上去
        pygame.draw.rect(self.background, (255, 255, 255), (BASEx, BASEy, TK, TK))

# 以下几个方法是通用的

    def add_entity(self, entity):  # 增加一个新的实体
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):  # 删除一个实体
        del self.entities[entity.id]

    def get(self, entity_id):  # 通过id给出实体，没有的话返回None
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None

    def process(self, time_passed):  # 处理世界中的每一个实体
        time_passed_seconds = time_passed / 1000.0 * 1.5  # 时间加速器
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

# 额外的方法

    def collision(self, name, location, direction, size, id):
        # 碰撞判定
        # 这里的entity可以表示对方，但self是指world而不是我自己，所以自己的值全都需要传入：位置、方向、尺寸和id
        location = Vec2d(*location)  # 传入的值可能不符合Vec2d格式，这里规范一下
        direction = Vec2d(*direction)
        self.entities2 = copy.copy(self.entities)
        for entity in self.entities2.values():
            # 先检查对方不是自己！
            if id != entity.id:
                # 是否有碰撞体积
                if (name in ("tank_user", "tank_enemy") and entity.collision_to_tank)\
                        or (name == "canon" and entity.collision_to_canon):  # 注意分类的集合，不重复也不缺少
                    # 获得自身到对方的距离向量
                    distance = entity.location - location
                    # 获得距离向量到自身朝向的投影
                    proj_x = distance.projection(direction)
                    # 距离向量到自身侧向的投影
                    proj_y = distance.projection(direction.perpendicular())
                    if proj_y.get_length() < (size + entity.size - 4)/2:  # 这里标量化了，不用担心方向，-4是为了让侧面不容易被卡住
                        if direction.dot(proj_x) > 0:  # dot表示点积，确保是向前的
                            if proj_x.get_length() < (size + entity.size)/2:
                                return entity
        return None

# 下面定义所有的对象类


class GameEntity(object):
    # 游戏中所有对象基类, 具有若干通用属性（在init里面）
    # 只有两个通用方法：render和process: render就是绘画自身, process包括调用state的think，和执行其他的通用动作两部分
    def __init__(self, world, name, image):  # 定义通用属性，每一个都要赋予初始值
        self.world = world
        self.name = name
        self.image = image
        self.id = 0
        self.location = Vec2d(0, 0)  # 赋予初值，但是没什么意义，只是表示存在这个属性，后面还要修改
        self.speed = 0.
        self.direction = Vec2d(0, -1)  # 默认是朝下的（敌人）
        self.hp = 1  # 所有对象默认生命值 = 1
        self.size = TK
        self.invincible = False  # 默认不是无敌的
        self.collision_to_tank = True  # 默认对坦克有碰撞体积
        self.collision_to_canon = True  # 默认对炮弹有碰撞体积
        self.flag = 0  # 所属阵营（0表示中立，1表示玩家，2表示敌人）
        self.brain = StateMachine()

    def render(self, surface):
        angle = -self.direction.get_angle() - 90
        rotated_image = pygame.transform.rotate(self.image, angle)
        x, y = self.location
        w, h = rotated_image.get_size()
        surface.blit(rotated_image, (x-w/2, y-h/2))

    def process(self, time_passed):
        self.brain.think()
        # 这里的think可以在后面的各个state里面定义内容
        # 也可以定义一些在state之外的通用动作，或者不定义，全都放在state的think里面
        # 通常，每一步都要让可以移动的东西继续移动
        if self.speed > 0:
            self.location += time_passed * self.speed * self.direction

    def got_shot(self):  # 如果被击中，会触发此动作,但默认没有效果，对于基地等特殊对象才有效果
        pass


class Tank(GameEntity):
    # 坦克大类（包括玩家和敌人）
    # 具有的新属性：炮弹速度、炮弹库存、转弯和开火的概率，新方法：开炮fire，转向turn
    # 3个状态：前进going、停止stopping、被玩家控制controlled，在后面详细设置
    def __init__(self, world, name, image):  # 这里容易混淆，这一行的name是外界传入的
        # 执行基类构造方法
        GameEntity.__init__(self, world, name, image)  # 这里的name是上面那行传过来的，world同理
        # 创建各种状态
        going_state = TankStateGoing(self)
        stopping_state = TankStateStopping(self)
        controlled_state = TankStateControlled(self)
        self.brain.add_state(going_state)
        self.brain.add_state(stopping_state)
        self.brain.add_state(controlled_state)
        # 所有坦克默认速度48（每秒移动一个车身长度）
        self.normal_speed = 48  # 额定的速度
        self.speed = self.normal_speed  # 实际速度（可能不等于额定速度哦）
        # 新属性：炮弹速度、炮弹库存、转弯和开火的概率
        self.canon_speed = 120
        self.canon_amount = 100
        self.turning_prob = 25  # 实际上是它的倒数，prob表示probability
        self.fire_prob = 50
        self.overheat = False  # 所谓过热，上一个炮弹还在飞行时，不能开炮

    # 定义开火动作
    def fire(self):
        if not self.overheat:
            if self.canon_amount > 0:
                canon_image = pygame.image.load("canon.png").convert_alpha()
                canon = Canon(self.world, canon_image)  # 建立一个实例
                canon.brain.set_state("flying")
                canon.shooter = self  # 记录炮弹的发射者
                canon.location = self.location + self.direction * (TK / 2)
                canon.direction = self.direction
                canon.flag = self.flag  # 阵营和发射者的阵营相同
                canon.speed = self.canon_speed  # 速度由发射者赋予它
                self.world.add_entity(canon)  # 向世界添加炮弹，并使发射者的炮弹库存减少1，且进入过热状态
                self.canon_amount -= 1
                self.overheat = True

    # 定义拐弯
    def turn(self):
        a = randint(1, 5)  # 随机数决定拐弯方向
        if a == 1 or a == 2:
            self.direction = self.direction.perpendicular()
        elif a == 3 or a == 4:
            self.direction = - self.direction.perpendicular()
        else:
            self.direction = - self.direction


class TankUser(Tank):  # 玩家的坦克
    def __init__(self, world, image):  # 这里少了name属性，因为单个的个体不需要区分name，只是一类坦克整体有name
        # 首先继承父类的构造方法
        Tank.__init__(self, world, "tank_user", image) # 这里的name被固定下来，作为每一个创建的对象的标记
        # 对和父类不同的属性进行修改
        self.canon_amount = 40
        self.canon_speed = 240
        self.flag = 1

    def got_shot(self):
        global GAMEOVER
        time.sleep(0.2)  # 延迟0.2秒，注意使用前要先import time
        GAMEOVER = True


class TankEnemy1(Tank):  # 第一类敌人，所有属性都是默认的
    def __init__(self, world, image):
        Tank.__init__(self, world, "tank_enemy", image)  # 四类敌人都统称为tank_enemy，这里就不再建一个敌人大类了
        self.flag = 2


class TankEnemy2(Tank):  # 第二类敌人（高速装甲车，靠撞击造成伤害，每0.5秒撞击一次，防止连续伤害）
    def __init__(self, world, image):
        Tank.__init__(self, world, "tank_enemy", image)
        self.canon_amount = 0  # 禁止开炮
        self.normal_speed = 120  # 移动速度比其它坦克快
        self.flag = 2

    def collide(self):  # 撞击动作，和canon的动作类似，后面补充
        pass


class TankEnemy3(Tank):  # 第三类敌人，开炮比较快
    def __init__(self, world, image):
        Tank.__init__(self, world, "tank_enemy", image)
        self.canon_speed = 240  # 炮弹速度比其它坦克快一倍
        self.flag = 2


class TankEnemy4(Tank):  # 第四类敌人，4重装甲，受伤有加成，有生命槽
    def __init__(self, world, image):
        Tank.__init__(self, world, "tank_enemy", image)
        self.hp = 4
        self.flag = 2

    # 受伤加成
    def got_shot(self):
        if self.hp > 1:
            self.normal_speed += 36
            self.canon_speed += 48
            self.canon_amount += 5

    # 具有生命槽，长32，宽4，与坦克本身有10的空隙
    def render(self, surface):
        Tank.render(self, surface)
        x, y = self.location
        w, h = self.image.get_size()
        bar_x = x - 16
        bar_y = y - h / 2 - 10
        surface.fill((255, 0, 0), (bar_x, bar_y, 32, 4))
        surface.fill((0, 255, 0), (bar_x, bar_y, 8 * self.hp, 4))


class Terran(GameEntity):  # 地形对象，不可以动，中立阵营
    def __init__(self, world, name, image):  # 这不是最低级class，所以不能定义确定的name，等待传入
        self.name = name
        GameEntity.__init__(self, world, name, image)
        self.flag = 0  # 虽然默认也是0，但还是保险一些啦


class Base(Terran):  # 基地
    def __init__(self, world, image):  # 最低一级的class在__init__中定义name属性
        Terran.__init__(self, world, "base", image)
        self.flag = 0  # 并不是属于玩家阵营的，玩家也可以自己摧毁它

    def got_shot(self):  # 如果被击中，会导致游戏结束
        global GAMEOVER  # 引用全局变量的声明
        time.sleep(0.2)  # 延迟0.2秒，注意使用前要先import time
        GAMEOVER = True


class Wall(Terran):  # 墙，尺寸只有12
    def __init__(self, world, image):
        Terran.__init__(self, world, "wall", image)
        self.size = TR


class Iron(Terran):  # 铁皮，无敌的，尺寸12
    def __init__(self, world, image):
        Terran.__init__(self, world, "iron", image)
        self.size = TR
        self.invincible = True


class Forrest(Terran):  # 树，没有碰撞体积
    def __init__(self, world, image):
        Terran.__init__(self, world, "forrest", image)
        self.collision_to_tank = False
        self.collision_to_canon = False


class River(Terran):  # 河水，没有炮弹碰撞体积
    def __init__(self, world, image):
        Terran.__init__(self, world, "river", image)
        self.collision_to_canon = False


class Border(Terran):  # 屏幕边界，是无敌的
    def __init__(self, world, image):
        Terran.__init__(self, world, "border", image)
        self.invincible = True


class Bonus(Terran):  # 奖励包，没有炮弹碰撞体积
    def __init__(self, world, image):
        Terran.__init__(self, world, "bonus", image)
        self.size = 32
        self.collision_to_canon = False


class Canon(GameEntity):  # 炮弹类
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "canon", image)
        # 创建各种状态
        flying_state = CanonStateFlying(self)
        self.brain.add_state(flying_state)
        self.size = TR
        self.invincible = True  # 无敌的，不会被摧毁
        self.collision_to_canon = False  # 不会撞上其他的炮弹
        self.shooter = None  # 炮弹的发射者


# 下面定义所有的状态STATE

class CanonStateFlying(State):  # 炮弹的飞行状态，只有中途动作，因为只有这一个状态，没有进出动作
    def __init__(self, canon):
        State.__init__(self, "flying")
        self.canon = canon

    def do_actions(self):  # 唯一的动作，撞上什么东西然后爆炸
        goal = self.canon.world.collision("canon", self.canon.location, self.canon.direction, TR, self.canon.id)
        if goal is not None:
            self.canon.world.remove_entity(self.canon)
            self.canon.shooter.overheat = False  # 炮弹发射者解除过热状态
            if self.canon.flag != goal.flag and not goal.invincible:
                goal.hp -= 1
                goal.got_shot()
                if goal.hp <= 0:
                    if goal.name == "tank_enemy":
                        global ENEMY_NUMBER
                        ENEMY_NUMBER -= 1
                    self.canon.world.remove_entity(goal)


class TankStateGoing(State):  # 包括完整的中途动作、转移条件、进出动作
    def __init__(self, tank):
        State.__init__(self, "going")
        self.tank = tank

    def do_actions(self):  # 随机的转向和开火
        self.tank.speed = self.tank.normal_speed
        if randint(1, self.tank.fire_prob) == 1:
            self.tank.fire()
        if randint(1, self.tank.turning_prob) == 1:
            self.tank.turn()

    def check_conditions(self):  # 撞到什么东西，进入stopping状态
        goal = self.tank.world.collision("tank_enemy", self.tank.location, self.tank.direction, TK, self.tank.id)
        if goal is not None:
            if goal.name == "bonus":
                self.tank.world.remove_entity(goal)  # 如果撞到的东西是bonus，就去掉它，并给自己加速（假设所有的bonus都是加速器）
                self.tank.normal_speed += 48
            return "stopping"
        return None

    def entry_actions(self):  # 进入动作，当然这也可以放进do_action里面去
        self.tank.turning_prob = 25


class TankStateStopping(State):
    def __init__(self, tank):
        State.__init__(self, "stopping")
        self.tank = tank

    def do_actions(self):  # 同样是随机的转向和开火，但不能移动了
        self.tank.speed = 0
        if randint(1, self.tank.fire_prob) == 1:
            self.tank.fire()
        if randint(1, self.tank.turning_prob) == 1:
            self.tank.turn()

    def check_conditions(self):
        goal = self.tank.world.collision("tank_enemy", self.tank.location, self.tank.direction, TK, self.tank.id)
        if goal is None:
            return "going"
        return None

    def entry_actions(self):  # 进入动作，当然这也可以放进do_action里面去
        self.tank.turning_prob = 10


class TankStateControlled(State):
    def __init__(self, tank):
        State.__init__(self, "controlled")
        self.tank = tank

    def do_actions(self):
        goal = self.tank.world.collision("tank_user", self.tank.location, self.tank.direction, TK, self.tank.id)
        # 控制方向，and遇到阻挡会停下来
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.tank.direction = Vec2d(-1, 0)
            if goal is None:
                self.tank.speed = self.tank.normal_speed
            elif goal.name == "bonus":
                self.tank.world.remove_entity(goal)  # 如果撞到的东西是bonus，就去掉它，并给自己加速（假设所有的bonus都是加速器）
                self.tank.normal_speed += 48
                self.tank.canon_amount += 15
            else:
                self.tank.speed = 0  # 如果撞到别的东西，就停下来
        elif pressed_keys[K_RIGHT]:
            self.tank.direction = Vec2d(1, 0)
            if goal is None:
                self.tank.speed = self.tank.normal_speed
            elif goal.name == "bonus":
                self.tank.world.remove_entity(goal)
                self.tank.normal_speed += 48
                self.tank.canon_amount += 15
            else:
                self.tank.speed = 0
        elif pressed_keys[K_UP]:
            self.tank.direction = Vec2d(0, -1)
            if goal is None:
                self.tank.speed = self.tank.normal_speed
            elif goal.name == "bonus":
                self.tank.world.remove_entity(goal)
                self.tank.normal_speed += 48
                self.tank.canon_amount += 15
            else:
                self.tank.speed = 0
        elif pressed_keys[K_DOWN]:
            self.tank.direction = Vec2d(0, 1)
            if goal is None:
                self.tank.speed = self.tank.normal_speed
            elif goal.name == "bonus":
                self.tank.world.remove_entity(goal)
                self.tank.normal_speed += 48
                self.tank.canon_amount += 15
            else:
                self.tank.speed = 0
        else:
            self.tank.speed = 0
        # 控制开火
        if pressed_keys[K_SPACE]:
            self.tank.fire()


# 游戏主进程

def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    pygame.display.set_caption('Tank Battle v0.3')  # pygame下的窗口标题，和python主体的设置方法不一样
    world = World()  # 这里定义的小写world变量名是一个实例，用来在后面传递给其他类。当然，World类只有这一个实例
    w, h = BATTLEFIELD
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
    bonus_image = pygame.image.load("bonus.png").convert_alpha()
 
    # 放置玩家坦克
    tank_user = TankUser(world, tank_user_image)
    tank_user.location = Vec2d(100, h - TK / 2)
    tank_user.brain.set_state("controlled")
    world.add_entity(tank_user)
    global CANON_AMOUNT
    CANON_AMOUNT = tank_user.canon_amount

    # 放置敌人坦克
    for enemy_no in range(ENEMY_COUNT1):
        tank_enemy1 = TankEnemy1(world, tank_enemy1_image)
        # 建立实例
        tank_enemy1.location = Vec2d(randint(0, w), randint(0, 2 * h / 3))
        # 随机放置位置
        tank_enemy1.brain.set_state("going")
        # 默认状态
        world.add_entity(tank_enemy1)
        # 一个一个添加它们

    for enemy_no in range(ENEMY_COUNT2):
        tank_enemy2 = TankEnemy2(world, tank_enemy2_image)
        tank_enemy2.location = Vec2d(randint(0, w), randint(0, 2 * h / 3))
        tank_enemy2.brain.set_state("going")
        world.add_entity(tank_enemy2)

    for enemy_no in range(ENEMY_COUNT3):
        tank_enemy3 = TankEnemy3(world, tank_enemy3_image)
        tank_enemy3.location = Vec2d(randint(0, w), randint(0, 2 * h / 3))
        tank_enemy3.brain.set_state("going")
        world.add_entity(tank_enemy3)

    for enemy_no in range(ENEMY_COUNT4):
        tank_enemy4 = TankEnemy4(world, tank_enemy4_image)
        tank_enemy4.location = Vec2d(randint(0, w), randint(0, 2 * h / 3))
        tank_enemy4.brain.set_state("going")
        world.add_entity(tank_enemy4)

    # 放置地形
    wall_location = []  # 先创建一个空的list
    for x in range (100, 601, 12):
        for y in range (80, 501, 108):
            z = (x, y)
            wall_location.append(z)
    for pos in wall_location:
        wall = Wall(world, wall_image)
        wall.location = Vec2d(*pos)
        world.add_entity(wall)

    iron_location = [(BASEx, 520), (BASEx + 12, 520), (BASEx + 24, 520), (BASEx + 36, 520), (BASEx + 48, 520),
                     (6, 360), (18, 360), (30, 360), (w-6, 360), (w-18, 360), (w-30, 360)]
    for pos in iron_location:
        iron = Iron(world, iron_image)
        iron.location = Vec2d(*pos)
        world.add_entity(iron)

    base = Base(world, base_image)
    base.location = (BASEx + TK / 2, BASEy + TK / 2)
    world.add_entity(base)
 
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

        seconds = time_passed / 1000.
        global TIME
        TIME += seconds
        # 记录时间

        # 随机时间和地点出现奖励
        if randint(1, bonus_prob) == 1:
            bonus = Bonus(world, bonus_image)
            bonus.location = Vec2d(randint(0, w), randint(0, h))
            world.add_entity(bonus)

        # 防止坦克和炮弹（会移动的东西）超出边框范围
        world.entities2 = copy.copy(world.entities)
        for entity in world.entities2.values():
            if entity.name == "tank_user" or entity.name == "tank_enemy":  # 如果是坦克，就停止移动
                if entity.location.x < 0 + TK / 2:
                    entity.location.x = 0 + TK / 2
                if entity.location.x > BATTLEFIELD[0] - TK / 2:
                    entity.location.x = BATTLEFIELD[0] - TK / 2
                if entity.location.y < 0 + TK / 2:
                    entity.location.y = 0 + TK / 2
                if entity.location.y > BATTLEFIELD[1] - TK / 2:
                    entity.location.y = BATTLEFIELD[1] - TK / 2
            if entity.name == "canon": # 如果是炮弹，就直接消失
                if entity.location.x < 0 + TR / 2:
                    world.remove_entity(entity)
                    entity.shooter.overheat = False  # 炮弹发射者解除过热状态
                if entity.location.x > BATTLEFIELD[0] - TR / 2:
                    world.remove_entity(entity)
                    entity.shooter.overheat = False  # 炮弹发射者解除过热状态
                if entity.location.y < 0 + TR / 2:
                    world.remove_entity(entity)
                    entity.shooter.overheat = False  # 炮弹发射者解除过热状态
                if entity.location.y > BATTLEFIELD[1] - TR / 2:
                    world.remove_entity(entity)
                    entity.shooter.overheat = False  # 炮弹发射者解除过热状态

        # 随时刷新炮弹库存
        world.entities2 = copy.copy(world.entities)
        for entity in world.entities2.values():
            if entity.name == "tank_user":
                CANON_AMOUNT = entity.canon_amount  # 这里又不用声明全局变量了，在run()里只要声明一次就可以了

        world.process(time_passed)
        world.render(screen)

        # 显示计分板信息
        font = pygame.font.SysFont(None, 24)  # 准备小字号
        font3 = pygame.font.SysFont(None, 48)  # 准备大字号
        text_surface1 = font.render('Time: %d' % TIME, True, (255, 255, 255))  # 显示时间
        text_surface2 = font.render('Enemies: %d' % ENEMY_NUMBER, True, (255, 255, 255))  # 显示剩余敌人数量
        text_surface3 = font3.render('YOU WIN!', True, (255, 255, 255))
        text_surface4 = font3.render('GAME OVER!', True, (255, 255, 255))
        text_surface5 = font.render('Canons: %d' % CANON_AMOUNT, True, (255, 255, 255))  # 显示剩余弹药
        screen.blit(text_surface1, (BATTLEFIELD[0] + 15, 5))
        screen.blit(text_surface2, (BATTLEFIELD[0] + 15, 35))
        screen.blit(text_surface5, (BATTLEFIELD[0] + 15, 65))
        if ENEMY_NUMBER == 0:
            screen.blit(text_surface3, (BATTLEFIELD[0] + 65, 125))
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_SPACE]:
                exit()
        if GAMEOVER:
            screen.blit(text_surface4, (BATTLEFIELD[0] + 35, 125))
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_SPACE]:
                exit()

        pygame.display.update()


if __name__ == "__main__":
    run()

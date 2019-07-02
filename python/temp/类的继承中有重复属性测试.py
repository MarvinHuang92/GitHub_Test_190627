#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' description of this module '

__author__ = 'Marvin Huang'


# 首先定义基类，有两个属性，名字，性别
class Person(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender


# 定义子类，引用super中的名字和性别，但加入新的属性course
class Teacher(Person):
    def __init__(self, name, gender, course):
        super(Teacher, self).__init__(name, gender)
        # 这里的super里面有字，是为了在多继承中区分来自哪一个父类的属性
        # 如果是单继承，可以直接写成super().__init__(name, gender)
        self.course = course


t = Teacher('Alice', 'Female', 'English')
print(t.name)
print(t.course)


# 以下是自己的测试：
class C1(object):
    def __init__(self, name):  # 只看name这一个属性
        self.name = name

    def print_name(self):  # 再定义一个方法，简单的打印出自己的名字
        print("This is " + self.name)


class C2(C1):
    def __init__(self):
        super().__init__("class 2")


class C3(C1):
    def __init__(self, name):  # C3和C2，都是C1的子类，这一行的name是外界传入的（这是唯一的一个接口）
        super().__init__(name)  # 这一行的name来自上一行，而不是外界传入的

c1 = C1("class 1")
c2 = C2()
c3 = C3("class 3")
c1.print_name()
c2.print_name()
c3.print_name()

if c2.name == "class 1":
    print("c2 is class 1")
elif c2.name == "class 2":
    print("c2 is class 2")

# 检查每一个类的name是什么

class GameEntity(object):
    # 游戏中所有对象基类, 具有若干通用属性（在init里面）
    # 只有两个通用方法：render和process: render就是绘画自身, process包括调用state的think，和执行其他的通用动作两部分
    def __init__(self, world, name, image):  # 定义通用属性，每一个都要赋予初始值
        self.world = world
        self.name = name
        self.image = image


class Tank(GameEntity):
    # 坦克大类（包括玩家和敌人）
    # 具有的新属性：炮弹速度、炮弹库存、转弯和开火的概率，新方法：开炮fire，转向turn
    # 3个状态：前进going、停止stopping、被玩家控制controlled，在后面详细设置
    def __init__(self, world, name, image):
        # 执行基类构造方法
        GameEntity.__init__(self, world, name, image)
        # 创建各种状态




class TankUser(Tank):  # 玩家的坦克
    def __init__(self, world, image):  # 这里少了name属性，因为单个的个体不需要区分name，只是一类坦克整体有name
        # 首先继承父类的构造方法
        Tank.__init__(self, world, "tank_user", image)
        # 对和父类不同的属性进行修改
        self.canon_amount = 100
        self.canon_speed = 240
        self.flag = 1



class TankEnemy1(Tank):  # 第一类敌人，所有属性都是默认的
    def __init__(self, world, image):
        Tank.__init__(self, world, "tank_enemy1", image)
        self.flag = 2


class TankEnemy2(Tank):  # 第二类敌人（高速装甲车，靠撞击造成伤害，每0.5秒撞击一次，防止连续伤害）
    def __init__(self, world, image):
        Tank.__init__(self, world, "tank_enemy2", image)
        self.canon_amount = 0  # 禁止开炮
        self.normal_speed = 120  # 移动速度比其它坦克快
        self.flag = 2




class TankEnemy3(Tank):  # 第三类敌人，开炮比较快
    def __init__(self, world, image):
        Tank.__init__(self, world, "tank_enemy3", image)
        self.canon_speed = 240  # 炮弹速度比其它坦克快一倍
        self.flag = 2


class TankEnemy4(Tank):  # 第四类敌人，4重装甲，受伤有加成，有生命槽
    def __init__(self, world, image):
        Tank.__init__(self, world, "tank_enemy4", image)
        self.hp = 4
        self.flag = 2




class Terran(GameEntity):  # 地形对象，不可以动，中立阵营
    def __init__(self, world, name, image):
        GameEntity.__init__(self, world, name, image)
        self.flag = 0  # 虽然默认也是0，但还是保险一些啦


class Base(Terran):  # 基地
    def __init__(self, world, image):  # 最低一级的class都不需要name属性，但是带着也没关系
        Terran.__init__(self, world, "base", image)
        self.flag = 0  # 并不是属于玩家阵营的，玩家也可以自己摧毁它



class Wall(Terran):  # 墙，尺寸只有12
    def __init__(self, world, image):
        Terran.__init__(self, world, "wall", image)



class Iron(Terran):  # 铁皮，无敌的，尺寸12
    def __init__(self, world, image):
        Terran.__init__(self, world, "iron", image)



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
        self.collision_to_canon = False


class Canon(GameEntity):  # 炮弹类
    def __init__(self, world, image):
        GameEntity.__init__(self, world, "canon", image)
        # 创建各种状态


world = 0
image = 1

tankuser = TankUser(world, image)
tankenemy1 = TankEnemy1(world, image)
tankenemy2 = TankEnemy2(world, image)
tankenemy3 = TankEnemy3(world, image)
tankenemy4 = TankEnemy4(world, image)
base = Base(world, image)
wall = Wall(world, image)
iron = Iron(world, image)
forrest = Forrest(world, image)
river = River(world, image)
border = Border(world, image)
bonus = Bonus(world, image)
canon = Canon(world, image)


print(base.name)
print(tankenemy1.name)
print(canon.name)

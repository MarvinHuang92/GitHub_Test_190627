#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' description of this module '

__author__ = 'Marvin Huang'

class Student(object):
    count = 0

    def __init__(self, name):
        self.name = name
        Student.count += 1
        # __init__本质是每次添加新的实例时就会调用
        # 所以一切与新加实例相关的都可以写在它的下面


# 测试:
if Student.count != 0:
    print('测试失败!')
else:
    bart = Student('Bart')
    if Student.count != 1:
        print('测试失败!')
    else:
        lisa = Student('Bart')
        if Student.count != 2:
            print('测试失败!')
        else:
            print('Students:', Student.count)
            print('测试通过!')



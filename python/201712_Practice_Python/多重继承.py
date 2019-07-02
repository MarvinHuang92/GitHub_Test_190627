#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' description of this module '

__author__ = 'Marvin Huang'

class Animal(object):
    pass
class Mammal(Animal):
    def mammal(self):
        print('it is a mammal')
class FlyableMixIn(object):
    def fly(self):
        print('it is flyable')
class Bat(Mammal,FlyableMixIn):
    def __init__(self):
        print('it is a bat')



bat=Bat()
bat.fly()
bat.mammal()

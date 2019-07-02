#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' description of this module '

__author__ = 'Marvin Huang'

from Vec2d import *

right = Vec2d(1, 0)
left = Vec2d(-1, 0)
up = Vec2d(0, -1)
down = Vec2d(0, 1)

R = right.get_angle()
L = left.get_angle()
U = up.get_angle()
D = down.get_angle()

print (R, L, U, D)

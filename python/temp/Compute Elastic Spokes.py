#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' description of this module '

__author__ = 'Marvin Huang'

from math import *

# 预设条件
ring_radius = 200
gravity = 3600

# 第一个轮辐的角度
theta = 90

# 三个轮辐端点位置
ax = cos(radians(theta)) * ring_radius
ay = sin(radians(theta)) * ring_radius
bx = cos(radians(theta + 120)) * ring_radius
by = sin(radians(theta + 120)) * ring_radius
cx = cos(radians(theta + 240)) * ring_radius
cy = sin(radians(theta + 240)) * ring_radius

#
vector_a = (px - ax, py - ay)


print('%.3f' % bx, '%.3f' % by)



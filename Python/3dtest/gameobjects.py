#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' description of this module '

__author__ = 'Marvin Huang'


from vector3 import *

#### 测试1 #####
print ("测试1：")
A = Vector3(6, 8, 12)
B = Vector3(10, 16, 12)
print ("A is", A)
print ("B is", B)
print ("Magnitude of A is", A.get_magnitude())
print ("A+B is", A+B)
print ("A-B is", A-B)
print ("A normalized is", A.get_normalized())
print ("A*2 is", A * 2)


#### 测试2 #####
print ("测试2：")
A = (-6, 2, 2)
B = (7, 5, 10)
plasma_speed = 100. # meters per second
AB = Vector3.from_points(A, B)
print ("Vector to droid is", AB)
distance_to_target = AB.get_magnitude()
print ("Distance to droid is", distance_to_target, "meters")
plasma_heading = AB.get_normalized()
print ("Heading is", plasma_heading)
#######输出结果#########

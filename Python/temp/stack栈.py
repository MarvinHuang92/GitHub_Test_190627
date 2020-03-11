#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' description of this module '

__author__ = 'Marvin Huang'


stack = []
for i in range (10):
    stack.append(i)
print(stack)

stack.append(10)
print(stack)

n = stack.pop()
print(stack)
print(n)



grid = [
    [10 for col in range(10)]
for row in range(10)]

print(grid)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' description of this module '

__author__ = 'Marvin Huang'


def wrap_angle(angle):
    return angle % 360


a = wrap_angle(361)
b = wrap_angle(359)
c = wrap_angle(-1)
d = wrap_angle(-361)
e = wrap_angle(360)
f = wrap_angle(0)
g = wrap_angle(-360)

print(a, b, c, d, e, f, g)


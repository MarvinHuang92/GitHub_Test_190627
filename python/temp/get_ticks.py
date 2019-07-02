#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' description of this module '

__author__ = 'Marvin Huang'

import pygame

ticks = pygame.time.get_ticks()

while True:
    pygame.time.Clock().tick(1)
    print(ticks)
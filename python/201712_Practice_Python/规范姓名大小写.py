# -*- coding: utf-8 -*-

def normalize(name):
	name = name.capitalize()
	return name



# 测试:
L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)

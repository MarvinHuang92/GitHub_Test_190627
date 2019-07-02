# -*- coding: utf-8 -*-

L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

def by_name(t): # 注意：这里传入的t是每一个tuple，而不是整个list
	return t[0].lower() # 不区分大小写
    
L2 = sorted(L, key=by_name)
print(L2)

def by_score(t):
    return t[1] # 由低到高

L3 = sorted(L, key=by_score)
print(L3)

def by_score_high_low(t):
    return -t[1] # 由高到低，和加入reverse=True一样

L4 = sorted(L, key=by_score_high_low)
print(L4)
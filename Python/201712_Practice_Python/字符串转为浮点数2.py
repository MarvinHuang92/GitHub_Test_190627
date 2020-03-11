# -*- coding: utf-8 -*-
from functools import reduce

def str2float(s):
	def num_of_point(s):
		num = 0
		for n in s:
			if n == '.':
				num = num + 1
		return num

	def pos_of_point(s):
		b = s.find('.') # 如果找不到，find会返回-1，分类讨论即可
		if b == -1:
			return 0
		else:
			c = len(s)-b-1
			return c

	def calc(a, b):
		return a * 10 + b

	def char2num(s):
		DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
		return DIGITS[s]
	
	if num_of_point(s) > 1:
		raise TypeError('错误！小数点数目多于1个')
	else:
		e = s.replace(".", "") 
		# 使用循环切片方法
		# for n in range(0,len(s)-1):
			# e = s[:n] + s[n+1:]
		# 无法切干净里面的. 不知道为什么
		
		f = reduce(calc, map(char2num, e))    
		return f*(0.1**pos_of_point(s))
	


# 测试：
print('str2float(\'123.456\') =', str2float('123.456'))
if abs(str2float('123.456') - 123.456) < 0.00001:
    print('测试成功!')
else:
    print('测试失败!')

print('str2float(\'123456\') =', str2float('123456'))
print('str2float(\'.123456\') =', str2float('.123456'))
print('str2float(\'1.23456\') =', str2float('1.23456'))
print('str2float(\'12.3456\') =', str2float('12.3456'))
print('str2float(\'123.456\') =', str2float('123.456'))
print('str2float(\'1234.56\') =', str2float('1234.56'))
print('str2float(\'12345.6\') =', str2float('12345.6'))
print('str2float(\'123456.\') =', str2float('123456.'))
print('str2float(\'123.4.56\') =', str2float('123.4.56'))

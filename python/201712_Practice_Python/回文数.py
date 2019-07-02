# -*- coding: utf-8 -*-

def is_palindrome(n): # 判断一个数字是否是回文数
	s = str(n) # 先转化成字符串，然后首尾逐一比较
	for i in range(0,len(s)-1):
		if s[i] != s[len(s)-1-i]:
			return False
	return True


# 测试:
output = filter(is_palindrome, range(1, 1000))
print('1~1000:', list(output))
if list(filter(is_palindrome, range(1, 200))) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 44, 55, 66, 77, 88, 99, 101, 111, 121, 131, 141, 151, 161, 171, 181, 191]:
    print('测试成功!')
else:
    print('测试失败!')
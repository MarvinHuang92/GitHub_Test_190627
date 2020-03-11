# -*- coding: utf-8 -*-

height1 = float(input('输入你的身高（厘米）'))
weight = float(input('输入你的体重（千克）'))
height=height1/100
bmi=weight/(height**2)
a=18.5*(height**2)
b=25*(height**2)

print('你的合理体重范围：%.1fkg~%.1fkg' % (a,b))
print('你的BMI指数为：%.1f' % bmi) 

if bmi<18.5:
	print('你的体重过轻')
elif bmi<25:
	print('你的体重正常')
elif bmi<28:
	print('你的体重过重')
elif bmi<32:
	print('你已肥胖')
else:
	print('你已严重肥胖')
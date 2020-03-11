# -*- coding: utf-8 -*-
import functools

def decorator1(fn): # 这个decorator是要在任何程序执行前后都打印log
	@functools.wraps(fn)
	def wrapper(*args, **kw):
		print('begin call %s' % fn.__name__)
		result = fn(*args, **kw) # 想要在end call之前使用return是不可以的，程序会在trturn处中断，所以用一个变量名result代替程序本身
		print('end call %s' % fn.__name__)
		return result # 把return放在最后
	return wrapper

def decorator2(TEXT=''): # 这个decorator是要无论是否输入自定义文本，都可以打印log
	# 用强行给它一个默认变量的方法，简单粗暴
	# 但是有个缺陷：一定在@decorator的时候后面要加()，不然会报错
	def decorator_core(fn):
		@functools.wraps(fn)
		def wrapper(*args, **kw):
			print('%s begin call %s():' % (TEXT, fn.__name__))
			result = fn(*args, **kw)
			print('%s end call %s():' % (TEXT, fn.__name__))
			return result 
		return wrapper
	return decorator_core

def log(text): # 这个是网友提供的方法，用if把两种情况直接组装在一起，可以在@log时不加()
	# 注意第一种情况有3层嵌套，第二种只有2层
    if isinstance(text,str):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args,**kw):
                print('%s %s--这个是自定义log文本的'%(func.__name__,text))
                return func(*args,**kw)
            return wrapper
        return decorator
    else:
        @functools.wraps(text) 
		# 注意这里取了个巧：text在第一种情况代表而文本，第二种情况text代表函数名func
		# 因为它占据了一开始def log(text)的位置
        def wrapper(*args,**kw):
            print('%s --这个没有自定义的' %text.__name__)
            return text(*args,**kw)
        return wrapper

# 测试
@decorator1
def function1():
    print('function1 is running')

@decorator2('User')
def function2():
    print('function2 is running')

@decorator2()
def function3():
    print('function3 is running')

@log('USER')
def function4():
    print('function4 is running')

@log
def function5():
    print('function5 is running')

function1()
print('\n')
function2()
print('\n')
function3()
print('\n')
function4()
print('\n')
function5()

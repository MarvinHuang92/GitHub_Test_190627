#-*-coding:utf-8-*- #编码声明，不要忘记！
import requests  #这里使用requests，小脚本用它最合适！
from lxml import html    #这里我们用lxml，也就是xpath的方法

#豆瓣模拟登录，最简单的是cookie，会这个方法，80%的登录网站可以搞定
cookie = {} 

raw_cookies = ''#引号里面是你的cookie，用之前讲的抓包工具来获得

for line in raw_cookies.split(';'):
    #key,value = line.split("=", 1)
	key = line.split("=")
	#value = line.split("=")[1]
	print (key)
	#print (value)
    #cookie[key] = value #一些格式化操作，用来装载cookies

#重点来了！用requests，装载cookies，请求网站
#page = requests.get('https://www.douban.com/people/52910265/',cookies=cookie)

#对获取到的page格式化操作，方便后面用XPath来解析
#tree = html.fromstring(page.text)

#XPath解析，获得你要的文字段落！
#intro_raw = tree.xpath('//span[@id="intro_display"]/text()')

#简单的转码工作，这步根据需要可以省略
#for i in intro_raw:
#    intro = i.encode('utf-8')

#print (intro) #妹子的签名就显示在屏幕上啦

#接下来就是装载邮件模块，因为与本问题关联不大就不赘述啦~

# -*- coding: utf-8 -*-

""" run a whole loop of CANape and CANalyzer by one click """

__author__ = 'Marvin Huang'


import os, re, shutil


file_exist = False
# 区分是哪一种map文件，如果都不是，报错
for file_name in os.listdir(PR_path):      # 读取所有文件夹和文件名，返回一个list
    if re.match('^*.map$', file_name) != None:
        file_exist = True
        break

if file_exist:
    if file_name == '1321':
        pass
    elif file_name == '7894':
        pass
    else:
        file_name == 'ERROR'

if (not file_exist) or (file_name == 'ERROR'):
    pass   # 报错
# 复制map文件到指定的位置
# 执行py
# 调用bat并给它正确的参数
# 把输出结果复制出来

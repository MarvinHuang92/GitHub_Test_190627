# -*- coding: utf-8 -*-

""" 静态网页爬虫，分析体彩7星彩中奖情况 """

__author__ = 'Marvin Huang'

import os, get_data, calc_prize
from lottery_config import *

# 检查历史记录是否存在
content = []
history_read = False
counter = 0
if os.path.exists('history.ini'):
    print('读取历史记录...\n')
    with open('history.ini') as f:
        content = f.readlines()
        f.close()
    try:
        # 这个是以前的，已经过期
        # starting_url = '/' + content[-3].strip('http://www.js-lottery.com')
        
        # 这个是现在的，但不知道为什么不好用
        # starting_url = '/cms/post-' + content[-3].strip('http://www.js-lottery.com')
        
        # 这个很奇怪，格式不对但却能用
        starting_url = '/' + content[-3]
        print('Last History URL: %s' % starting_url)
        for line in content:
            if counter > 2:
                counter = 0
            elif counter == 1:
                print(line.strip())
            counter += 1
        history_read = True
    except IndexError:
        print('历史记录文件格式错误\n')
        content = []
        starting_url = default_url
        history_read = False
else:
    print('未找到历史记录\n')
    starting_url = default_url

# 运行爬虫
current_data = get_data.get_data(starting_url)
while True:
    # 如果正确读取了历史记录，则跳过最后一次记录的结果
    if not history_read:
        result1 = current_data['current_url']
        result2 = current_data['report'] + '  ' + calc_prize.calc_prize(default_array, current_data['lottery_num'])
        # 在屏幕显示结果
        print("全国 " + result2)
        # 将结果附加在历史记录中
        content.append(result1+ '\n')
        content.append(result2+ '\n')
        content.append('\n')  # 一个空白行，方便人工阅读ini文件
    # 重置状态，否则将持续跳过
    history_read = False

    try:
        next_url = current_data['next_url']  # 因为最后一个缺少next_url键，会报错KeyError
        current_data = get_data.get_data(next_url)
    except KeyError:
        break

# 写入新的历史记录
with open('history.ini', 'w') as f:
    f.writelines(content)
    f.close()
    
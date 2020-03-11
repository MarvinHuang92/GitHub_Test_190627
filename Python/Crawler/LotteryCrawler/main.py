# -*- coding: utf-8 -*-

""" 静态网页爬虫，分析体彩7星彩中奖情况 """

__author__ = 'Marvin Huang'

import get_data, calc_prize
from lottery_config import *

current_data = get_data.get_data(default_url)
while True:
    print(current_data['report'] + '  ' + calc_prize.calc_prize(default_array, current_data['lottery_num']))
    try:
        next_url = current_data['next_url']  # 因为最后一个缺少next_url键，会报错KeyError
        current_data = get_data.get_data(next_url)
    except KeyError:
        break

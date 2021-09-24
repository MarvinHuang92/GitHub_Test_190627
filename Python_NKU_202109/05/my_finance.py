# -*- coding: utf-8 -*-
"""
get DJI data

@author: Dazhuang
"""

import json
import re
import requests

def retrieve_dji_list():
    try:
        r = requests.get('http://money.cnn.com/data/dow30/')
    except ConnectionError as err:
        print(err) 
    search_pattern = re.compile('class="wsod_symbol">(.*?)<\/a>.*<span.*">(.*?)<\/span>.*\n.*class="wsod_stream">(.*?)<\/span>')
    dji_list_in_text = re.findall(search_pattern, r.text)
    dji_list = []
    for item in dji_list_in_text:
        dji_list.append({'code': item[0], 'name': item[1], 'price': float(item[2])})
    return dji_list
    
def retrieve_quotes_historical(stock_code, start = '', end = ''):
    quotes = []
    url = 'https://finance.yahoo.com/quote/%s/history?p=%s' % (stock_code, stock_code)
    try:
        r = requests.get(url)
    except ConnectionError as err:
        print(err)    
    m = re.findall('"HistoricalPriceStore":{"prices":(.*?),"isPending"', r.text)
    if m:
        quotes = json.loads(m[0])
        quotes = quotes[::-1]
    return [item for item in quotes if 'type' not in item]
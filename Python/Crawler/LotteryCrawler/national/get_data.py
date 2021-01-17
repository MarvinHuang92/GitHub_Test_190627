# -*- coding: utf-8 -*-

import requests, re


# 在输入的网址上爬取开奖日期、期数、开奖号码、下一次开奖网址，并返回dict
def get_data(target_url):

    # 请求的首部信息
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
    # 例子的url
    # url = 'https://www.js-lottery.com/Article/news/group_id/3/article_id/91912.html' # 目标网页
    url = 'http://www.js-lottery.com' + target_url
    # 利用requests对象的get方法，对指定的url发起请求，该方法会返回一个Response对象
    res = requests.get(url, headers=headers)
    # 通过Response对象的text方法获取网页的文本信息，res.text是一个完整的str
    # print(res.text)

    # 将res.text从一整个str拆分成单行
    text_list = res.text.split('\n')
    # 搜索其中带有关键信息的行
    batch_num = '<h1><font style="color: #FF0000;font-size:25px;"><font style="color: #000000;">'
    date_line = '&nbsp;开奖日期'
    lottery_num_line = '&nbsp;本期开奖号码'
    end_line = '<div class="last">上一篇：<a'    # 注意这里实际是找它的下一行
    found_lines = 0
    batch_num_index = -1
    date_line_index = -1
    lottery_num_line_index = -1
    end_line_index = -1

    for i in range(len(text_list)):
        # print(text_list[i])
        if found_lines != 4:
            if re.search(batch_num, text_list[i]) is not None:
                batch_num_index = i
                found_lines += 1
            if re.search(date_line, text_list[i]) is not None:
                date_line_index = i
                found_lines += 1
            if re.search(lottery_num_line, text_list[i]) is not None:
                lottery_num_line_index = i
                found_lines += 1
            if re.search(end_line, text_list[i]) is not None:
                end_line_index = i + 1  # 注意这里实际是找它的下一行
                found_lines += 1
        else:  # 如果三个关键行都找到了，就停止查找
            break

    batch_num_str = text_list[batch_num_index]
    date_line_str = text_list[date_line_index]
    lottery_num_line_str = text_list[lottery_num_line_index]
    end_line_str = text_list[end_line_index]
    # print(batch_num_index, batch_num_str)
    # print(date_line_index, date_line_str)
    # print(lottery_num_line_index, lottery_num_line_str)
    # print(end_line_index, end_line_str)

    # 提取关键信息，写入dict
    data = {}
    data['current_url'] = url
    data['batch_no'] = re.findall(r"中国体育彩票江苏省7位数第(.+?)期开奖公告", batch_num_str)[0]
    data['date'] = re.findall(r"开奖日期：(.+?)日", date_line_str)[0] + '日'
    # 如果直接搜不到，就简单截取最后13个字符（7个数字+6个空格）
    try:
        data['lottery_num'] = re.findall(r"本期开奖号码：(.+?) <br/></p><table style=", date_line_str)[0]
    except IndexError:
        data['lottery_num'] = lottery_num_line_str.strip()[-13:]
    # 将字符串形式的开奖号码转换成list
    lottery_num_int_list = []
    for i in range(7):
        lottery_num_int_list.append(int(data['lottery_num'].split(' ')[i]))
    data['lottery_num'] = lottery_num_int_list
    # 最后一期开奖页面找不到这一行，会报错IndexError
    try:
        data['next_url'] = re.findall(r'href="(.+?)"><font style', end_line_str)[0]
    except IndexError:
        pass

    # 添加文字说明
    report = str(data['date']) + ' 第' + str(data['batch_no']) + '期 开奖号码: '
    for i in range(7):
        report += str(data['lottery_num'][i])
    data['report'] = report

    return data

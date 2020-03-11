# -*- coding: utf-8 -*-


# 根据输入的购买号码和开奖号码计算是否中奖
def calc_prize(buy_num, lottery_num):

    # 根据主号码生成10份号码
    # 输入的号码都是list形式

    # 初始化10行7列的空数组（元素都是0）
    # 第一个数组表示10份自选号码
    candidate = [[0 for col in range(7)] for row in range(10)]
    # 第二个数组表示一致性：由0,1组成，1表示这一位数和开奖结果一致，0表示不一致
    consistence = [[0 for col in range(7)] for row in range(10)]
    # 二维数组前行后列
    for row in range(10):
        for digit in range(7):
            candidate[row][digit] = buy_num[digit] + row
            if candidate[row][digit] >= 10:
                candidate[row][digit] -= 10
            if candidate[row][digit] == lottery_num[digit]:
                consistence[row][digit] = 1
    # print(candidate)
    # print(consistence)

    # 统计一致性矩阵每行最多有几个连续的1
    max_consistence = [0] * 10
    for row in range(10):
        c = 0
        total = 0
        for digit in range(7):
            if consistence[row][digit] == 1:
                c += 1
                if total < c:
                    total = c
            else:
                c = 0
        max_consistence[row] = total

    # 将连续一致数字的数量转换为中奖等级，prize六个元素分别对应特等奖~五等奖
    prize = [0] * 6
    for i in range(10):
        if max_consistence[i] >= 2:
            prize[7 - max_consistence[i]] += 1

    # 文字说明
    text_list = ['特等奖*', '一等奖*', '二等奖*', '三等奖*', '四等奖*', '五等奖*']
    account_list = [5000000, 50000, 3000, 300, 20, 5]
    report = ''
    account = 0
    for i in range(6):
        if prize[i] != 0:
            report += (text_list[i] + str(prize[i]) + ' ')
            account += account_list[i] * prize[i]
    if report != '':
        report += ('共' + str(account) + '元')

    return report

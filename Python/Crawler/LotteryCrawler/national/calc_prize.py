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

    # 统计一致性矩阵中1的数量（不需要连续）
    max_consistence = [0] * 10
    for row in range(10):
        c = 0
        # 前区：前6位数字，每对一位记作10
        for digit in range(6):
            if consistence[row][digit] == 1:
                c += 10
        # 后区：对了记作1
        if consistence[row][6] == 1:  # 元素[6]实际上是第7位
            c += 1
        max_consistence[row] = c
    # print(max_consistence)

    # 将连续一致数字的数量转换为中奖等级，prize六个元素分别对应一等奖~六等奖
    prize = [0] * 6
    for i in range(10):
        # 一等奖
        if max_consistence[i] == 61:
            prize[0] += 1
        # 二等奖
        if max_consistence[i] == 60:
            prize[1] += 1
        # 三等奖
        if max_consistence[i] == 51:
            prize[2] += 1
        # 四等奖
        if max_consistence[i] == 50 or max_consistence[i] == 41:
            prize[3] += 1
        # 五等奖
        if max_consistence[i] == 40 or max_consistence[i] == 31:
            prize[4] += 1
        # 六等奖
        if max_consistence[i] == 30 or max_consistence[i] == 21 or max_consistence[i] == 11 or max_consistence[i] == 1:
            prize[5] += 1
    # print(prize)

    # 文字说明
    text_list = ['一等奖*', '二等奖*', '三等奖*', '四等奖*', '五等奖*', '六等奖*']
    account_list = [5000000, 50000, 3000, 500, 30, 5]
    report = ''
    account = 0
    for i in range(6):
        if prize[i] != 0:
            report += (text_list[i] + str(prize[i]) + ' ')
            account += account_list[i] * prize[i]
    if report != '':
        report += ('共' + str(account) + '元')

    return report

discount = 1000  # 个税减免政策
worker_union = 5  # 工会费

def taxed_income_calc(income):
    global discount
    global worker_union
    insurance = income * 0.185
    income_to_tax = income - insurance - 5000 - discount
    if income_to_tax <= 3000:
        tax = income_to_tax * 0.03
    elif 3000 < income_to_tax <= 12000:
        tax = income_to_tax * 0.1 - 210
    elif 12000 < income_to_tax <= 25000:
        tax = income_to_tax * 0.2 - 1410
    elif 25000 < income_to_tax <= 35000:
        tax = income_to_tax * 0.25 - 2660
    elif 35000 < income_to_tax <= 55000:
        tax = income_to_tax * 0.3 - 4410
    elif 55000 < income_to_tax <= 80000:
        tax = income_to_tax * 0.35 - 7160
    else:
        tax = income_to_tax * 0.45 - 15160
    return income - insurance - tax - worker_union, discount


def income_before_tax_calc(taxed_income):
    upper_limit = taxed_income * 2.5
    lower_limit = taxed_income
    i = 0
    while i <= 500:
        avg = (upper_limit + lower_limit) / 2
        calc_try, discount = taxed_income_calc(avg)
        residual = calc_try - taxed_income
        if -1 < residual < 1:
            break
        elif residual < 0:
            lower_limit = avg
        else:
            upper_limit = avg
        i += 1
    return avg, i, discount


def config():
    global discount
    global worker_union
    discount = float(input('个税减免金额: '))
    worker_union = float(input('工会费: '))
    print('')


while True:
    taxed_income = float(input('INCOME AFTER TAX (-1 to Exit, 0 to Config Discount): '))
    if taxed_income == 0:
        config()
        continue
    elif taxed_income < 0:
        break
    avg, i, discount = income_before_tax_calc(taxed_income)
    # 对结果进行经验修正
    avg_orig = avg
    avg = 0.9119 * avg + 993.84
    print('================================================')
    if i >= 500:
        print('calc out of time!')
    else:
        print('income_before_tax: %.2f' %avg)
        print('income_ after_tax: %.2f' %taxed_income)
        print('tax:               %.2f ; %.1f%%' %((avg - taxed_income), ((avg - taxed_income) / avg * 100)))
        print('tax discount:      %d' % discount)
        print('original_calc:     %.2f (Just for Debugging)' %avg_orig)
    print('================================================\n')

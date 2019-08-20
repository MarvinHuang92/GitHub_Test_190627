
import csv

# 打开文件
# 方式wb会省去许多问题
# with open("test.csv", "rb", encoding="utf-8") as csvfile: #读取csv文件，返回的是迭代类型
with open("test.csv", "rb") as csvfile:  # 读取csv文件，返回的是迭代类型
    read = csv.reader(csvfile)
    for i in read:
        print(i)

# 注意newline
with open("test.csv","w",newline="") as datacsv:
    # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
    csvwriter = csv.writer(datacsv,dialect = ("excel"))
    # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
    csvwriter.writerow(["A","B","C","D"])

# 读
with open('test.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['first_name'], row['last_name'])

# Out:
# Baked Beans
# Lovely Spam
# Wonderful Spam

# 写
with open('test.csv', 'wb') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #注意header是个好东西
    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

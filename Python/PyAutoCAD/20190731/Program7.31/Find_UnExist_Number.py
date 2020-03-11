import re

file2 = 'UnExist.txt'

print ("================= Preparing Filename =======================")  # 从文件中读取所有文件名

filename_list = []
for line in open("dwg_list_file.txt"):
    line = line.strip()  # 去掉文件换行的回车符
    if line != "":  # 忽略空行
        filename_list.append(line)
        print (line)

print ("\nDone.")

print ("============== Filename Legal Validation ===================")  # 验证文件名格式，从列表中删除不合法文件名

def legal_valid(filename):
    legal_pattern = re.compile(r'^SH-[A-Z0-9]{3,}-[A-Z]{2,}-(\d{3})-(\d{3}).dwg$')
    if re.match(legal_pattern, filename) == None:
        name_is_legal = False
    else:
        name_is_legal = True
    return name_is_legal

illegal_filename_list = []
for filename in filename_list:
    if not legal_valid(filename):
        illegal_filename_list.append(filename)
        filename_list.remove(filename)

print ("Legal Names:")
for s in filename_list:
    print (s)
print ("\nillegal Names:")
for s in illegal_filename_list:
    print (s)
print ("\nDone.")

print ("=============== Get Part Number & Catagory =================")  # 读取文件类别字段，并重新排序

partnumber_list = []
catagory_index_list = []
all_catagories = []
for filename in filename_list:
    partnumber = int(re.split(r'-', filename)[3])
    partnumber_list.append(partnumber)
    catagory = re.split(r'-', filename)[1] + '-' + re.split(r'-', filename)[2]
    if not catagory in all_catagories:
        all_catagories.append(catagory)
        catagory_index_list.append(len(all_catagories) - 1)
    else:
        catagory_index_list.append(all_catagories.index(catagory))

with open(file2, 'w') as f:
    f.truncate()
for cat in all_catagories:
    Drawing_Number = []
    print ("-------------- %s Missing Part No: ---------------" % cat)
    for p_index in range(len(partnumber_list)):
        if all_catagories[catagory_index_list[p_index]] == cat:
            print (partnumber_list[p_index])
            Drawing_Number.append(partnumber_list[p_index])

    # 计算缺失的图表编号
    Drawing_Number.sort()
    Lost_Number = []
    for i in range(1, len(Drawing_Number)):
        if Drawing_Number[i] - Drawing_Number[i - 1] > 1 and Drawing_Number[i] <= 500:
            Big = Drawing_Number[i]
            Small = Drawing_Number[i - 1]
            while Big > Small + 1:
                Big = Big - 1
                Lost_Number.append(Big)

    # 对编号进行重排序，并输出到文件
    Lost_Number.sort()
    with open(file2, 'a+') as f:
        f.write("------- %s Missing Part No: --------\n" % cat)
        for i in Lost_Number:
            f.write(str(i) + ' ')
        f.write("\n\n")

print ("\nAll Procedures Done.")

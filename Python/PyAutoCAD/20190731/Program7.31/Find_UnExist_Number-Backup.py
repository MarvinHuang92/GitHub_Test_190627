import re
file = open('path.txt')
file_path = file.read()
file2 = open('UnExist.txt','w')

PartNumber=re.compile(r'\\')
file_path=PartNumber.sub(r'\\\\',file_path)

UnExist=[]
Drawing_Number = []

#设定Regex格式
PartNumber=re.compile(r'-(\d\d\d)-')
Str='aa'

# 读取文件目录中每一行，写为一个Str，利用Regax进行筛选
for line in open("dwg_list_file.txt"):
    Str=Str+line
PartNumber = PartNumber.findall(Str)

#转换筛选结果为int格式
for i in PartNumber:
    i=int(i)
    Drawing_Number.append(i)

#计算缺失的图表编号
Lost_Number=[]
for i in range(len(Drawing_Number)):
    if Drawing_Number[i]-Drawing_Number[i-1]>1 and Drawing_Number[i]<=500:
        Big=Drawing_Number[i]
        Small=Drawing_Number[i-1]
        while Big>Small+1:
            Big=Big-1
            Lost_Number.append(Big)
        

#对编号进行重排序
Lost_Number.sort()
for i in Lost_Number:
    file2.write(str(i)+',')
file.close


            
        

            


 
 

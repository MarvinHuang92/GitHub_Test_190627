#!/usr/bin/env python
# -*- coding: utf-8 -*-

# v1.1 --- 增加读取当前日期功能
# v1.2 --- 改用文件目录记录所有dwg名字


from pyautocad import Autocad, APoint
import math
import time  # 引入time模块

def read_DET(part_no):
    # 确定三位数零件号
    global DET
    if part_no <= 9:
        DET = "00%d" %(part_no)
    elif 9 < part_no <= 99:
        DET = "0%d" %(part_no)
    elif part_no > 99:
        DET = "%d" %(part_no)
    # print ("read DET: #%s" %(DET))
    return DET

acad=Autocad(create_if_not_exists = True)

# min = 10
# max = 87
DWG_File_path = "C:\\Users\PeterZhu\\Desktop\\SensorOP10\\"
#DWG_File_path = "D:\\Programming\\GitHub_190628\\PyAutoCAD\\test_DWG\\"

SuccessNumber = []
ErrorNumber = []
UnExistNumber = []
file_name_list = []

# 读取文件目录中每一行，存入列表
try:
    for line in open("dwg_list_file.txt"):
        if line != "":
            file_name_list.append(line)
    print ("Read DWG File List\n=======================\n")
except:
    print ("Can not find DWG File List!\n=======================\n")

# 循环读取待修改的dwg文件
for dwg_name in file_name_list:
    dwg_name = dwg_name.strip()  # 从txt文件中读取行会带有回车，需要切除后再作为字符串使用
    working = True  # 初始化“工作正常”
    DET = ""  # 初始化全局变量DET
    try:
        # 判断文件名是否合法
        try:
            dwg_name_split = dwg_name.split("-")
        except:
            print ("Invalid File Name: %s" %(dwg_name))
            working = False

        # 切分文件名放进list中，并强制转换为整数
        part_no = int(dwg_name_split[len(dwg_name_split) - 2])
        DET = read_DET(part_no)  # 调用函数，让DET不再是空值
        if 0 < part_no < 1000:
            #print (part_no)
            try:
                print("Open file: %s%s" %(DWG_File_path, dwg_name))
                acad.ActiveDocument.Application.Documents.Open("%s%s" %(DWG_File_path, dwg_name))
            except:
                print("Can not open this file")
                working = False
        else:
            print ("Invalid Part Number: %s" %(dwg_name))
            working = False


        # 如果文件名合法
        if working:
            print("Start working on Part #%s"%(DET))

            try:                
                #获取MREVBLK块的对角线坐标
                for obj in acad.iter_objects("AcDbBlockReference"):
                    if obj.Name == "MREVBLK":
                        Point_Lower_Left=obj.GetBoundingBox()[0]
                        Point_Upper_Right=obj.GetBoundingBox()[1]

                #获得MREVBLK边界对角线点的坐标
                LL=APoint(Point_Lower_Left)
                UR=APoint(Point_Upper_Right)
                UL=APoint(LL.x,UR.y)
                LR=APoint(UR.x,LL.y)
                print ("Block Coordinate Read")

                #确定文字位置和大小的缩放比例
                Length=UL.y-LL.y
                Scale=Length/92.07500000000059

                #新建图层，设定图层颜色，并设为当前图层
                LayerObj=acad.ActiveDocument.Layers.Add("REVISIONS INFORMATION")
                acad.ActiveDocument.ActiveLayer=LayerObj
                ClrNum=4
                LayerObj.color=ClrNum
                print ("New Layer Created")


                #填写各类信息
                #1 001
                REY="001"
                insertPnt=APoint((UL.x)+1*Scale,(UL.y)-12*Scale)
                height=1.125*Scale
                textObj=acad.model.AddText(REY,insertPnt,height)

                #2 DET-三位数零件号
                insertPnt=APoint((UL.x)+5.8*Scale,(UL.y)-12*Scale)
                height=1.125*Scale
                textObj=acad.model.AddText(DET,insertPnt,height)

                #3
                CHANGE="Original Version"
                insertPnt=APoint((UL.x)+15*Scale,(UL.y)-12*Scale)
                height=1.125*Scale
                textObj=acad.model.AddText(CHANGE,insertPnt,height)

                #4
                BY="D.H_KIM"
                insertPnt=APoint((UL.x)+33*Scale,(UL.y)-12*Scale)
                height=0.5*Scale
                textObj=acad.model.AddText(BY,insertPnt,height)

                #4
                CK="Y.S_JANG"
                insertPnt=APoint((UL.x)+36.3*Scale,(UL.y)-12*Scale)
                height=0.5*Scale
                textObj=acad.model.AddText(CK,insertPnt,height)

                #5 日期
                DATE=time.strftime("%d-%b-%y", time.localtime())  # %y表示两位数年份，%Y表示四位数
                DATE = DATE.upper()
                insertPnt=APoint((UL.x)+40*Scale,(UL.y)-12*Scale)
                height=1*Scale
                textObj=acad.model.AddText(DATE,insertPnt,height)
                print ("Info Filled\nWork finished on Part #%s"%(DET))

            except:
                print ("Work NOT finished on Part #%s"%(DET))


            # 保存文件
            try:
                acad.ActiveDocument.Application.Documents(dwg_name).Close()
                print ("File Saved: Part #%s\n" %(DET))
                SuccessNumber.append(DET)
            except:
                print ("cannot save this file")
                ErrorNumber.append(DET)
            
        else:
            print ("Part #%s Doesn't Exist!\n" %(DET))
            UnExistNumber.append(DET)

    except:
        print ("ERROR: #%s\n" %(DET))
        ErrorNumber.append(DET)

print ("Succeeds: #", SuccessNumber)
print ("Errors:   #", ErrorNumber)
print ("UnExists: #", UnExistNumber)


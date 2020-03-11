#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''增加读取当前日期功能 --- v1.1 '''


from pyautocad import Autocad, APoint
import math
import time  # 引入time模块

acad=Autocad(create_if_not_exists=True)

max = 256

#循环读取待修改的dwg文件
for i in range(1,max):
    try:
        part_num = True #初始化“零件号存在”
        
        #判断零件位数
        if 9<i<=99:
            try:
                acad.ActiveDocument.Application.Documents.Open("C:\\Users\\PeterZhu\\Desktop\\AutoCAD_Source\\SH-TL101823-DET-0%d-001.dwg"%(i))
            except:
                part_num = False
        elif i>99:
            try:
                acad.ActiveDocument.Application.Documents.Open("C:\\Users\\PeterZhu\\Desktop\\AutoCAD_Source\\SH-TL101823-DET-%d-001.dwg"%(i))
            except:
                part_num = False
        elif i<=9:
            try:
                acad.ActiveDocument.Application.Documents.Open("C:\\Users\\PeterZhu\\Desktop\\AutoCAD_Source\\SH-TL101823-DET-00%d-001.dwg"%(i))
            except:
                part_num = False

        #如果存在此零件号
        if part_num:
            print("Open Part No%d"%(i))
            
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
            #1
            REY="001"
            insertPnt=APoint((UL.x)+1*Scale,(UL.y)-12*Scale)
            height=1.125*Scale
            textObj=acad.model.AddText(REY,insertPnt,height)

            #2
            if i>9:
                DET="0%d"%(i)
            elif i>99:
                DET="%d"%(i)
            elif i<=9:
                DET="00%d"%(i)
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

            #5
            DATE=time.strftime("%d-%b-%y", time.localtime())
            DATE = DATE.upper()
            insertPnt=APoint((UL.x)+40*Scale,(UL.y)-12*Scale)
            height=1*Scale
            textObj=acad.model.AddText(DATE,insertPnt,height)
            print ("Info Filled")

            if 9<i<=99:
                    acad.ActiveDocument.Application.Documents("SH-TL101823-DET-0%d-001.dwg"%(i)).Close()
            elif i>99:
                    acad.ActiveDocument.Application.Documents("SH-TL101823-DET-%d-001.dwg"%(i)).Close()
            elif i<=9:
                    acad.ActiveDocument.Application.Documents("SH-TL101823-DET-00%d-001.dwg"%(i)).Close()
            print ("File Saved: Part No%d\n"%(i))
            
        else:
            print ("Part No%d Doesn't Exist!\n"%(i))

    except:
        print ("ERROR: No%d\n"%(i))


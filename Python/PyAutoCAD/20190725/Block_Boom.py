#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    ===========================
    Author = Li Yang
    Email:liyang@alu.hit.edu.cn
    ===========================

    PEP8 Python 编码规范：
    （1）、包名：简短全小写，不建议使用下划线；
    （2）、模块名、全局变量名、局部变量名、常量名、方法名：
               简短全小写，为了提升可读性，可以使用下划线；
    （3）、常量名：简短全大写，为了提升可读性，可以使用下划线；
    （4）、类名：大写驼峰，采用名词或形容词+名词形式；
    参考文献：https://blog.csdn.net/ratsniper/article/details/78954852
    注：在Pycharm中全选代码，按Ctrl+Alt+L快捷键，自动按PEP8要求排版。
"""

from pyautocad import Autocad
from pyautocad import APoint
import time

" ****************************** ---- 1、与CAD的连接 ---- ****************************** "

acad = Autocad(create_if_not_exists=True)
acad.prompt("Hello! Autocad from Python.")
print(acad.doc.Name)

" ******************************** ---- 2、主程序 ---- ********************************* "

for obj in acad.iter_objects("AcDbBlockReference"):
    print(obj.Name)
    if obj.Name == "MREVBLK":
        print("Boom左下角点坐标：", obj.GetBoundingBox()[0])
        print("Boom右上角点坐标：", obj.GetBoundingBox()[1])
        insertionPnt = APoint(obj.GetBoundingBox()[1])

        # copyObj = obj.Copy()
        # startPnt = APoint(0, 0)
        # endPnt = APoint(500, 0)
        # copyObj.Move(startPnt,endPnt)
        # try:
        #     copyObj.Explode()  # 炸开块
        # except:
        #     pass
        # copyObj.Delete()
        try:
            obj.Explode()  # 炸开块
        except:
            pass
        obj.Delete()

txt = ["1OF2", "2OF2"]

try:
    try:
        for obj in acad.iter_objects("AttributeDefinition"):
            if obj.TagString in txt:
                obj.Delete()
    except:
        for obj in acad.iter_objects("AttributeDefinition"):
            if obj.TagString in txt:
                obj.Delete()
except:
    pass

for obj in acad.iter_objects("AttributeDefinition"):
    if obj.TagString == "ONE":
        obj.TagString = "NEW_TgaString" # 新的标记，不能有空格。






#         except:
#             copyObj.Delete()  # 删除重复
#
        # txt = ["SYM", "DET", "BY", "RDATE", "CK"]
        # # for obj in acad.iter_objects("AttributeDefinition"):
        # #     obj.Delete()
# #             # 以下获取块的属性信息
# #             # 如果想获取某一特定块的属性信息可以用ObjectID识别特定块
# #             # print("**************")
#             print(obj.TagString)
# #             # print(obj.InsertionPoint)
# #             # print(obj.TextAlignmentPoint)
#
#             if obj.TagString in txt:
#                 pass
#             elif obj.TagString == "ONE":
#                 obj.TagString = "NEWLABEL"
#                 time.sleep(0.5)
#             elif obj.TagString == "1OF2":
#                 obj.Delete()
#                 time.sleep(0.5)
#             elif obj.TagString == "2OF2":
#                 obj.Delete()
#                 time.sleep(0.5)

#                 obj.TagString = "NEWLABEL"
#                 insert_pnt = obj.InsertionPoint
#                 ali_pnt = obj.TextAlignmentPoint
#
#             # if obj.TagString in txt_2:
#             #     obj.InsertionPoint = APoint(insert_pnt)
#             #     obj.TextAlignmentPoint = APoint(ali_pnt)
#
#
#             # else:
#             #     obj.TagString = New_TagString
#             #     obj.InsertionPoint = APoint(insert_pnt)
#             #     obj.TextAlignmentPoint = APoint(ali_pnt)
#
#
# #                 startPnt = APoint(0, 0)
# #                 endPnt = APoint(300, 0)
# #                 obj.Move(startPnt, endPnt)
# #                 LayerObj = acad.ActiveDocument.Layers.Add("New_Layer")
# #                 obj.layer = "New_Layer"

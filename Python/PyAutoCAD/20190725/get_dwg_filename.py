#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" 读取文件夹下的所有dwg文件，并输出文件名字到dwg_list_file.txt """

import os

file_path = "C:\\Users\\PeterZhu\\Desktop\\SensorOP10"

path_list = os.listdir(file_path)  # os.listdir(file)会历遍文件夹内的文件并返回一个列表
# print (path_list)

dwg_list = []  # 定义一个空列表，用于存储path_list中的所有dwg文件名

# 遍历path_list列表并且利用split筛选出后缀名，将所有dwg文件名存储进path_list
for file_name in path_list:
    if file_name.split(".")[len(file_name.split(".")) - 1] == "dwg":
        dwg_list.append(file_name)

# 排序一下
dwg_list.sort()

# 如果已经存在"dwg_list_file.txt"，将它删除
if os.path.exists("dwg_list_file.txt"):
    os.remove("dwg_list_file.txt")
for file_name in dwg_list:
    # "a"表示以不覆盖的形式（Append）写入到文件中，"w"表示覆盖（Write），当前文件夹如果没有"dwg_list_file.txt"会自动创建
    with open("dwg_list_file.txt", "a") as f:
        f.write(file_name + "\n")
        f.close()

print ("File_name_list Generated")

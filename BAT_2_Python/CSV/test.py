# 添加第一行python版本说明
# 修改关键词start
# 修改成rb和wb


# -*- coding: utf-8 -*-

"""  Transfer Fault_Event_Id.txt file into csv format for more clear view  """


import csv

with open('Fault_Event_Id.csv', 'wb') as csv_file:
    csv_writer = csv.writer(csv_file, dialect='excel')
    with open('Fault_Event_Id.txt', 'rb') as txt_file:
        introduction = True
        header_line = False
        for line in txt_file.readlines():
            #  Locate the header position according to keyword ‘start’
            if introduction and 'start' in line:
                introduction = False
                header_line = True
            #  Copy down the introduction part (before the header) from txt file directly
            if introduction:
                line_list = line.strip('\n').replace(' ', '_').split(' ')
                csv_writer.writerow(line_list)
            else:
                #  Insert a line after the introduction as the header
                if header_line:
                    csv_writer.writerow(['', 'Fault_Event_Name', 'Fault_ID'])
                    csv_writer.writerow([''])
                    header_line = False
                #  Clear up unnecessary spaces in fault event list
                else:
                    line_list = line.strip('\n').split(' ')
                    line_list_dry = []
                    for segment in line_list:
                        if segment != '':
                            line_list_dry.append(segment)
                    print(line_list_dry)
                    csv_writer.writerow(line_list_dry)
    txt_file.close()
csv_file.close()

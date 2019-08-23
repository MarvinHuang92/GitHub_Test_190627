# -*- coding: utf-8 -*-

"""  Transfer Event and Behavior ID from txt file into csv format for more clear view  """


import csv
separator = ['=============================================================================']
enum_id = 0


# Remove all '/', '*' and spaces in a line and then write to csv file
def strip_and_writerow(line, csv_writer):
    line_list = [line.strip().strip('/').strip('*').strip()]
    if line_list != ['']:
        csv_writer.writerow(line_list)


# Calculate ID of enum events that not explict displayed
def calculate_enum_id(list):
    global enum_id
    if len(list) >= 3:
        enum_id = int(list[2]) + 1
    else:
        list.append('->')
        list.append(enum_id)
        enum_id += 1
    return list


# Read txt file and transfer it to csv format
def transfer(file_name, variant):
    if variant == 'event':
        keyword_copyright = '*'
        keyword_event = '#ifndef'
        header = ['', 'Fault_Event', 'ID']
    elif variant == 'behavior':
        keyword_copyright = '//'
        keyword_event = 'enum Value'
        header = ['Behavior', '', 'ID']

    comments = [separator, ['NOTE: This CSV file is converted from TXT format by a python script.'],
                ['If you find any formation or display error, please refer to the source file: ' + file_name + '.txt']]
    comments2 = [[''], ['The IDs with equal sign (=) are directly assigned in enum,'],
                ['and the IDs with arrow (->) are calculated through the script, which is only for reference.']]

    header_line = False
    event_list = False
    with open(file_name + '.csv', 'wb') as csv_file:
        csv_writer = csv.writer(csv_file, dialect='excel')
        if variant == 'event':
            # To make artistic format, insert a line of separators
            csv_writer.writerow(separator)
        with open(file_name + '.txt', 'rb') as txt_file:
            # Initialize enum_id
            global enum_id
            enum_id = 0
            for line in txt_file.readlines():
                # Locate copyright lines position
                if keyword_copyright in line:
                    copyrights = True
                else:
                    copyrights = False
                # Locate the header line position
                if not copyrights and keyword_event in line:
                    header_line = True

                # Remove all '/', '*' and spaces before and after copyright lines
                if copyrights and not event_list:
                    strip_and_writerow(line, csv_writer)
                # Print Event IDs
                elif not copyrights:
                    if '#endif' in line:
                        break
                    # Insert a line after copyrights part as a header
                    if header_line:
                        for i in range(len(comments)):
                            csv_writer.writerow(comments[i])
                        if variant =='behavior':
                            for i in range(len(comments2)):
                                csv_writer.writerow(comments2[i])
                        csv_writer.writerow(separator)
                        csv_writer.writerow([''])
                        csv_writer.writerow(header)
                        csv_writer.writerow([''])
                        header_line = False
                        event_list = True
                    # Clear up unnecessary spaces in fault event list
                    elif event_list:
                        line_list = line.strip().split(' ')
                        if line_list != [''] and line_list != ['{']:
                            line_list_dry = []
                            for segment in line_list:
                                if segment != '':
                                    line_list_dry.append(segment.strip(','))
                            if variant == 'behavior':
                                line_list_dry = calculate_enum_id(line_list_dry)
                            csv_writer.writerow(line_list_dry)
                    if '= 255' in line:
                        break
        txt_file.close()
    csv_file.close()


transfer('Fault_Event_Id', 'event')
transfer('FCT_Behavior_Specification_Id', 'behavior')
transfer('FCT_Filtered_Behavior_Id', 'behavior')

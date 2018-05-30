import os
import re
import csv
from datetime import datetime


def getting_files(path):
    """
    Function scans directory and creates 2 lists:
    names_of_nodes - short names of network elements;
    list_of_files - full titles of config files for transferring data to the next function.
    """
    list_of_files = []
    names_of_nodes = []
    for f in os.listdir(path):
        # print(f)
        file_name, file_ext = os.path.splitext(f)
        f_date, f_id, f_title, f_ip, f_suffix = file_name.split('.')
        # print('{}_{}'.format(f_title[:-2:], f_date[0:10]))
        names = '{}'.format(f_title[:-2:])
        list_of_files.append(f)
        names_of_nodes.append(names)
    # print(list_of_files)
    # print(names_of_nodes)
    print('Please wait a minute... Program is handling ' + str(len(list_of_files)) + ' file(s)')
    v_lan_result = vlan_parser(list_of_files)
    csv_writer(names_of_nodes, v_lan_result)


def vlan_parser(list_of_files):
    """
    Function parses each file from previous function according to some rules
    for getting unique list of vlans from each network element and transfers this data
    to the next function
    """
    list_of_vlans = []
    parser_name = ' name'
    for file in list_of_files:
        with open(file) as current_file:
            vlans_of_current_file = []
            for line in current_file:
                if re.match(parser_name, line):
                    vlan_name_line = line.strip()
                    found_vlan = vlan_name_line[5:11]
                    vlans_of_current_file.append(found_vlan)
            # print(vlans_of_current_file)
            list_of_vlans.append(vlans_of_current_file)
    # print(list_of_vlans)
    v_lan_counter_result = vlan_counter(list_of_vlans)
    return v_lan_counter_result


def vlan_counter(list_of_vlans):
    """
    Function calculates how many network elements aggregate on each element
    """
    global_counter = []
    for line in list_of_vlans:
        # print(line)
        local_counter = []
        for i in line:
            if i[0:2] in ('CH', 'CK', 'CR', 'HM', 'KD', 'KI', 'KY', 'MY', 'OD', 'VN'):
                local_counter.append(i.strip())
        global_counter.append(str(len(set(local_counter))))
    # print(global_counter)
    return global_counter


def csv_writer(names_of_nodes, global_counter):
    """
    Function combines two list names_of_nodes, global_counter which were got as results
    from 1st and 3rd function in order to create final file
    """
    names_of_nodes = names_of_nodes
    global_counter = global_counter
    category = []
    for i in global_counter:
        if int(i) == 0:
            category.append('Node should be verified')
        elif 0 < int(i) < 5:
            category.append('TR_Cat_4')
        elif 5 <= int(i) < 10:
            category.append('TR_Cat_3')
        elif 10 <= int(i) < 20:
            category.append('TR_Cat_2')
        else:
            category.append('TR_Cat_1')
    result = zip(names_of_nodes, category, global_counter)
    # print(result)
    header = ['Node_ID', 'Category', 'Amount']
    stamp = datetime.now()
    time_stamp = "_" + stamp.strftime("%Y-%m-%d_%H-%M")
    file_directory = "D:\PyCharm\Project\Project_Parser\/"
    file_name = "Output"
    with open(file_directory + file_name + time_stamp + ".csv", 'w') as output_file:
        writer = csv.writer(output_file, delimiter='\t')
        writer.writerow(header)
        writer.writerows(result)
    with open(file_directory + file_name + time_stamp + ".csv", "r+") as corrected_file:
        new_file = corrected_file.readlines()
        corrected_file.seek(0)
        for line in new_file:
            if line != "\n":
                corrected_file.write(line)
        corrected_file.truncate()
    print('Result file has been created successfully')


getting_files(os.chdir('D:\PyCharm\Project\Project_Parser\DB'))

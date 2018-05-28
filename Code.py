import os
import re
import csv


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
    print(names_of_nodes)
    vlan_parser(list_of_files)
    csv_writer(names_of_nodes)
    # return list_of_files, names_of_nodes


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
    vlan_counter(list_of_vlans)
    # return list_of_vlans


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
    print(global_counter)
    csv_writer(global_counter)
    # return global_counter


def csv_writer(names_of_nodes, global_counter):
    """
    Function combines two list names_of_nodes, global_counter which were got as results
    from 1st and 3rd function in order to create final file
    """
    names_of_nodes = names_of_nodes
    global_counter = global_counter
    result = zip(names_of_nodes, global_counter)
    # print(result)
    with open('output.csv', 'w') as new_file:
        writer = csv.writer(new_file, delimiter='\t')
        writer.writerows(result)
    print('File has been created successfully')


getting_files(os.chdir('D:\PyCharm\Project\Project_Parser\Files'))




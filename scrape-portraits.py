import os
import csv
import requests

parent_dir = 'data-set'
file = 'ss-names.csv'
path = os.path.abspath(file)
image_links = []

with open(file) as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    line_count = 0

    for row in data:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            if os.path.isdir(parent_dir):
                os.mkdir('data-set')
                os.chdir('data-set')
            else:
                os.chdir('data-set')

            folder_name = row[line_count-1].split(
                ', ')[line_count-1].replace(' ', '_')

            if os.path.isdir(folder_name) == False:
                print(f'\nCreating folder: {folder_name}')
                os.mkdir(folder_name)
                os.chdir(folder_name)
                line_count += 1
            else:
                print(f'{folder_name} already exists')

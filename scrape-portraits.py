import os
import csv

parent_dir = 'data-set'
file = 'ss-names.csv'
path = os.path.abspath(file)
image_links = []

with open(file, 'r') as csv_file:
    data = csv.reader(csv_file, delimiter=',')

    if os.path.isdir(parent_dir) == False:
        os.mkdir(parent_dir)
    os.chdir(parent_dir)

    i = 0
    for row in data:
        name = row[i].replace(' ', '_')

        if os.path.isdir(name):
            print(f'A folder called {name} already exists')

        else:
            print(f'\nCreating folder: {name}')
            os.mkdir(name)

import os
import csv
from scraper import scrape_images

parent_dir = 'data-set'
file = 'ss-names.csv'
path = os.path.abspath(file)

# creates the folders for data-set if they don't already exist
with open(file, 'r') as csv_file:
    data = csv.reader(csv_file, delimiter=',')

    if os.path.isdir(parent_dir) == False:
        os.mkdir(parent_dir)
    os.chdir(parent_dir)

    i = 0
    for row in data:
        raw_name = row[i].strip()
        name = row[i].replace(' ', '_')

        if os.path.isdir(name):
            print(f'A folder called {name} already exists')
            os.chdir(name)
            scrape_images(raw_name, 100)
            os.chdir('..')
        else:
            if name != 'Name':
                print(f'\nCreating folder: {name}')
                os.mkdir(name)

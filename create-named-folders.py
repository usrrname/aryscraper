import os
import csv
from scraper import scrape_images

parent_dir = 'data-set'
file = 'ss-names.csv'
path = os.path.abspath(file)

with open(file, 'r') as csv_file:

    data = csv.reader(csv_file, delimiter=',')
    names = [x for x in data if x != 'Name']

    # if data-set folder does not exist, create it
    if os.path.isdir(parent_dir) == False:
        os.mkdir(parent_dir)
    os.chdir(parent_dir)

    index = 1
    while index < len(names):

        name = ''.join(names[index])
        print(name)
        # if folder already exists; scrape 100 images
        if os.path.isdir(name) and name != 'Name':
            print(f'A folder called {name} already exists')
            os.chdir(name)
            scrape_images(name, 100)
            os.chdir('..')
        # creates the folders for data-set if they don't already exist
        else:
            print(f'\nCreating folder: {name}')
            os.mkdir(name)

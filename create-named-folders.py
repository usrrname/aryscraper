import os
import csv
from scraper import download_images

parent_dir = 'data-set'
file = 'ss-names.csv'
path = os.path.abspath(file)


def create_folders(parent_dir, names):
    # if data-set folder does not exist, create it
    if os.path.isdir(parent_dir) == False:
        os.mkdir(parent_dir) and os.chdir(parent_dir)
    # if if exists, move into it
    os.chdir(parent_dir)
    for name in names:
        folder_name = ''.join(name).replace(' ', '_')
        if os.path.isdir(folder_name) == False and folder_name != 'Name':
            print(f'Creating folder {folder_name}')
            os.mkdir(folder_name)
        else:
            # print(f'A folder called {folder_name} already exists')
            break


def create_data_set(file, parent_dir, number_of_images):

    with open(file, 'r') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        names = [x for x in data if x != 'Name']
        create_folders(parent_dir, names)

    index = 1
    # loop through list of names listed from csv file
    while index < len(names):
        # stringify the google search query
        query = ''.join(names[index])
        folder_name = query.replace(' ', '_')

        # if folder already exists; scrape 50 images
        if os.path.isdir(folder_name):
            os.chdir(folder_name)
            download_images(query, number_of_images)
            os.chdir('..')
        index += 1

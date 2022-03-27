import os
import csv
from scraper import download_images

parent_dir = 'data-set'
file = 'ss-names.csv'
path = os.path.abspath(file)


def create_data_set(file, parent_dir, number_of_images):

    with open(file, 'r') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        names = [x for x in data if x != 'Name']

        # if data-set folder does not exist, create it
        if os.path.isdir(parent_dir) == False:
            os.mkdir(parent_dir)
        os.chdir(parent_dir)
        index = 1
        # loop through list of names listed from csv file
        while index < len(names):
            # stringify the google search query
            query = ''.join(names[index])
            folder_name = query.replace(' ', '_')

            # if folder already exists; scrape 50 images
            if os.path.isdir(folder_name) and folder_name != 'Name':
                print(f'A folder called {folder_name} already exists')
                os.chdir(folder_name)
                download_images(query, number_of_images)
                os.chdir('..')
                index += 1
            # creates the folders for data-set if they don't already exist
            else:
                print(f'\nCreating folder: {folder_name}')
                os.mkdir(folder_name) and os.chdir(folder_name)
                download_images(query, number_of_images)
                os.chdir('..')
                index += 1


create_data_set('ss-names.csv', 'data-set', 50)

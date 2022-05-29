import os
from scraper import download_images
from util import list_folders, sanitize_names_for_folders


def create_folders(parent_dir, names):
    folder_names = sanitize_names_for_folders(names)
    # if data-set folder does not exist, create it
    if os.path.isdir(parent_dir) == False:
        os.mkdir(parent_dir) and os.chdir(parent_dir)
    # if if exists, move into it
    os.chdir(parent_dir)

    for folder in folder_names:
        if os.path.isdir(folder) == False and folder != 'Name':
            print(f'Creating folder {folder}')
            os.mkdir(folder)
        else:
            print(f'A folder called {folder} already exists')
    list_folders(os.getcwd())


def create_data_set(names, number_of_images):
    flattened_names = []
    transformed_names = [flattened_names.append(''.join(name))
                         for name in names if name != 'Name']
    folder_names = sanitize_names_for_folders(names)

    if os.getcwd() != 'data-set':
        os.chdir('data-set')

    index = 0
    # loop through list of names listed from csv file
    while index < len(names):

        if os.path.isdir(folder_names[index]) == True and folder_names[index] != 'Name':

            # if folder already exists; scrape 50 images
            os.chdir(folder_names[index])
            print('switching to folder: ' + folder_names[index])
            # stringify the google search query
            query = ''.join(names[index]).strip()
            try:
                download_images(query, number_of_images)
                os.chdir('..')
            except Exception as e:
                print(e)
                print(
                    f'Error downloading images from {folder_names[index]}')
                os.chdir('..')
        index += 1

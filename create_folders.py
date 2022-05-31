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

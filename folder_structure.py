import os
from scraper import download_images
from util import list_folders, write_csv_header
from glob import glob


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
            print(f'A folder called {folder_name} already exists')
            break
    list_folders(os.getcwd())


def create_raw_data_set(name, number_of_images):

    folder_name = name.replace(' ', '_')

    # if folder already exists; scrape 50 images
    if os.path.isdir(folder_name):
        os.chdir(folder_name)
        print(f'\nScraping images for {name}')
        os.mkdir('raw') and os.chdir('raw')
        print('Created raw and test folders in {}'.format(os.getcwd()))
        download_images(name, number_of_images)
        os.chdir('../..')

    # list most recently updated image index
    image_index = len(os.listdir(
        glob({folder_name/'raw/*jpg|png|jpeg|svg|gif|webp|bmp'})))
    print(f'\n{image_index} images scraped for {name}')

import os
import json
from scraper import download_images
from util import list_folders, sanitize_names_for_folders, get_names_from_csv, remove_html_tags, write_csv_header, write_to_csv, add_row_to_csv
from bs4 import BeautifulSoup
import shutil


def find_names_in_wikimedia_response(filename, names):
    """ finds names in wikimedia commons image api response, 
    creates folders, 
    then moves the image into the folder"""

    query = {}
    with open(filename, "r") as read_file:
        response = json.load(read_file)
        query = response['query']['pages']
    read_file.close()

    page_ids = list(query.keys())

    for pid in page_ids:
        filename = query[pid]['title'][5:]
        imageinfo = query[pid]['imageinfo'][0]['extmetadata']
        object_name_value = imageinfo['ObjectName']['value']
        object_name = remove_html_tags(object_name_value)
        file_ext = os.path.splitext(query[pid]['title'])[1]
        description_value = imageinfo['ImageDescription']['value'] or ''
        originaldate = imageinfo['DateTimeOriginal']['value'] or ''
        credit_value = imageinfo['Credit']['value'] or ''
        credit = remove_html_tags(credit_value)
        description = remove_html_tags(description_value)
        str_match = [
            s for s in names if s in description or object_name]

        for item in range(len(str_match)):
            folder_name = ''.join(str_match[item]).replace(' ', '_')
            filename = folder_name + file_ext

            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
            try:
                if not os.path.exists(filename):
                    continue
                else:
                    shutil.move(f'{filename}', f'{folder_name}/{filename}')
            except Exception as e:
                print(e)
            finally:
                continue


def create_folders(parent_dir, names):
    folder_names = sanitize_names_for_folders(names)
    # if data folder does not exist, create it
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

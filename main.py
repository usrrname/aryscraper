#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from scrape_names import scrape_ss_names
from create_folders import create_folders
from util import get_names_from_csv, sanitize_names_for_folders
from scraper import download_images


# def process():
#     print("Creating folders...")
#     create_folders('data-set', names)
#     print("Done!")


def main():
    names = get_names_from_csv('ss-info.csv')
    folder_names = sanitize_names_for_folders(names)
    name_map = dict(zip(folder_names, names))
    last_folder = ''
    current_path = os.getcwd()
    index = 0
    try:
        for index, fname in enumerate(folder_names):
            query = name_map[fname]
            os.chdir(f'{current_path}/data-set/{fname}')
            download_images(query, 100)
            os.chdir('../../')
    except Exception as e:
        last_folder = f'{fname}'
        print(f'Error downloading images from {fname}, {e.args}')
        file = open('../../index.txt', 'w')
        file.writelines(last_folder)
        file.close()
        sys.exit(2)
        os.chdir('../../')
    index+1


if __name__ == '__main__':
    # process()
    main()

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
#     create_folders('data', names)
#     print("Done!")
def download_and_save_err(last_folder, query):
    try:
        download_images(query, 100)
    except Exception as e:
        print(e)
        file = open('../../index.txt', 'w')
        file.writelines(last_folder)
        pass


def main():
    names = get_names_from_csv('ss-info.csv')
    folder_names = sanitize_names_for_folders(names)
    name_map = dict(zip(folder_names, names))
    os.chdir('data')
    last_folder = ''

    # record of last folder and search download that failed
    if os.path.exists('index.txt'):
        file = open('index.txt', 'r')
        last_folder = file.readlines()[0]
        folder_index = folder_names.index(last_folder)
        os.chdir(last_folder)
        query = name_map[last_folder]
        download_and_save_err(last_folder, query)

    else:
        current_path = os.getcwd()

        for fname in folder_names:
            query = name_map[fname]

            try:
                os.chdir(f'{current_path}/{fname}')
                download_images(query, 100)
            except Exception as e:
                last_folder = f'{fname}'
                print(f'Error downloading images from {fname}, {e.args}')
                file = open('../../index.txt', 'w')
                file.writelines(last_folder)
                file.close()
                continue


if __name__ == '__main__':
    # process()
    main()

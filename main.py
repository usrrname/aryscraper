#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from scrape_names import scrape_ss_names
from create_folders import create_folders
from util import get_names_from_csv, sanitize_names_for_folders
from scraper import download_images
names = get_names_from_csv('ss-info.csv')
folder_names = sanitize_names_for_folders(names)
name_map = dict(zip(folder_names, names))

# def process():
#     print("Creating folders...")
#     create_folders('data', names)
#     print("Done!")


def download_and_save_err(last_folder, query):
    try:
        download_images(query, 100)
    except Exception as e:
        os.chdir('../')
        print(e)
        file = open('failed.txt', 'a')
        file.writelines(last_folder + '\n')
    finally:
        folder_index = folder_names.index(last_folder)
        next_folder = folder_names[folder_index+1]
        main(next_folder)


def main(folder_name):
    if 'data' not in os.getcwd():
        print(os.getcwd())
        os.chdir('./data')

    last_folder = folder_name
    os.chdir(last_folder)
    query = name_map[last_folder]
    download_and_save_err(last_folder, query)


if __name__ == '__main__':
    # process()
    main('Professor_Dr_Wilhelm_Pfannenstiel')

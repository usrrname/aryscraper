#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# this script only works inside /data folder
import os
import sys
from scrape_names import scrape_ss_names
from create_folders import create_folders
from util import get_names_from_csv, sanitize_names_for_folders
from scraper import download_images, list_images_in_folder
names = get_names_from_csv('ss-info.csv')
folder_names = sanitize_names_for_folders(names)
name_map = dict(zip(folder_names, names))


def process():
    print("Creating folders...")
    create_folders('data', names)
    print("Done!")


def download_and_save_err(last_folder, query):
    try:
        download_images(query, 100)
    except Exception as e:
        os.chdir('../')
        print(f'{Exception} {e.args}')
        file = open('failed.txt', 'a')
        file.writelines(last_folder + '\n')
        file.close()
    finally:  # calls the main function to run search on next folder
        folder_index = folder_names.index(last_folder)
        next_folder = folder_names[folder_index+1]
        scrape_one_person(next_folder)


def scrape_one_person(folder_name):
    """retrieves google image search result images from SERPAPI for 1 person """
    if 'data' not in os.getcwd():
        os.chdir('./data')

    os.chdir(folder_name)
    query = name_map[folder_name]
    download_and_save_err(folder_name, query)


def find_unpopulated_folders(min_imgs, max_images):
    """finds folders that dont have any images in them"""
    empty_folders = []

    for index in range(len(folder_names)):
        num_of_images = list_images_in_folder(max_images, folder_names[index])

        if num_of_images == 0:
            empty_folders.extend([folder_names[index]])
            os.chdir('../')
        else:
            os.chdir('../')
    return empty_folders


if __name__ == '__main__':

    """Finds empty folders in which images dont exists and runs scraping on them"""
    os.chdir('data')
    empty_folders = find_unpopulated_folders(5, 100)

    for folder in empty_folders:
        os.chdir(folder)
        query = name_map[folder]
        try:
            download_and_save_err(folder, query)
        except Exception as e:
            print(e)
            continue

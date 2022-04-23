#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from scrape_names import scrape_ss_names
from folder_structure import create_folders, create_data_set
from util import get_names_from_csv

names = get_names_from_csv('ss-names.csv')


def process():
    filename = 'ss-names.csv'
    url = 'https://en.wikipedia.org/wiki/List_of_SS_personnel'
    header = ['Name']
    print("Scraping SS names...")
    scrape_ss_names(url, filename, header)
    print("Creating folders...")
    create_folders('data-set', names)
    print("Done!")


def main():
    create_data_set(names, 50)
    print("Creating data-set...")


if __name__ == '__main__':
    process()
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from folder_structure import create_folders, create_data_set
from names_from_csv import get_names_from_csv

names = get_names_from_csv('ss-names.csv')


def process():

    print("Creating folders...")
    create_folders('data-set', names)


def main():
    create_data_set(names, 50)
    print("Creating data-set...")


if __name__ == '__main__':
    process()
    main()

from util import get_image_format, get_image_link, is_already_saved, image_extensions, has_img_extension, list_folders, get_names_from_csv, sanitize_names_for_folders, add_row_to_csv, write_csv_header, read_json, last_row_from_csv
import csv
import requests
from serpapi import GoogleSearch
from dotenv import load_dotenv
from pathvalidate import sanitize_filename
from PIL import Image
import os
import sys
from glob import glob1
import urllib.request

load_dotenv()

token = os.environ.get('SERP_API_KEY')

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.5"}

ambiguous_names = ['Adam Grünewald', 'Anton Burger',
                   'Karl Otto von Salisch', 'Yuri Frolov']


def scrape_images(name, number_of_images, start_number):
    name = str(name)
    query = ''

    if any(name for word in ambiguous_names):
        # clarify search for names that are common
        query = name + ' nazi'

    else:
        query = name + (' portrait')  # standard query string

    params = {
        "api_key": token,
        "engine": "google",
        "ijn": "0",
        "start": start_number,
        "num": number_of_images,
        "q": query,
        "google_domain": "google.com",
        "tbm": "isch",
        'tbs': 'images'
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    image_results = results['images_results']

    try:
        # saves json of response incase of failure
        urllib.request.urlretrieve(
            results['search_metadata']['json_endpoint'], 'data.json')
        print('data.json for {query} saved!')
        filtered_images = [
            image for image in image_results if image['original']]
    except KeyError in Exception as e:
        print(f'{KeyError}: {e}')
    except TypeError in Exception as e:
        print(f'{TypeError}: {e}')
    return filtered_images


def save_images(name, image_urls, next_image_index=0):
    if next_image_index != 0:
        i = next_image_index

    for i, image in enumerate(image_urls):

        # get the image extension
        img_ext = get_image_format(image['original'])

        if img_ext not in image_extensions or None:
            continue

        title = image['title']
        img_position = image['position']  # position in search results
        file_title = sanitize_filename(name).lower().replace(
            ' ', '').strip('_')[:6]  # trim the file title for consistency

        filename = f'{i}-{file_title}{img_ext}'
        data_row = [name, filename, title,
                    img_position, image['original']]
        try:
            current_path = os.getcwd()
            with open(current_path + "/" + filename, 'wb') as handler:
                print(f'\nDownloading: {image["original"]}')
                img_data = requests.get(get_image_link(
                    image['original']), headers=headers).content
                handler.write(img_data)
                print(f'\n Successfuly Saved: {filename}')
                handler.close()
        except KeyError as e:
            print(
                f'\nMapping of original key not found: {KeyError}, {e}')
        except Exception as e:
            print(f'{e}')
            continue

        # add info about saved image
        try:
            if not os.path.exists('data-info.csv'):
                write_csv_header(
                    'data-info.csv', ["Name", "Filename", "Title", "Position", "Original URL"])
                add_row_to_csv(current_path + '/' + 'data-info.csv', data_row)
            elif is_already_saved(data_row, 'data-info.csv') == False:
                add_row_to_csv(current_path + '/' + 'data-info.csv', data_row)
        except Exception as e:
            print(f'\n Failed to Save: data-info.csv at the {i}th file, {e}')


def lookup_recent_row(csv_file):
    # finds image position in returned response
    most_recent_row = last_row_from_csv(csv_file)
    last_image_index = int(most_recent_row[3])

    # gets last index used to prepend filename
    next_image_index = int(most_recent_row[1].split('-')[0]) + 1
    print(
        f'last image index: {last_image_index}\n next image index: {next_image_index}')
    return next_image_index, last_image_index


def download_images(name, number_of_images):

    if not os.path.exists('raw'):  # if raw images folder doesnt exist, create it
        os.mkdir('raw') and os.chdir('raw') and write_csv_header(
            'data-info.csv', ["Name", "Filename", "Title", "Position", "Original URL"])
    else:  # if folder already exists, check for last saved image
        os.chdir('raw')

    files = os.listdir(os.getcwd())

    images_only = [file for file in files if has_img_extension(file)]

    number_of_files_in_folder = len(images_only)

    print(
        f'Status: {number_of_files_in_folder}/{number_of_images} files in {os.getcwd()}')

    if number_of_files_in_folder >= number_of_images:
        print(
            f'{number_of_files_in_folder} files in folder, only require {number_of_images} images\nFolder contains enough images. Skipping download.')
        return

    else:
        remainder = 100 - number_of_files_in_folder
        print(
            f'{number_of_files_in_folder} files in folder, need {remainder} more images')

        start_number = 0
        image_urls = []

        if remainder >= 1 and os.path.isfile('data.json'):
            last_image_index, next_image_index = 0, 1
            image_results = read_json('data.json')

            # find json file and fetch remaining images
            if os.path.exists('data-info.csv'):
                next_image_index, last_image_index = lookup_recent_row(
                    'data-info.csv')
                print(
                    f'last image position: {last_image_index}, next image number: {next_image_index}')
            image_urls = [
                image for image in image_results if image['position'] > last_image_index]

            save_images(name, image_urls, next_image_index)
        else:
            start_number = 1
            image_urls = scrape_images(name, number_of_images, start_number)
            save_images(name, image_urls)

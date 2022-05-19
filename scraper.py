import csv
import requests
from serpapi import GoogleSearch
from dotenv import load_dotenv
from pathvalidate import sanitize_filename
import os

from util import get_image_format, get_image_link, has_extension
load_dotenv()

token = os.environ.get('SERP_API_KEY')

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.5"}


def scrape_images(name, number_of_images, start_number):
    params = {
        "api_key": token,
        "engine": "google",
        "ijn": "0",
        "start": start_number,
        "num": number_of_images,
        "q": name + ' portrait',
        "google_domain": "google.com",
        "tbm": "isch",
        'tbs': 'images'
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    image_results = results['images_results']

    filtered_images = [image for image in image_results if 'original' in image
                       and has_extension(image['original'])]
    return filtered_images


def download_images(name, number_of_images):
    current_path = os.getcwd()
    number_of_files_in_folder = len(next(os.walk(current_path))[2])

    print(
        f'currently {number_of_files_in_folder} / {number_of_images} files in {os.getcwd()}')

    if number_of_files_in_folder >= number_of_images:
        print(
            f'{number_of_files_in_folder} files in folder, only require {number_of_images} images\nFolder contains enough images. Skipping download.')
        return

    elif number_of_files_in_folder < number_of_images:
        remainder = 50 - number_of_files_in_folder
        start_number = 0
        print(
            f'{number_of_files_in_folder} files in folder, need {remainder} more images')
        if remainder < 0:
            start_number = 0
        image_urls = scrape_images(name, number_of_images, start_number)

        for image in image_urls:

            print(f'\nDownloading: { image["original"]}')
            title = image[title]

            # get the image extension
            img_ext = get_image_format(image['original'])
            img_data = requests.get(get_image_link(
                image['original']), headers=headers).content
            img_position = image['position']

            file_title = sanitize_filename(name).lower().replace(' ', '')[:6]

            filename = f'{img_position}-{file_title}{img_ext}'
            data_row = [filename, image['title'], image['position'],
                        image['thumbnail'], image['original']]

            if os.path.isfile(filename):
                print(f'{filename} already exists')
                break
            else:
                try:
                    with open(current_path + "/" + title + img_ext, 'wb') as handler:
                        handler.write(img_data)
                        print(f'\n Successfuly Saved: {filename}')
                        handler.close()
                    with open('../data_info.csv', 'a') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(data_row)
                        csv_file.close()
                except KeyError as e:
                    print(f'\nMapping of original key not found: {KeyError}')
                except Exception as e:
                    print(f'\n Failed to Save: {filename}')

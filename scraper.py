from unittest import skip
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


def scrape_images(query_string, number_of_images):
    image_urls = []
    params = {
        "api_key": token,
        "engine": "google",
        "ijn": "0",
        "start": 0,
        "num": number_of_images,
        "q": query_string + ' portrait',
        "google_domain": "google.com",
        "tbm": "isch",
        'tbs': 'images'
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    image_results = results['images_results']

    while len(image_urls) < number_of_images:
        for image in image_results:
            if (image['original'] and has_extension(image['original'])):
                image_name = sanitize_filename(
                    image['title']).replace(' ', '_')
                image_urls.append(tuple((image_name, image['original'])))
            else:
                position = image['position']
                print(
                    f'{position}th search result does not have a valid image extension or its original image url does not exist')
                break
    return image_urls


def download_images(query, number_of_images):
    current_path = os.getcwd()
    number_of_files_in_folder = len(next(os.walk(current_path))[2])

    print(
        f'currently {number_of_files_in_folder} / {number_of_images} files in {os.getcwd()}')

    if number_of_files_in_folder >= number_of_images:
        print(
            f'{number_of_files_in_folder} files in folder, only require {number_of_images} images\nFolder contains enough images. Skipping download.')
        return

    elif number_of_files_in_folder < number_of_images:
        print(query)
        image_urls = scrape_images(query, number_of_images)

        for image_name, image_url in image_urls:

            print(f'\nDownloading: {image_url}')

            # get the image extension
            img_ext = get_image_format(image_url)
            img_data = requests.get(get_image_link(
                image_url), headers=headers).content
            filename = image_name + img_ext

            if os.path.isdir(filename):
                print(f'{filename} already exists')
                break
            else:
                with open(current_path + "/" + image_name + img_ext, 'wb') as handler:
                    try:
                        handler.write(img_data)
                        print(f'\n Successfuly Saved: {filename}')
                    except KeyError as e:
                        print(
                            f'\nMapping of original key not found: {KeyError}')
                    except Exception as e:
                        print(f'\n Failed to Save: {filename}')

                    handler.close()

from util import get_image_format, get_image_link, is_already_saved
import csv
from glob import glob
import requests
from serpapi import GoogleSearch
from dotenv import load_dotenv
from pathvalidate import sanitize_filename
import os

load_dotenv()

token = os.environ.get('SERP_API_KEY')

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.5"}

ambiguous_names = ['Anton Burger']


def scrape_images(name, number_of_images, start_number):

    if name in ambiguous_names:
        name.join(' Nazi')      # clarify search for names that are common
    else:
        name.join(' portrait')  # standard query string

    query = name

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

    filtered_images = [image for image in image_results if 'original' in image
                       and get_image_format(image['original']) in ['.jpg', '.png', '.jpeg', '.svg', '.gif', '.webp', '.bmp']]
    print(filtered_images)
    return filtered_images


def download_images(name, number_of_images):
    current_path = os.getcwd()
    number_of_files_in_folder = len(next(os.walk(current_path))[2])
    image_index = len(os.listdir(
        glob({current_path/'raw/*jpg|png|jpeg|svg|gif|webp|bmp'})))
    print(image_index)

    print(
        f'currently {number_of_files_in_folder} / {number_of_images} files in {os.getcwd()}')

    if number_of_files_in_folder >= number_of_images:
        print(
            f'{number_of_files_in_folder} files in folder, only require {number_of_images} images\nFolder contains enough images. Skipping download.')
        return

    elif number_of_files_in_folder < number_of_images:
        remainder = 50 - number_of_files_in_folder
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
            img_position = image['position']  # position in search results
            file_title = sanitize_filename(name).lower().replace(
                ' ', '')[:6]  # trim the file title for consistency
            filename = f'{img_position}-{file_title}{img_ext}'
            data_row = [name, filename, title, img_position, image['original']]

            if is_already_saved(data_row) == False:
                try:
                    with open(current_path + "/" + title + img_ext, 'wb') as handler:
                        img_data = requests.get(get_image_link(
                            image['original']), headers=headers).content
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
                    print(f'\n Failed to Save: {filename}, {e.message}')
            else:
                print(f'Image already in data-info.csv, skipping to next image')
                break

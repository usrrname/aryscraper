import imghdr
import requests
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

from util import hasExtension
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
    path = os.getcwd()

    for image in image_results:

        if (image['original'] and hasExtension(image['original'])):
            image_name = image['title'].strip().replace(
                ' ', '_').replace('-', '_').replace(',', '').replace('.', '').replace('/', '').replace('|', '').replace('/', '')
            image_urls.append(tuple((image_name, image['original'])))
            continue
        else:
            position = image['position']
            print(
                f'image at position {position} does not have a valid image extension or original url does not exist')

    for image_name, image_url in image_urls:
        print(f'\nDownloading image: {image_url}')
        img_ext = '.' + str(image_url).split('.')[-1] or '.jpg'
        img_data = requests.get(image_url, headers=headers).content
        filename = image_name + img_ext
        with open(path + "/" + image_name + img_ext, 'wb') as handler:
            handler.write(img_data)
            print(f'\n Successfully saved: {filename}')
            handler.close()

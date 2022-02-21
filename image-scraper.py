import requests
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
load_dotenv()

token = os.environ.get('SERP_API_KEY')

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.9"}


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

    path = os.path.abspath('data-set/' + query_string.replace(' ', '_'))

    for image in image_results:
        image_name = image['source'].strip()
        image_urls.append(tuple((image_name, image['original'])))

    for (img_name, img_url) in image_urls:
        str_arr = str(img_url).split('.')
        print(str_arr)
        img_ext = '.' + str_arr[-1]
        print(img_ext)
        img_data = requests.get(img_url, headers=headers).content
        with open(path + "/" + img_name + img_ext, 'wb') as handler:
            handler.write(img_data)
        handler.close()



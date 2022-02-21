from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
load_dotenv()

token = os.environ.get('SERP_API_KEY')


def scrape_image_urls(query_string, number_of_images):
    image_urls = []
    params = {
        "api_key": token,
        "engine": "google",
        "ijn": "0",
        "start": 0,
        "num": number_of_images,
        "q": query_string + 'portrait',
        "google_domain": "google.com",
        "tbm": "isch",
        'tbs': 'images'
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    image_results = results['images_results']

    for image in image_results:
        image_urls += [image['original']]

    return image_urls

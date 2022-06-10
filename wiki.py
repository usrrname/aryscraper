import pandas as pd
import requests
import json
from util import save_as_json


def get_abstract(lang, subject):

    url = f'https://{lang}.wikipedia.org/w/api.php'

    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts|links",
        "titles": subject,
        "format": 'json',
        "exintro": 1,
    }

    response = requests.get(url, params)
    data = response.json()
    page = next(iter(data['query']['pages'].values()))
    summary = page['extract']
    links = [{'title': link['title'], 'href': f'https://{lang}.wikipedia.org/wiki/' + link['title'].replace(' ', '_')}
             for link in page['links']]
    info = {
        'name': subject,
        'extract': summary,
        'links': links
    }
    return info


name = ''
data = get_abstract('de', name)
filename = name.replace(' ', '_') + '.json'
save_as_json(filename, data)

from functools import wraps
import translators as ts
import os
import pandas as pd
import requests
import json
from util import save_as_json, extract_info
import uuid


def get_wikidata(lang, subject, filename):
    # entering a name hits wikipedia api and creates a json in the name of the figure
    """parameters
    locale: two letter language locale
    subject: name of party member
    filename: filename with .json extension
    """

    url = f'https://{lang}.wikipedia.org/w/api.php'

    wiki_query = subject.strip().replace(' ', '_')

    params = {
        "action": "query",
        "format": "json",
        "prop": "description|extracts|links|pageimages",
        "redirects": 1,
        "utf8": 1,
        "piprop": "original",
        "pilimit": "2",
        "pllimit": 10,
        "plnamespace": "0",
        "titles": wiki_query,
        "exintro": 1,
        "explaintext": 1,
        "format": 'json',
        "exintro": 1,
    }

    response = requests.get(url, params)
    data = response.json()
    page = next(iter(data['query']['pages'].values()))

    id = uuid.uuid4()
    links = []
    extract, description, img_url = '', '', ''

    extract = extract_info(lang, page, 'extract')
    description = extract_info(lang, page, 'description')

    try:
        links = [{'title': link['title'], 'href': f'https://{lang}.wikipedia.org/wiki/' + link['title'].replace(' ', '_')}
                 for link in page['links']]
    except Exception as e:
        file = open(f'failed_{lang}.txt', 'a')
        file.writelines(f'{subject} {l} {e}' + '\n')
        file.close()
        pass

    try:
        img_url = page['original']['source']
    except Exception as e:
        file = open(f'failed_{lang}.txt', 'a')
        file.writelines(f'{subject} {l} {e}' + '\n')
        file.close()
        pass

    if lang != 'en':
        extract = ts.google(extract)
        description = ts.google(description)
        links = [{'title': ts.google(link['title']), 'href': f'https://{lang}.wikipedia.org/wiki/' +
                  link['title'].replace(' ', '_')} for link in links]

    # TODO: include s3 url in returned info
    info = {
        'id': str(id),
        'name': subject,
        'src': img_url,
        'filename': filename,
        'description': extract,
        'about': description,
        'links': links
    }

    return info


def create_name_filename_map(current_path):
    """creates a map of the name and the filename by transforming folder name into the raw name"""
    dirnames = []
    filenames = []

    for root, dirs, files in os.walk(current_path):
        dirnames.extend([f for f in dirs if not f[0] == '.'])
        filenames.extend([d for d in files if not d[0] == '.'][:1])

    names = [name.replace('_', ' ') for name in dirnames]
    img_dict = dict(zip(names, filenames))

    return img_dict



folder_map = create_name_filename_map('./women')
locales = ['en', 'de', 'nl', 'fr', 'pl', 'pt', 'sv', 'lv']
faces = []

for k, v in folder_map.items():
    for lang in locales:
        try:
            person_meta = get_wikidata(lang, k, v)
            faces.append(person_meta)
            break
        except:
            pass
        finally:
            save_as_json('women.json', faces)

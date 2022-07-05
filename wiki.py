from functools import wraps
import translators as ts
import os
from getopt import getopt
import sys
import pandas as pd
import requests
import json
from util import save_as_json, extract_info
import uuid


def get_wikidata(lang, subject, filename):
    """
    Makes wikipedia api query and returns a dict object with the relevant metadata
    ===Parameters===
    lang: two letter language locale like en/de
    subject: name of party member with spaces, should be an accepted route name for wikipedia query
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
    url = ''
    if response.status_code == 200:
        url = f'https://{lang}.wikipedia.org/wiki/{wiki_query}'

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
        'url': url,
        'filename': filename,
        'description': extract,
        'about': description,
        'links': links
    }

    return info


def create_name_filename_map(current_path):
    """Creates a map of the name and the filename by transforming folder name into the raw name"""
    dirnames = []
    filenames = []

    for root, dirs, files in os.walk(current_path):
        dirnames.extend([f for f in dirs if not f[0] == '.'])
        filenames.extend([d for d in files if not d[0] == '.'][:1])

    names = [name.replace('_', ' ') for name in dirnames]
    img_dict = dict(zip(names, filenames))

    return img_dict


def main(argv):
    dirname = ''
    outputfile = ''
    try:
        opts, args = getopt(
            argv, "hd:o:", [sys.argv[1:], "dirname=", "ofile="])
    except getopt.GetoptError as err:
        print('wiki.py -d <dirname> -o <outputfile> {err}')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('wiki.py -d {dirname} -o {outputfile}')
            sys.exit()
        elif opt in ("-d", "--dirname"):
            dirname = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        else:
            assert False, "unhandled option"

    print('Input directory is "', dirname)
    print('Output file is "', outputfile)

    folder_map = create_name_filename_map(dirname)
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
                save_as_json(outputfile, faces)


if __name__ == '__main__':
    main(sys.argv[1:])

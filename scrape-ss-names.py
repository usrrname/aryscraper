import requests
from bs4 import BeautifulSoup
import os
import csv
from util import remove_contents_in_brackets

file = 'ss-names.csv'
path = os.path.abspath(file)

url = "https://en.wikipedia.org/wiki/List_of_SS_personnel"
result = requests.get(url)

header = ['Name']
personnel = []

if result.status_code == 200:
    soup = BeautifulSoup(result.content, "html.parser")
    for a in soup.select("#mw-content-text h3+table td:first-child:not([colspan]) a"):
        if (a.get("href").startswith("/wiki/")):
            raw_title = a.get('title')
            name = remove_contents_in_brackets(raw_title)
            personnel.append([name])

            with open(file, 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                [writer.writerow(a) for a in personnel]
            f.close()

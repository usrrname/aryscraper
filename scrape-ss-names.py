import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import csv

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
            name = a.get('title')
            personnel.append(name)

            with open(file, 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerow([personnel])
            f.close()

import requests
from bs4 import BeautifulSoup
import csv
from util import remove_contents_in_brackets


def scrape_ss_names(url, filename, header):
    personnel = []
    result = requests.get(url)

    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")
        for a in soup.select("#mw-content-text h3+table td:first-child:not([colspan]) a"):
            if (a.get("href").startswith("/wiki/")):
                raw_title = a.get('title')
                name = remove_contents_in_brackets(raw_title)
                personnel.append([name])

                with open(filename, 'w', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    [writer.writerow(a) for a in personnel]
                f.close()
                return personnel

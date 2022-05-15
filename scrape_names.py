import requests
from bs4 import BeautifulSoup
from util import remove_contents_in_brackets, write_to_csv


def request_soupified_response(url):
    result = requests.get(url)

    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")
        return soup
    else:
        print(f'{result.status_code} error')
        return None


def scrape_ss_names(url, filename, header):
    personnel = []
    soup = request_soupified_response(url)
    for a in soup.select("#mw-content-text .mw-parser-output h3+table td:first-child:not([colspan]) a"):
        if (a.get("href").startswith("/wiki/")):
            raw_title = a.get('title')
            name = remove_contents_in_brackets(raw_title)
            personnel.append([name])

    personnel.sort()
    write_to_csv(filename, personnel, header)
    return personnel


def scrape_law_enforcement_names():
    personnel = []
    url = 'https://en.wikipedia.org/wiki/List_of_law_enforcement_officers_convicted_for_an_on-duty_killing_in_the_United_States'
    soup = request_soupified_response(url)
    for td in soup.select("#mw-content-text table.wikitable.sortable td:nth-child(2)"):
        personnel.append(td.text.replace('\n', ''))
        return personnel

from csv import writer
import pandas as pd
import requests
from bs4 import BeautifulSoup
from util import remove_contents_in_brackets, write_person_data_to_table, write_to_csv


def request_soupified_response(url):
    result = requests.get(url)

    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")
        return soup
    else:
        print(f'{result.status_code} error')
        return None


def scrape_ss_names(url, filename, header):
    collected_names = []
    soup = request_soupified_response(url)
    ranks = []
    for heading in soup.select('.mw-headline'):
        ranks.append(heading.text)

    for a in soup.select("#mw-content-text .mw-parser-output h3+table td:first-child:not([colspan]) a"):

        if (a.get("href").startswith("/wiki/")):
            raw_title = a.get('title')
            name = remove_contents_in_brackets(
                raw_title).replace('"', '').replace(',', '')
            collected_names.append(name)
    for a in soup.select('h2+table td:first-child:not([colspan]) a'):
        if (a.get("href").startswith("/wiki/")):
            raw_title = a.get('title')
            name = remove_contents_in_brackets(
                raw_title).replace('"', '').replace(',', '')
            collected_names.append(name)

    personnel = list(dict.fromkeys(collected_names))
    personnel.sort()
    person_list = [[person] for person in personnel]
    write_to_csv(filename, person_list, header)
    return person_list


def scrape_ss_data(url, filename):
    soup = request_soupified_response(url)
    tables = soup.find_all('table', {'align': 'center'})
    subject_tables = []
    for table in tables:
        new_table = []
        headings = table.find_all('th')
        header = [th.text.replace('\n', '') for th in headings]
        new_table.extend([header])
        for row in table.find_all('tr'):
            # Find all data for each column
            cells = row.find_all('td')
            new_row = [cell.text.replace('\n', '') for cell in cells]
            new_table.extend([new_row])
        subject_tables.extend(new_table)

    write_person_data_to_table(filename, subject_tables)


def scrape_law_enforcement_names(url, filename, header):
    personnel = []
    soup = request_soupified_response(url)
    for td in soup.select("#mw-content-text table.wikitable.sortable td:nth-child(2)"):
        personnel.append(td.text.replace('\n', ''))
        personnel.sort()
    write_to_csv(filename, personnel, header)
    return personnel

from warnings import catch_warnings
import requests
from bs4 import BeautifulSoup
from util import get_classifier_and_label, get_labels_from_csv, remove_contents_in_brackets, write_person_data_to_table, write_to_csv


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

    for a in soup.select("#mw-content-text .mw-parser-output h3+table td:first-child:not([colspan]) a"):

        if (a.get("href").startswith("/wiki/")):
            raw_title = a.get('title')
            name = remove_contents_in_brackets(
                raw_title).replace('"', '').replace(',', '')
            collected_names.append(name)

    for cell in soup.select('h2+table td:first-child:not([colspan])'):

        if (cell.get("href").startswith("/wiki/")):
            raw_title = a.get('title')
            name = remove_contents_in_brackets(
                raw_title).replace('"', '').replace(',', '')
            collected_names.append(name)
        else:
            print(cell.text)

    personnel = list(dict.fromkeys(collected_names))
    personnel.sort()
    person_list = [[person] for person in personnel]
    write_to_csv(filename, person_list, header)
    return person_list


scrape_ss_names(
    'https://en.wikipedia.org/wiki/List_of_SS_personnel', 'ss-names.csv', ['Name'])


def scrape_ss_data(url, filename):
    soup = request_soupified_response(url)
    tables = soup.find_all('table', {'align': 'center'})
    subject_tables = []
    labels_map = get_labels_from_csv('ss-ranks.csv')
    labels = list(labels_map.keys())

    for table in tables:
        new_table = []
        headings = table.find_all('th')
        header = [th.text.replace('\n', '') for th in headings]
        header.extend(['Class', 'Label'])
        new_table.extend([header])
        rows = table.find_all('tr')

        for row in rows[1:]:
            # Find all data for each column
            cells = row.find_all('td')

            row_data = [cell.text.replace('\n', '').replace('\xa0', '')
                        for cell in cells if cell.text not in labels]
            try:
                result = get_classifier_and_label(rows[1])
                if result != []:
                    row_data.extend(result)
                new_table.extend([row_data])
            except TypeError in Exception:
                print(TypeError)
            except ValueError:
                print(ValueError)
        subject_tables.extend(new_table)
    write_to_csv(filename, subject_tables, header=[])


# scrape_ss_data(
#     'https://en.wikipedia.org/wiki/List_of_SS_personnel', 'ss-info.csv')


def scrape_law_enforcement_names(url, filename, header):
    personnel = []
    soup = request_soupified_response(url)
    for td in soup.select("#mw-content-text table.wikitable.sortable td:nth-child(2)"):
        personnel.append(td.text.replace('\n', ''))
        personnel.sort()
    write_to_csv(filename, personnel, header)
    return personnel

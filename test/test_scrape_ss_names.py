

from util import get_names_from_csv
from scrape_names import scrape_ss_names


def test_scrape_ss_names_function():
    expected_ss_name_set = get_names_from_csv('ss-names.csv')

    assert(scrape_ss_names('https://en.wikipedia.org/wiki/List_of_SS_personnel',
           'ss-names-test.csv', ['Name']))

    actual = get_names_from_csv('ss-names-test.csv')

    assert expected_ss_name_set == actual, "The names scraped from the SS wiki page are not the same as the names in the test csv file. Maybe wikipedia changed! Update your ss-names.csv file"

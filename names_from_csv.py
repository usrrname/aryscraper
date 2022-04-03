import csv


def get_names_from_csv(file):

    names = []
    with open(file, 'r') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        names = [x for x in data if x != 'Name']
    names.sort()
    return names

import requests
import mimetypes
from pathlib import Path
import re
import csv
from humanize import naturalsize

image_extensions = ['.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.tiff',
                    '.tif', '.TIF', '.bmp', '.gif', '.GIF', '.webp', '.svg', '.SVG']


def get_classes_from_csv(file):
    class_map = {}
    with open(file, 'r') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        for row in data:
            if row[0] != 'Number':
                class_map.update({row[0]: row[1].strip()})
    return class_map


def get_labels_from_csv(file):
    label_map = {}
    with open(file, 'r') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        for row in data:
            if row[0] != 'Number':
                label_map.update({row[1].strip(): row[0]})
    return label_map


def remove_contents_in_brackets(line):
    pattern = r"\([^()]*\)"
    sanitized_string = re.sub(pattern, '', line)
    print(sanitized_string)
    return sanitized_string


def has_extension(file):
    file = str(file)
    img_ext = ('.png', '.PNG',  '.JPG', '.jpeg', '.jpg', '.tiff',
               '.bmp', '.gif', '.GIF', '.webp', '.svg', '.SVG')

    if any(word in file for word in image_extensions) or file.endswith(img_ext):
        return True
    else:
        return False


def get_image_link(image_url):
    url = str(image_url)

    contains_extension = [ext in url for ext in image_extensions]
    for ext in image_extensions:
        if url.endswith(ext):
            return url
        elif any(ext in url for ext in image_extensions):
            truthy_index = contains_extension.index(True)
            position = url.find(image_extensions[truthy_index])
            full_image_link = url[:position +
                                  len(image_extensions[truthy_index])]
            return full_image_link


def get_image_format(image_url):
    response = requests.head(image_url)
    content_type = response.headers['content-type']
    extension = mimetypes.guess_extension(content_type)
    print(extension)
    return extension


def get_folder_size(path, start_size):

    for file_ in Path(path).rglob('**/*'):

        start_size += file_.stat().st_size

    return naturalsize(start_size)


def list_folders(filepath):
    current_folder = Path(filepath)
    folders = [f for f in current_folder.rglob('**/*') if f.is_dir()]
    for folder in folders:
        size = get_folder_size(folder, folder.stat().st_size)
        print("{:<8} {:<15} {:<10}".format(
            folder.parent.name,
            folder.name,
            size
        ))


def get_classifier_and_label(row):
    result = []
    labels_map = get_labels_from_csv('ss-ranks.csv')
    labels = list(labels_map.keys())
    prospective_label = row.text.split(
        '\xa0')[0].replace('\xa0', '')
    prospective_label = ''.join(prospective_label)
    if prospective_label.startswith('\n'):
        prospective_label = prospective_label[1:]
    if prospective_label.endswith('-SS'):
        prospective_label = prospective_label[:-3]
    if prospective_label.startswith('Gerhard Putsch'):
        prospective_label = 'SS-Stabsscharführer'
    if prospective_label == 'Professor Wolfgang Abel':
        prospective_label = 'SS biologist'
    if prospective_label == 'Hermann Paul Maximilian Abendroth':
        prospective_label = 'SS-Kapellmeister'

    if any(string in prospective_label for string in labels):
        try:
            label = prospective_label
            classifier = labels_map.get(prospective_label)
            # print(f'{prospective_label} -> {classifier}')
            result = [classifier, label]
        except TypeError in Exception:
            print(TypeError.args)
            print(TypeError + ': ' +
                  prospective_label + ' not found in labels')
    return result


def write_to_csv(filename, person_list, header):
    with open(filename, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        [writer.writerow(a) for a in person_list]
        f.close()
        return person_list


def write_person_data_to_table(filename, tables):
    with open(filename, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        [writer.writerow(row) for row in tables]
        f.close()


def write_csv_header(filename, header):
    with open(filename, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        f.close()


def is_already_saved(data_row):
   # checks if image info is already saved in csv
    with open('../data-info.csv', "r") as infile:
        reader = csv.reader(infile)
        next(reader)
        for line in reader:
            if [data_row] == line:
                print('Image already in data-info.csv')
                return True
            else:
                return False


def sanitize_names_for_folders(names):
    folder_names = []
    for name in names:
        if name != 'Name':
            folder_name = ''.join(name)
            if len(folder_name.split(' ')) <= 4:
                folder_name = folder_name.strip().replace(' ', '_')
                folder_names.append(folder_name)
            else:
                name_array = folder_name.split(' ')[: 4]
                folder_name = ''.join(name_array).strip().replace(' ', '_')
                folder_names.extend([folder_name])
    return folder_names


def get_names_from_csv(file):
    names = []
    with open(file, 'r') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        data = list(data)
        for row in data:
            if row != [] and row[0] != 'Name':
                extracted_name = remove_contents_in_brackets(
                    row[0].strip())
                extracted_name = extracted_name.replace(
                    '"', '').replace(',', '').replace('.', '')
                if '[]' in extracted_name:
                    extracted_name = extracted_name.replace('[]', '')
                if '/' in extracted_name:
                    extracted_name = extracted_name.replace('/', ' ')
                names.append(extracted_name)
        
    csv_file.close()
    names.sort()
    return names

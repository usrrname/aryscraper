import requests
import mimetypes
from pathlib import Path
import re
import os
import csv
import json
from humanize import naturalsize
import re
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
    return sanitized_string


def has_img_extension(file):
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
        else:
            if ('http' or 'https') in image_url:
                return image_url
            else:
                url = os.path.splitext(image_url)[0]
                return 'https://'.join(url)


def get_image_format(image_url):
    response = requests.head(image_url)
    try:
        content_type = response.headers['content-type']
    except KeyError in Exception:
        print(f'{KeyError, e}')

    extension = mimetypes.guess_extension(content_type)
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
    return folders


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
            print(TypeError + ': {prospective_label} not found')
    return result


def write_to_csv(filename, person_list, header):
    with open(filename, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(header)
        else:
            [writer.writerow(a) for a in person_list]
        f.close()
        return person_list


def last_row_from_csv(filename):
    with open(filename, 'r', encoding='UTF8') as file:
        reader = csv.reader(file, quotechar='"',
                            delimiter=',')
        last_line = list(reader)[-1]
        return last_line
    f.close()


def add_row_to_csv(filename, data_row):
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data_row)
        f.close()


def write_csv_header(filename, header):
    with open(filename, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        f.close()


def is_already_saved(data_row, filename):
   # checks if image info is already saved in csv
    with open(filename, "r") as infile:
        reader = csv.reader(filename, delimiter=',',
                            quotechar='"', escapechar='\\')
        for line in reader:
            for cell in line:
                if line in data_row:
                    print('Image already in data-info.csv')
                    return True
                else:
                    return False


def sanitize_names_for_folders(names):
    folder_names = []
    for name in names:
        if name != 'Name':
            folder_name = ''.join(name)
            folder_name = folder_name.strip().replace(' ', '_')
            folder_names.append(folder_name)
    return folder_names


def get_names_from_csv(file):
    names = []
    # ranks = list(get_labels_from_csv('ss-ranks.csv').values())

    with open(file, 'r') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        data = list(data)
        for row in data:
            if row != [] and row[0] != 'Name':
                # if row != [] and row[0] != 'Name' and row[0] not in ranks:
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


def read_json(filename):
    results = []
    with open(filename, "r") as read_file:
        image_dict = json.load(read_file)
        results = image_dict.get('images_results')
        read_file.close()
    return results


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def save_as_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()


def extract_info(lang, page, key):
    try:
        result = page[key]
    except Exception as e:
        file = open(f'failed_{lang}.txt', 'a')
        file.writelines(f'{subject} {l} {e}' + '\n')
        file.close()
        pass
    return result

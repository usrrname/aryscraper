import requests
import mimetypes
from pathlib import Path
import re
import csv
from humanize import naturalsize

image_extensions = ['.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.tiff',
                    '.bmp', '.gif', '.GIF', '.webp', '.svg', '.SVG']


def get_names_from_csv(file):

    names = []
    with open(file, 'r') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        names = [x for x in data if x != 'Name']
    names.sort()
    return names


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

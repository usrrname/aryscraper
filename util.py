from pathlib import Path
import re
import csv
from humanize import naturalsize

image_extensions = ['.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.tiff',
                    '.bmp', '.gif', '.GIF', '.webp', '.svg', '.SVG', 's3.amazonaws.com']


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
    url = str(image_url)

    contains_extension = [ext in url for ext in image_extensions]
    for ext in image_extensions:
        if url.endswith(ext):
            image_format = url.split('.')[-1]
            return image_format
        elif any(ext in url for ext in image_extensions):
            truthy_index = contains_extension.index(True)
            position = url.find(image_extensions[truthy_index])
            image_format = url[position:position +
                               len(image_extensions[truthy_index])]
            return image_format


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

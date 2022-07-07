import os
import unicodedata
import re


def compare_strs(s1, s2):
    def NFD(s):
        return unicodedata.normalize('NFD', s)

    return NFD(s1) == NFD(s2)


def find_corresponding_folder(person_name, folder_name):
    substr = person_name.strip().replace(' ', '_')
    for root, dirs, subdirs in os.walk(folder_name):
        for folder in dirs:
            folder_without_brackets = re.sub(
                "[\(\[].*?[\)\]]", "", folder).strip()
            if substr in folder or compare_strs(substr, folder_without_brackets):
                return folder


def sanitize_names_for_folders(names):
    folder_names = []
    for name in names:
        if name != 'Name':
            folder_name = ''.join(name)
            folder_name = folder_name.strip().replace(' ', '_')
            folder_names.append(folder_name)
    return folder_names


def get_names_in_folder(folder):
    os.chdir(folder)
    current_folders = os.listdir()
    current_folders.sort()
    names = [name.replace('_', ' ')
             for name in current_folders if name != '.DS_Store']
    return names


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

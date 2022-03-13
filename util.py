import re


def remove_contents_in_brackets(line):
    pattern = r"\([^()]*\)"
    sanitized_string = re.sub(pattern, '', line)
    print(sanitized_string)
    return sanitized_string


def hasExtension(file):
    file = file.lower()
    image_extensions = ['.png', '.jpg', '.jpeg', '.tiff',
                        '.bmp', '.gif', '.webp', '.svg']
    img_ext = ('.png', '.jpg', '.jpeg', '.tiff',
               '.bmp', '.gif', '.webp', '.svg')
    if any(word in file for word in image_extensions) or file.endswith(img_ext):
        return True
    else:
        return False

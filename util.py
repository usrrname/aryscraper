import re


def remove_contents_in_brackets(line):
    pattern = r"\([^()]*\)"
    sanitized_string = re.sub(pattern, '', line)
    print(sanitized_string)
    return sanitized_string


def hasExtension(file):
    file = str(file.lower())
    image_extensions = ['.png', '.jpg', '.jpeg', '.tiff',
                        '.bmp', '.gif', '.webp', '.svg']
    img_ext = ('.png', '.jpg', '.jpeg', '.tiff',
               '.bmp', '.gif', '.webp', '.svg')
    if any(word in file for word in image_extensions) or file.endswith(img_ext):
        return True
    else:
        return False


def get_image_link(image_url):
    url = str(image_url)
    extensions = ['.png', '.jpg', '.jpeg', '.tiff',
                          '.bmp', '.gif', '.webp', '.svg']
    contains_extension = [ext in url for ext in extensions]
    for ext in extensions:
        if url.endswith(ext):
            image_format = url.split('.')[-1]
            return image_format
        elif any(ext in url for ext in extensions):
            truthy_index = contains_extension.index(True)
            position = url.find(extensions[truthy_index])
            full_image_link = url[:position+len(extensions[truthy_index])]
            return full_image_link


def get_image_format(image_url):
    url = str(image_url)
    extensions = ['.png', '.jpg', '.jpeg', '.tiff',
                          '.bmp', '.gif', '.webp', '.svg']
    contains_extension = [ext in url for ext in extensions]
    for ext in extensions:
        if url.endswith(ext):
            image_format = url.split('.')[-1]
            return image_format
        elif any(ext in url for ext in extensions):
            truthy_index = contains_extension.index(True)
            position = url.find(extensions[truthy_index])
            image_format = url[position:position+len(extensions[truthy_index])]
            return image_format

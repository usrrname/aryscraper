import os
import json
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
from numpy import asarray
from PIL import Image
from mtcnn import MTCNN
from names import women, men
from util import read_dict_from_json, get_one_image_file, save_as_json
from wiki import create_name_filename_map
# change image size as needed
required_size = (120, 120)


def extract_face(filename, required_size):
    image = Image.open(filename)
    image = image.convert('RGB')
    pixels = asarray(image)
    detector = MTCNN()
    results = detector.detect_faces(pixels)
    # extract the bounding box from the first face found
    if results != []:
        x1, y1, width, height = results[0]['box']
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        # extract the face
        face = pixels[y1:y2, x1:x2]
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = asarray(image)
        return face_array


def plot_gallery(folders, titles, rows, cols, filename):
    """Plot a gallery of portraits"""

    mpl.rcParams['font.size'] = 10
    mpl.rcParams['figure.figsize'] = (1.8 * cols, 2.4 * rows)
 # specify folder to plot
    folders = os.listdir()
    i = 1

    for folder in folders:
        name = folder.replace('_', ' ')

        if name in titles:
            os.chdir(folder)
            files = os.listdir(os.getcwd())
            path = [file for file in files if file != '.DS_Store'][0]

            try:
                face = extract_face(path, required_size)
                # print(i, face.shape)
            except Exception as err:
                print(name, err)
                pass
            plt.subplot(rows, cols, i, frameon=False, xticks=[], yticks=[])
            plt.xlabel(name.upper(), labelpad=5)
            plt.tight_layout()

            try:
                plt.imshow(face, cmap=plt.cm.gray)
            except Exception as err:
                print(name, err)
                pass
            finally:
                os.chdir('..')
                i += 1
    plt.show()

    # TODO: add save function


def save_img(filename, face):
    plt.imsave(filename, face)


def extract_img(imgpath, folder):
    for index, person in peopledict.items():
        if person['wikiquery'] == folder:
            face = extract_face(imgpath, required_size)
            try:
                filename = os.path.join(
                    save_dir, person['name'].replace(' ', '_') + '_mtcnn.jpg')
                save_img(filename, face)
                person.update({'faceExtraction': filename})
                peopledict.update({index: person})
            except Exception as err:
                print(err)
                pass
            finally:
                save_as_json(save_dir + '/' +
                             'einsatz1941_extracted.json', peopledict)


if __name__ == '__main__':

    target_folder = 'men'
    save_dir = 'men_extracted'

    # create name-filename map
    folder_map = create_name_filename_map('./men')
    peopledict = read_dict_from_json('men.json')

    # if output directory doesn't exist, creates it
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    for key, person in peopledict.items():

        filename = person['filename'].split('/')[0] + '_extracted'
        extension = os.path.splitext(person['filename'])[1]
        extracted_face_filename = save_dir + '/' + filename + extension
        face = extract_face(target_folder+'/' +
                            person['filename'], required_size)
        save_img(extracted_face_filename, face)

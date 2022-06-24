# example of loading the keras facenet model
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
from numpy import asarray
from PIL import Image
import os
from mtcnn import MTCNN
from names import women, einsatzgruppen, men

required_size = (224, 224)


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


if __name__ == '__main__':
    folder = ''
    current_path = os.getcwd()
    if not current_path.endswith(folder):
        os.chdir(folder)
    plot_gallery(folder, names, 9, 9, '')

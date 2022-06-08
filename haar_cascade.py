# Haar cascade face extraction
import os
import cv2
from glob import glob
from google.colab.patches import cv2_imshow


imgdir = './'
save_dir = 'extracted'
ext = ['svg', 'tiff', 'png', 'jpg', 'gif', 'webp', 'jpeg']  # Image formats


def find_images_in_dir(imgdir):
    files = []
    [files.extend(glob(imgdir + '*.' + e)) for e in ext]
    return files


files = find_images_in_dir(imgdir)
filenames = [os.path.splitext(filepath) for filepath in files]

images = [cv2.imread(file) for file in files]


def get_filename(image_index, count):
    (name, extension) = filenames[image_index]
    filename = f'{save_dir}/{name}-{count}{extension}'
    return filename


def haar_cascade_extraction(images):
    os.mkdir(save_dir)
    for index, image in enumerate(images):
        grayscaled_img = cv2.cvtColor(
            image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        face_cascade = cv2.CascadeClassifier(
            'haarcascade_frontalface_alt2.xml')
        faces = face_cascade.detectMultiScale(grayscaled_img, 1.1, 4)

        for count, (x, y, w, h) in enumerate(faces):
            # Draw rectangle around face
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 255))
            face = image[y:y + h, x:x + w]
            resized = cv2.resize(face, (120, 120))
            # Counts up if there is more than one face in image
            filename = get_filename(index, count)
            print(f'Cropping and Saving: {filename}')
            cv2_imshow(resized)
            cv2.imwrite(filename, resized)
            cv2.waitKey(1)
            cv2.destroyAllWindows()

# for testing
# haar_cascade_extraction(images)

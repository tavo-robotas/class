import cv2
import os

dir_path = os.path.join(os.getcwd(), 'data/acme/')

for filename in os.listdir(dir_path):
    # If the images are not .JPG images, change the line below to match the image type.
    if filename.endswith(".JPG"):
        image = cv2.imread('data/acme/' + filename)
        resize = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imwrite(filename, resize)

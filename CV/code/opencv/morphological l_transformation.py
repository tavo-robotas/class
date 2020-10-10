import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

source = cv.imread('data/smarties.png', cv.IMREAD_GRAYSCALE)
# source = cv.cvtColor(source, cv.COLOR_BGR2RGB)

_, mask = cv.threshold(source, 220, 255, cv.THRESH_BINARY_INV)

kernel   = np.ones((2, 2), np.uint8)
dilate   = cv.dilate(mask, kernel, iterations=2)
erode    = cv.erode(mask, kernel, iterations=2)
open     = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
close    = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
gradient = cv.morphologyEx(mask, cv.MORPH_GRADIENT, kernel)
tophat   = cv.morphologyEx(mask, cv.MORPH_TOPHAT, kernel)

titles = ['source', 'mask', 'dilate', 'erode', 'open', 'close', 'gradient', 'tophat']
images = [source, mask, dilate, erode, open, close, gradient, tophat]

for i in range(len(images)):
    plt.subplot(2 , 4, i+1)
    plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])

plt.show()
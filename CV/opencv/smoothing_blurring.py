import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

image = cv.imread('data/me.jpg')
source = cv.cvtColor(image, cv.COLOR_BGR2RGB)

# there are few available blurring filters on opencv
# homogeneous, gaussian, median, bilateral, etc.

# homogeneous is simplest
kernel = np.ones((5, 5), np.float32)/25

destination = cv.filter2D(source, -1, kernel)
blurred     = cv.blur(source, (5, 5))
gaussian    = cv.GaussianBlur(source, (5, 5), 0)
median      = cv.medianBlur(source, 5)
bilateral   = cv.bilateralFilter(source, 9, 75, 75)

titles = ['image', '2D convolution', 'blur', 'gaussian', 'median', 'bilateral']
images = [source, destination, blurred, gaussian, median, bilateral]

for i in range(len(images)):
    plt.subplot(2, 3, i+1)
    plt.title(titles[i])
    plt.imshow(images[i], 'gray')
    plt.xticks([]), plt.yticks([])

plt.show()

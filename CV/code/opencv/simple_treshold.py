import cv2 as cv
from matplotlib import pyplot as plt

image = cv.imread('data/gradientas.jpg',0)

# Simple threshold
# the result of tresholding are IRT and second a tresholded value of image
_, thr1 = cv.threshold(image, 127, 255, cv.THRESH_BINARY)
_, thr2 = cv.threshold(image, 200, 255, cv.THRESH_BINARY_INV)
_, thr3 = cv.threshold(image, 100, 255, cv.THRESH_TRUNC)
_, thr4 = cv.threshold(image, 100, 255, cv.THRESH_TOZERO)
_, thr5 = cv.threshold(image, 100, 255, cv.THRESH_TOZERO_INV)

pavadinimai = ['vaizdas', 'bin', 'bin_inv', 'trunc', '2zero', '2zero_inv']
images = [image, thr1, thr2, thr3, thr4, thr5]

for i in range(len(images)):
    plt.subplot(2, 3, i+1)
    plt.imshow(images[i], 'gray')
    plt.title(pavadinimai[i])
    plt.xticks([]), plt.yticks([])

# cv.imshow('vaizdas', image)
# cv.imshow('threshold_1', thr1)
# cv.imshow('threshold_2', thr2)
# cv.imshow('threshold_3', thr3)
# cv.imshow('threshold_4', thr4)
# cv.imshow('threshold_5', thr5)

# cv.waitKey(0)
# cv.destroyAllWindows()

plt.show()
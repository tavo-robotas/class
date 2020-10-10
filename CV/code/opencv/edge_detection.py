import cv2 as cv
from matplotlib import pyplot as plt
import  numpy as np

def call(x):
    pass

source = cv.imread('data/me.jpg', 0)



thr1 = cv.getTrackbarPos('thr1', 'langas')
thr2 = cv.getTrackbarPos('thr2', 'langas')


# Canny edge detection algorithm is composed of 5 steps:
#   1.Noise reduction
#   2.Gradient calculation
#   3.Non-maximum suppression
#   4.Double threshold
#   5.Edge tracking by Hysteresis
# Opencv  has in-built functions to do that
canny = cv.Canny(source, 100, 200)

titles = ['original', 'canny']
images = [source, canny]

cv.namedWindow('langas')
cv.createTrackbar('thr1', 'langas', 0, 100, call)
cv.createTrackbar('thr2', 'langas', 0, 200, call)

for i in range(len(images)):
    plt.subplot(1, 2, i+1)
    plt.title(titles[i])
    plt.imshow(images[i], 'gray')
    plt.xticks([]), plt.yticks([])

plt.show()
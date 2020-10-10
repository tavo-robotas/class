import cv2 as cv
import numpy as np

image = cv.imread('data/contours.jpg', -1)
convert = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(convert, 127, 255, 0)


contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
# print(str(len(contours)))
# print(contours[0])

cv.drawContours(image, contours, 1, (0, 255, 255), 5)

# print(contours[0])

cv.imshow('contrast', thresh)
cv.imshow('vaizdas', image)
cv.waitKey(0)
cv.destroyAllWindows()
import cv2 as cv
from matplotlib import pyplot as plt

image = cv.imread('data/sudoku.jpg', 0)

_, th1 = cv.threshold(image, 125, 255, cv.THRESH_BINARY)

th2 = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)
th3 = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

# cv.imshow('vaizdas', image)
# cv.imshow('th1', th1)
# cv.imshow('th2', th2)
# cv.imshow('th3', th3)



cv.waitKey(0)
cv.destroyAllWindows()
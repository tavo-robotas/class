import numpy as np
import cv2 as cv

source = cv.imread('data/shapes.jpg')
gray = cv.cvtColor(source, cv.COLOR_BGR2GRAY)

ret, thresh = cv.threshold(gray, 200, 255, 0)

contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# specific = contours[0]

# cv.drawContours(source, [specific], 0, (0, 255, 255), 3)

# print(len(contours[0]))

for i, contour in enumerate(contours):

    mask = np.zeros(gray.shape, np.uint8)
    cv.drawContours(mask, [contour], 0, 255, -1)
    mean = cv.mean(source, mask=mask)
    cv.imshow('langas', mask)
   
    cv.waitKey(0)
    cv.destroyAllWindows()


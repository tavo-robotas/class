import cv2 as cv
import numpy as np


img = cv.imread('data/pixels_II.jpg', 0)


np.savetxt('test.txt', img, delimiter=',', fmt='%d')

cv.imshow('pixel', img)
cv.waitKey(0)
cv.destroyAllWindows()
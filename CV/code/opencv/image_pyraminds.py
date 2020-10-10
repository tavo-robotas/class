import cv2 as cv
import numpy as np

image = cv.imread('data/me.jpg')

layer_1 = image.copy()
# There two types of images pyramids that are available
# 1. Gaussian pyramid
# 2. Laplacian pyramid that is created from gaussian pyramid

#low_res_1 = cv.pyrDown(image)
#low_res_2 = cv.pyrDown(low_res_1)
#hig_res_1 = cv.pyrUp(low_res_2)

# Lets create a gaussian pyramid array

gp = [layer_1]
iter = 6
for i in range(iter):
    layer_1 = cv.pyrDown(layer_1)
    gp.append(layer_1)
    # cv.imshow(str(i), layer_1)

#cv.imshow('uper_gauss_pyramid', last)

for i in range(5, 0, -1):
    gaussian_expanded = cv.pyrUp(gp[i])
    laplacian = cv.subtract(gp[i-1], gaussian_expanded)
    cv.imshow(str(i), laplacian)


#cv.imshow('langas', image)
#cv.imshow('pyrdown_1', low_res_1)
#cv.imshow('pyrdown_2', low_res_2)
#cv.imshow('pyrup_1', hig_res_1)



cv.waitKey(0)
cv.destroyAllWindows()
import  numpy as np
import cv2

TR_logo = cv2.imread('data/tavorobotas.png')
CV_logo = cv2.imread('data/opencv.png')
# returns a tuples of rows, columns, channels
print(TR_logo.shape)
# returns total number of pixel is accessed
print(TR_logo.size)
# returns image obtained datatype
print(TR_logo.dtype)

# tuple unpacking
b, g, r = cv2.split(TR_logo)
TR_logo = cv2.merge((b, g, r))


# neveikia
# interest = image[100:50, 250:100]
# image[200:50, 250:100] = interest

TR_logo = cv2.resize(TR_logo, (600, 739))
CV_logo = cv2.resize(CV_logo, (600, 739))

destination = cv2.add(TR_logo, CV_logo)

weighted = cv2.addWeighted(TR_logo, 0.9 , CV_logo, 0.1, 0)


cv2.imshow('vaizdas', weighted)
cv2.waitKey(0)
cv2.destroyAllWindows()
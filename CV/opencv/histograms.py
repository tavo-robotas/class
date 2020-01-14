import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

image = np.zeros((200,200), np.uint8)

cv.imshow('vaizdas', image)
cv.waitKey(0)
cv.destroyAllWindows()
import cv2 as cv
from matplotlib import pyplot as plt


image_1 = cv.imread('data/me.jpg', -1)

cv.imshow('vaizdas', image_1)

image_2 = cv.cvtColor(image_1, cv.COLOR_BGR2RGB)

plt.xticks([]), plt.yticks([])
plt.imshow(image_2)
plt.show()


cv.waitKey(0)
cv.destroyAllWindows()
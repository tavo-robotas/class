import cv2 as cv
import numpy as np

image    = cv.imread('data/me.jpg')
template = cv.imread('data/face.jpg', 0)
grey = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

w, h = template.shape[::-1]

print(w, h)
res = cv.matchTemplate(grey, template, cv.TM_CCOEFF_NORMED)
# print(res)
locate = np.where(res >= 0.99)
print(locate)

for point in zip(*locate[::-1]):
    cv.rectangle(image, point, (point[0] + w, point[1] + h), (0, 0, 255), 2)

cv.imshow('vaizdas', image)
cv.waitKey(0)
cv.destroyAllWindows()
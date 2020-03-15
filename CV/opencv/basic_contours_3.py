import numpy as np
import cv2 as cv

source = cv.imread('data/rotated.jpg')
gray = cv.cvtColor(source, cv.COLOR_BGR2GRAY)

ret, thresh = cv.threshold(gray, 200, 255, 0)

contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
specific = contours[0]
moments = cv.moments(specific)
# cv.drawContours(source, [specific], 0, (0, 255, 255), 3)

perimeter = cv.arcLength(specific, True)

rectangle = cv.minAreaRect(specific)
box = cv.boxPoints(rectangle)
box = np.int0(box)

(x, y), (w, h), a = rectangle

cX = int(moments["m10"] / moments["m00"])
cY = int(moments["m01"] / moments["m00"])


print(f'x is {x}, y is {y}, angle is {a}')


cv.drawContours(source, [box], 0, (0, 0, 255), 2)

# cv.circle(source, (x, y), 1, (255, 255, 0), 3)

# cv.rectangle(source, (x, y), (x+w, y+h), (255, 0, 255), 2)

# print(len(contours[0]))

cv.imshow('langas', source)
cv.waitKey(0)
cv.destroyAllWindows()


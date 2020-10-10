import cv2 as cv
import numpy as np

image = cv.imread('data/shapes.jpg')
grey  = cv.cvtColor(image, cv.COLOR_BGR2GRAY)


_, thresh = cv.threshold(grey, 200, 255, cv.THRESH_BINARY)

contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

def name(i):
    switch = {
        3: 'trys',
        4: 'keturi',
        5: 'penki',
        6: 'šeši',
        7: 'septyni'
    }
    return switch.get(i, 'apskritimas')



for contour in contours:
    approx = cv.approxPolyDP(contour, 0.01*cv.arcLength(contour, True), True)
    cv.drawContours(image, [approx], 0, (255, 0, 255), 1)
    x = approx.ravel()[0]
    y = approx.ravel()[1]

    cv.putText(image, name(len(approx)), (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

cv.imshow('vaizdas', image)
cv.waitKey(0)
cv.destroyAllWindows()


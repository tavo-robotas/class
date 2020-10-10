import numpy as np
import cv2

def callback(x):
    print(x)

cv2.namedWindow('langas')

switch = 'color\greyscale'

cv2.createTrackbar('POS', 'langas', 0, 255, callback)
cv2.createTrackbar(switch, 'langas', 0, 1, callback)

font = cv2.FONT_HERSHEY_COMPLEX

while 1:
    image = cv2.imread('data/me.jpg')
    pos = cv2.getTrackbarPos('POS', 'langas')
    cv2.putText(image, str(pos), (100, 200), font, 4, (255, 255, 255))
    k = cv2.waitKey(1)
    if k == 27:
        break

    s = cv2.getTrackbarPos(switch, 'langas')

    if s == 0:
        pass
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imshow('langas', image)

cv2.destroyAllWindows()
import numpy as np
import cv2

def callback(x):
    print(x)


image = np.zeros((300, 512, 3), np.uint8)

cv2.namedWindow('langas')
cv2.createTrackbar('B', 'langas', 0, 255, callback)
cv2.createTrackbar('G', 'langas', 0, 255, callback)
cv2.createTrackbar('E', 'langas', 0, 255, callback)

switch = '0 : OFF\n 1: ON'
cv2.createTrackbar(switch, 'langas', 0, 1, callback)

while 1:
    cv2.imshow('langas', image)
    k = cv2.waitKey(1)
    if k == 27:
        break

    b = cv2.getTrackbarPos('B', 'langas')
    g = cv2.getTrackbarPos('G', 'langas')
    r = cv2.getTrackbarPos('R', 'langas')
    s = cv2.getTrackbarPos(switch, 'langas')

    if s == 0:
        image[:] = 0
    else:
        image[:] = [b, g, r]

cv2.destroyAllWindows()
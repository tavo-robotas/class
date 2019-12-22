import cv2
import numpy as np
import imutils
import time

from collections import deque

def call(x):
    pass


cv2.namedWindow('detection')
cv2.createTrackbar('LH', 'detection', 0, 255, call)
cv2.createTrackbar('LS', 'detection', 0, 255, call)
cv2.createTrackbar('LV', 'detection', 0, 255, call)
cv2.createTrackbar('UH', 'detection', 255, 255, call)
cv2.createTrackbar('US', 'detection', 255, 255, call)
cv2.createTrackbar('UV', 'detection', 255, 255, call)
# image = cv2.imread('data/balls.jpg')
capture = cv2.VideoCapture(0)
while capture.isOpened():
    _, image = capture.read()
    if _:

        blurred = cv2.GaussianBlur(image, (13, 13), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        l_h = cv2.getTrackbarPos('LH', 'detection')
        l_s = cv2.getTrackbarPos('LS', 'detection')
        l_v = cv2.getTrackbarPos('LV', 'detection')
        u_h = cv2.getTrackbarPos('UH', 'detection')
        u_s = cv2.getTrackbarPos('US', 'detection')
        u_v = cv2.getTrackbarPos('UV', 'detection')

        lower_bound = np.array([l_h, l_s, l_v])
        upper_bound = np.array([u_h, u_s, u_v])

        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        # cv erode documentation
        mask = cv2.erode(mask, None, iterations=2)
        # cv dilate documentation
        mask = cv2.dilate(mask, None, iterations=2)

        result = cv2.bitwise_and(image, image, mask=mask)

        outlines = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(outlines)
        if len(contours) > 0:
            #print(contours)
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int( M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            if radius > 10:

                cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(image, center, 5, (255, 255, 255), -1)
                coordinates = str(int(x)) + ' : ' + str(int(y))
                image = cv2.putText(
                    image,
                    coordinates,
                    (30, 40),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA)
            #cv2.drawContours(image, contours, -1, (0, 255, 255), 3)


        cv2.imshow('image', image)
        cv2.imshow('mask', mask)
        cv2.imshow('rest', result)

        key = cv2.waitKey(1)
        if key == 27:
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()

import cv2 as cv
import numpy as np
import os
source = 1
cap = cv.VideoCapture(source)

mtx = None
r_m = None
t_m = None


def call(x):
    pass


cv.namedWindow('sense', cv.WINDOW_AUTOSIZE)
cv.createTrackbar('LH', 'sense', 0, 255, call)
cv.createTrackbar('LS', 'sense', 0, 255, call)
cv.createTrackbar('LV', 'sense', 0, 255, call)
cv.createTrackbar('UH', 'sense', 255, 255, call)
cv.createTrackbar('US', 'sense', 255, 255, call)
cv.createTrackbar('UV', 'sense', 255, 255, call)

with np.load(os.getcwd() + '/data.npz') as file:
    _, mtx, dist, r_m, t_m = [file[i] for i in ('ret', 'mtx', 'dist', 'rotation', 'translation')]
    print(f"Intrinsic matrix:{mtx}")
    print(f"distortion coeff:{dist}")

def undistort(img, mtx, dist, w, h):
    h, w = img.shape[:2]
    nmtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, nmtx, (w, h), 5)
    dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    return dst

while cap.isOpened():
    ret, frame = cap.read()
    h, w = frame.shape[:2]
    undistorted = undistort(frame, mtx, dist, w, h)
    if ret:
        blurred = cv.GaussianBlur(undistorted, (13, 13), 0)
        hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

        l_h = cv.getTrackbarPos('LH', 'sense')
        l_s = cv.getTrackbarPos('LS', 'sense')
        l_v = cv.getTrackbarPos('LV', 'sense')
        u_h = cv.getTrackbarPos('UH', 'sense')
        u_s = cv.getTrackbarPos('US', 'sense')
        u_v = cv.getTrackbarPos('UV', 'sense')

        lower_bound = np.array([l_h, l_s, l_v])
        upper_bound = np.array([u_h, u_s, u_v])

        mask = cv.inRange(hsv, lower_bound, upper_bound)
        # cv erode documentation
        mask = cv.erode(mask, None, iterations=2)
        # cv dilate documentation
        mask = cv.dilate(mask, None, iterations=2)

        result = cv.bitwise_and(undistorted, undistorted, mask=mask)

        # contours, hierarchy = cv.findContours(result, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # specific = contours[0]
        # moments = cv.moments(specific)
        # cv.drawContours(source, [specific], 0, (0, 255, 255), 3)
        #
        # perimeter = cv.arcLength(specific, True)
        #
        # rectangle = cv.minAreaRect(specific)
        # box = cv.boxPoints(rectangle)
        # box = np.int0(box)
        #
        # (x, y), (w, h), a = rectangle

        # cX = int(moments["m10"] / moments["m00"])
        # cY = int(moments["m01"] / moments["m00"])
        #
        #cv.drawContours(frame, [box], 0, (0, 0, 255), 2)
        #print(f'x is {x}, y is {y}, angle is {a}')
        cv.imshow('undistorted', result)
        key = cv.waitKey(1)
        if key == 27:
            break
    else:
        break
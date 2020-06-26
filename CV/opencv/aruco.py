import numpy as np
import cv2 as cv
import PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import os

def callback(x):
    pass


path = os.path.join(os.getcwd(), 'camera_calibration/data/test/edited/')

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
cv.namedWindow('thresh')
cv.createTrackbar('L', 'thresh', 0, 255, callback)
cv.createTrackbar('U', 'thresh', 0, 255, callback)
def generate():
    fig = plt.figure()
    nx = 4
    ny = 3
    for i in range(1, nx * ny + 1):
        ax = fig.add_subplot(ny, nx, i)
        img = aruco.drawMarker(aruco_dict, i, 700)
        plt.imshow(img, cmap=mpl.cm.gray, interpolation="nearest")
        ax.axis("off")

    plt.savefig("data/markers.png")
    plt.show()

source = 0
capture = cv.VideoCapture(source)
with np.load(path + 'output/data.npz') as file:
    mtx, dist, r_m, t_m = [file[i] for i in ('mtx', 'dist', 'rotation', 'translation')]

while capture.isOpened():
    L = cv.getTrackbarPos('L', 'thresh')
    U = cv.getTrackbarPos('U', 'thresh')

    retain, frame = capture.read()
    if retain:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(gray, L, U, cv.THRESH_BINARY)

        parameters = aruco.DetectorParameters_create()
        corners, ids, rejected = aruco.detectMarkers(thresh, aruco_dict, parameters=parameters)

        if len(corners) > 0:
            cv.aruco.drawDetectedMarkers(frame, corners, ids)
            if ids is not None:
                rvecs, tvecs, _ = cv.aruco.estimatePoseSingleMarkers(corners, 0.1, mtx, dist, r_m, t_m)
                for i in range(len(ids)):
                    cv.aruco.drawAxis(frame, mtx, dist, rvecs[i], tvecs[i], 0.1)

        cv.imshow('frame', frame)
        cv.imshow('thresh', thresh)
        key = cv.waitKey(1)
        if key == 27 or 0xFF == ord('q'):
            break


capture.release()
cv.destroyAllWindows()
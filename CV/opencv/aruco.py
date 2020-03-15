import numpy as np
import cv2 as cv
import PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)


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


while capture.isOpened():
    retain, frame = capture.read()
    if retain:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        parameters = aruco.DetectorParameters_create()
        corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if len(corners) > 0:
            cv.aruco.drawDetectedMarkers(frame, corners, ids)
            # Display the resulting frame
        cv.imshow('frame', frame)
        key = cv.waitKey(1)
        if key == 27 or 0xFF == ord('q'):
            break


capture.release()
cv.destroyAllWindows()
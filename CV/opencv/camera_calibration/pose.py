import cv2 as cv
import numpy as np
import os

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d, Axes3D
from pytransform3d.rotations import *
from pytransform3d.transformations import *
from itertools import product, combinations


path = os.path.join(os.getcwd(), 'data/test/edited/')
v_source = 0

capture = cv.VideoCapture(v_source)

with np.load(os.getcwd() + '/output/data.npz') as file:
    _, mtx, dist, r_m, t_m = [file[i] for i in ('ret', 'mtx', 'dist', 'rotation', 'translation')]
board = (7, 7)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
obj = np.zeros((7*7, 3), np.float32)
obj[:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)

axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)


def unit(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv.line(img, corner, tuple(imgpts[0].ravel()), (255, 0, 0), 5)
    img = cv.line(img, corner, tuple(imgpts[1].ravel()), (0, 255, 0), 5)
    img = cv.line(img, corner, tuple(imgpts[2].ravel()), (0, 0, 255), 5)
    return img


def cube(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1, 2)

    # draw ground floor in green
    img = cv.drawContours(img, [imgpts[:4]], -1, (0, 255, 0), -3)

    # draw pillars in blue color
    for i, j in zip(range(4), range(4, 8)):
        img = cv.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (255, 0, 0), 3)

    # draw top layer in red color
    img = cv.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)

    return img


def plot():
    l_l = -2
    h_l = 2
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_aspect("auto")
    ax.set_autoscale_on(True)
    plt.setp(
        ax,
        xlim=(l_l, h_l),
        ylim=(l_l, h_l),
        zlim=(l_l, h_l),
        xlabel="X",
        ylabel="Y",
        zlabel="Z"
    )
    plt.tick_params(axis='both', labelsize=10, )

    ax.set_xticks(ax.get_xticks()[::2])
    ax.set_yticks(ax.get_yticks()[::2])
    ax.set_zticks(ax.get_zticks()[::2])

    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    ax.zaxis.set_ticklabels([])
    plt.ion()
    plt.pause(0.05)
    plt.show()

while capture.isOpened():
    retain, img = capture.read()

    if retain:
       
# for name in os.listdir(path):
#     if name.endswith('.jpg'):
        #img = cv.imread(path + name)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, board, None)

        if ret == True:
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

            # Find the rotation and translation vectors.
            _, rvecs, tvecs, inliers = cv.solvePnPRansac(obj, corners2, mtx, dist)

            # project 3D points to image plane
            points, jac = cv.projectPoints(axis, rvecs, tvecs, mtx, dist, obj)

            img = unit(img, corners2, points)


            cv.imshow('testas', img)


        cv.imshow('testas', img)

        key = cv.waitKey(1)
        if key == 27:
            break

        # if cv2.waitKey(1) and 0xFF == ord('q'):
        #     break
    else:
        break

capture.release()
cv.destroyAllWindows()


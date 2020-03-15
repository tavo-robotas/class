import cv2 as cv
import numpy as np
import glob
import os



path = os.path.join(os.getcwd(), 'data/test/edited/')

v_source = 0
















































import










































































capture = cv.VideoCapture(v_source)



with np.load(path + 'output/data.npz') as file:
    mtx, dist, r_m, t_m = [file[i] for i in ('mtx', 'dist', 'rotation', 'translation')]
board = (7, 7)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
obj = np.zeros((7*7, 3), np.float32)
obj[:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)

axis = np.float32([
    [0, 0, 0],
    [0, 3, 0],
    [3, 3, 0],
    [3, 0, 0],
    [0, 0, -3],
    [0, 3, -3],
    [3, 3, -3],
    [3, 0, -3]])


def draw(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1, 2)

    # draw ground floor in green
    img = cv.drawContours(img, [imgpts[:4]], -1, (0, 255, 0), -3)

    # draw pillars in blue color
    for i, j in zip(range(4), range(4, 8)):
        img = cv.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (255, 255, 255), 3)

    # draw top layer in red color
    img = cv.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)

    return img


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
            _, rot, tra, lie = cv.solvePnPRansac(obj, corners2, mtx, dist)

            # project 3D points to image plane
            points, jac = cv.projectPoints(axis, rot, tra, mtx, dist)

            img = draw(img, corners2, points)
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


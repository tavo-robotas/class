import numpy as np
import cv2 as cv
import os
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
board = (7, 7)
mean_error = 0
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
obj_points = []  # 3d point in real world space
img_points = []  # 2d points in image plane.


path = os.path.join(os.getcwd(), 'data/test/edited')
#source = 0
#capture = cv.VideoCapture(source)
h, w = cv.imread('data/test/edited/f01.jpg', 0).shape[:2]
# while capture.isOpened():
#     retain, frame = capture.read()
for name in os.listdir(path):
    if name.endswith('.jpg'):
        print(name)
    # if retain:
        img = cv.imread('data/test/edited/' + name)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        #h, w = gray.shape[:2]
        # if retain:
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, board, None)

        # If found, add object points, image points (after refining them)
        if ret:
            obj_points.append(objp)

            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            img_points.append(corners2)

                # Draw and display the corners
            img = cv.drawChessboardCorners(img, board, corners2, ret)

            cv.imshow('img', img)
            cv.waitKey(50)

#         cv.imshow('testas', frame)
#         key = cv.waitKey(1)
#         if key == 27:
#             break
#
#             # if cv2.waitKey(1) and 0xFF == ord('q'):
#             #     break
#     else:
#         break
#
# capture.release()
# cv.destroyAllWindows()


ret, mtx, dist, rotation, translation = cv.calibrateCamera(obj_points, img_points, (w, h), None, None)
img = cv.imread('data/test/edited/f01.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
matrix, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
distortion = cv.undistort(img, mtx, dist, None, matrix)

x, y, w, h = roi
distortion = distortion[y:y+h, x:x+w]
cv.imwrite(path + '/output/result.jpg', distortion)

np.savez(path + '/output/data.npz', ret=ret, mtx=mtx, dist=dist, rotation=rotation, translation=translation)

for i in range(len(obj_points)):
    points, _ = cv.projectPoints(obj_points[i], rotation[i], translation[i], mtx, dist)
    error = cv.norm(img_points[i], points, cv.NORM_L2)/len(points)
    mean_error += error

print(f"total error: {mean_error/len(obj_points)}")

#ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objp, img_points, gray.shape[::-1], None, None)
# print("Camera matrix : \n")
# print(mtx)
# print("dist : \n")
# print(dist)
# print("rvecs : \n")
# print(rotation)
# print("tvecs : \n")
# print(translation)

'''
camera calibration for distorted images with calibration board samples
reads distorted images, calculates the calibration and write undistorted images
usage:
    calibrate.py [--debug <output path>] [--square_size] [<image mask>]
default values:
    --square_size: 1.0
    <image mask> defaults to ../data/left*.jpg
'''

import numpy as np
import cv2 as cv
import os
import argparse
import time
import threading
from queue import Queue

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--square",  type=float, default=2.3)
    ap.add_argument("-t", "--thread",  type=int,)
    ap.add_argument("-b", "--board",   type=tuple, default=(7, 7))
    ap.add_argument("-o", "--source",  type=str)
    ap.add_argument("-f", "--nframes", type=int, default=40)
    ap.add_argument("-v", "--video",   type=str)
    ap.add_argument("-d", "--delay",   type=int, default=10)
    ap.add_argument("-p", "--pattern", type=int, default=0)
    args = vars(ap.parse_args())

    square_size = float(args.get('square'))
    board = tuple(args.get('board'))
    file = args.get('video')
    nframes = args.get('nframes')
    states = {0: 'DETECTION', 1: 'CAPTURE', 2: 'CALIBRATED'}
    patterns = {0: 'CHESS', 1: 'CIRCLE', 2: 'A_CIRCLE'}
    template = patterns.get(args.get('pattern'))
    mode = states.get(0) # default DETECTION
    previous = 0
    delay = args.get('delay')
    undistort = False

    workingdir="/home/pi/Desktop/Captures/"
    savedir="camera_data/"

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((7*7, 3), np.float32)
    objp[:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)
    objp *= square_size

    # Arrays to store object points and image points from all the images.
    obj_points = []  # 3d point, the physical position of the corners in real world 3D space
    img_points = []  # 2d points in image plane.


    path = os.path.join(os.getcwd(), 'data/test/edited')
    undistort = False
    camera = 1


    def process(fn):
        print(f'processing {fn}')
        pass

    def undistort(img, mtx, dist, w, h):
        nmtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, nmtx, (w, h), 5)
        dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
        return dst

    def project():
        pass

    def save_params(ret, mtx, dist, rotation, translation):
        # h, w = cv.imread('data/test/edited/f01.jpg', 0).shape[:2]
        # cv.imwrite(path + '/output/result.jpg', distortion)
        np.savez(os.getcwd() + '/output/data.npz', ret=ret, mtx=mtx, dist=dist, rotation=rotation, translation=translation)
        print(f'calibration data saved to: {os.getcwd() + "/output/"}')

    def error(obj_points, rotation, translation, mtx, dist):
        total = 0
        status = cv.checkRange(mtx) and cv.checkRange(dist)
        if status:
            for i in range(len(obj_points)):
                points, _ = cv.projectPoints(obj_points[i], rotation[i], translation[i], mtx, dist)
                error = cv.norm(img_points[i], points, cv.NORM_L2)/len(points)
                total += error
            print(f'average error {total/len(obj_points)}')
            if total/len(obj_points) > 0.15:
                return False, status
            else:
                return total/len(obj_points), status
        else:
            print('camera matrix or dist coefficients has anomalies')
            return False, False

    def calibrate(w, h):
        print("--Starting calibration--")
        ret, mtx, dist, rotation, translation = cv.calibrateCamera(obj_points, img_points, (w, h), None, None)
        reprojection, ok = error(obj_points, rotation, translation, mtx, dist)
        print("--Calibration succeeded--" if reprojection else "--Calibration failed--\n")
        print("Camera matrix : \n")
        print(mtx)
        print("dist : \n")
        print(dist)
        print("rvecs : \n")
        print(rotation)
        print("tvecs : \n")
        print(translation)
        if reprojection:
            save_params(ret, mtx, dist, rotation, translation)
            return ret, mtx, dist, rotation, translation



    def get_pattern(i, view, size):
        switcher = {
            'CHESS'   : cv.findChessboardCorners(view, size, cv.CALIB_CB_ADAPTIVE_THRESH, cv.CALIB_CB_NORMALIZE_IMAGE),
            'CIRCLE'  : cv.findCirclesGrid(view, size, None),
            'A_CIRCLE': cv.findCirclesGrid(view, size, None, cv.CALIB_CB_ASYMMETRIC_GRID),
        }
        return switcher.get(i, False)

    def save(frame, time_string):
        cv.imwrite(os.getcwd() + "/output/samples/" + time_string, frame)

    def capture(mode, previous):
        blink = False
        capture = cv.VideoCapture(camera)
        while capture.isOpened():
            retain, frame = capture.read()
            h, w = frame.shape[:2]
            #print(f"image width: {w}, height: {h}")
            if retain:
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                found, corners = get_pattern(template, gray, board)

                # If found, add object points, image points (after refining them)
                if found:
                    # termination criteria
                    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                    if template == 'CHESS':
                        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                    # Draw and display the corners
                    img = cv.drawChessboardCorners(frame, board, corners2, found)
                    key = cv.waitKey(1)
                    if blink:
                        pass
                        #draw counter

                    if capture.isOpened() and time.process_time() - previous > delay:
                        previous = time.process_time()
                        obj_points.append(objp)
                        img_points.append(corners)
                        blink = capture.isOpened()

                        now = time.localtime()  # get struct_time
                        time_string = time.strftime("%Y/%m/%d_%H:%M:%S", now) + '.jpg'
                        save(frame, time_string)
                        print(f"--capturing example {len(img_points)}--")
                        if len(img_points) > nframes:
                            mode = states.get(1)
                            capture.release()

                if mode is "CALIBRATED":
                    pass

                if mode is "CAPTURE":
                    ret, mtx, dist, rotation, translation, = calibrate(w, h)

                if mode is "DETECTION":
                    cv.putText(frame, f'surinkta: {len(img_points)}', (400, 400), cv.FONT_HERSHEY_DUPLEX, 1,
                               (255, 255, 255),
                               1)
                    cv.imshow('testas', frame)
                    key = cv.waitKey(1)
                    if key == 27:
                        break
            else:
                break

        capture.release()

    # if a video path was not supplied, grab the reference to the web cam
    if not args.get("video", False):
        print("starting video stream...")
        t0 = threading.Thread(target=capture, args=(mode, previous,))
        t0.start()
        # otherwise, grab a reference to the video file
    else:
        vs = cv.VideoCapture(file)



if __name__ == '__main__':
    #print(__doc__)
    main()
    cv.destroyAllWindows()
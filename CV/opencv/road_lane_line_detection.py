import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
import pdb

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match = 255
    cv.fillPoly(mask, vertices, match)
    masked = cv.bitwise_and(img, mask)
    return masked


def draw(target, vectors):
    target = np.copy(target)
    blank = np.zeros((target.shape[0], target.shape[1], 3), np.uint8)
    for line in vectors:
        for x1, y1, x2, y2 in line:
            cv.line(blank, (x1, y1), (x2, y2), (0, 255, 255), 3)

    target = cv.addWeighted(target, 0.8, blank, 1, 0.0)
    return target


# source = cv.imread('data/road.jpg')
# image  = cv.cvtColor(source, cv.COLOR_BGR2RGB)

def process(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    canny = cv.Canny(gray, 100, 110)
    height, width, channels = image.shape
    interest = [(0, height), (width/2, height/2), (width, height)]
    crop = region_of_interest(canny, np.array([interest], np.int32))

    lines = cv.HoughLinesP(
        crop,
        rho=1,
        theta=np.pi/60,
        threshold=120,
        lines=np.array([]),
        minLineLength=15,
        maxLineGap=5
        )
    if lines is None:
        return None
    else:
        result = draw(image, lines)
        return result


capture = cv.VideoCapture('data/road_solid_white_right.mp4')
while capture.isOpened():
    ret, frame = capture.read()
    if ret:
        frame = process(frame)
        cv.imshow('vaizdas', frame)

        key = cv.waitKey(30)
        if key == 27:
            break
    else:
        break

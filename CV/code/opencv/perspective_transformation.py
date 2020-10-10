import cv2 as cv
import numpy as np

capture = cv.VideoCapture(0)



while capture.isOpened():
    ret, frame = capture.read()

    key = cv.waitKey(1)
    if key == 27:
        break

    cv.imshow('frame', frame)

capture.release()
cv.destroyAllWindows()

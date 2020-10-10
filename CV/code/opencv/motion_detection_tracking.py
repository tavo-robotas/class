import  cv2 as cv
import numpy as np


capture = cv.VideoCapture('data/vtest.avi')
ret, fr1 = capture.read()
ret, fr2 = capture.read()

while capture.isOpened():

    diff = cv.absdiff(fr1, fr2)
    grey = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(grey, (5, 5), 0)
    _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)

    dilate = cv.dilate(thresh, None, iterations=3)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    for contour in contours:
        (x, y, w, h) = cv.boundingRect(contour)
        if cv.contourArea(contour) < 700:
            continue
        else:
            cv.rectangle(fr1, (x, y), (x+w, y+h), (255, 255, 255), 2)
            cv.putText(fr1, 'status movement', (10, 20), cv.FONT_HERSHEY_SIMPLEX, 1,
                       (255, 255, 255), 2)

    #cv.drawContours(fr1, contours, -1, (0, 255, 255), 2)
    cv.imshow('vaizdas', fr1)
    fr1 = fr2
    ret, fr2 = capture.read()
    if cv.waitKey(60) == 27:
        break

cv.destroyAllWindows()
capture.release()

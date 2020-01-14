from camera import Stream
import cv2
from datetime import datetime

stream = Stream()
stream.start()

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

while True:

    # get image from webcam
    image = stream.get_current_frame()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    print('im not blocked')
    cv2.imshow('grid', gray)
    cv2.waitKey(100)

    # save image to file, if pattern found
    ret, corners = cv2.findChessboardCorners(gray, (7, 7), None)

    if ret == True:
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        filename = datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg'
        cv2.imwrite("data/sample_images/" + filename, gray)



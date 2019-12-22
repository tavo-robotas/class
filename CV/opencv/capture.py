import cv2

# default in-built camera video capture.
# Its likely that your in-built camera as well is indexed with 0
capture = cv2.VideoCapture(0)

# The list of available codes can be found in http://www.fourcc.org/codecs.php
fcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter('capture.avi', fcc, 20.0, (640, 480))

# indefinitely running loop while capture is opened
while capture.isOpened():
    retain, frame = capture.read()
    if retain:
        # getting video capture property
        # https://docs.opencv.org/4.0.0/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
        h = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        w = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print (h, w)
        # converting color image to grey scale by using opencv code COLOR_BGR2GRAY

        output.write(frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('testas', gray)

        key = cv2.waitKey(1)
        if key == 27:
            break

        # if cv2.waitKey(1) and 0xFF == ord('q'):
        #     break
    else:
        break

capture.release()
output.release()
cv2.destroyAllWindows()
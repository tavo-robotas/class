import cv2

# default in-built camera video capture.
# Its likely that your in-built camera as well is indexed with 0
capture = cv2.VideoCapture(0)

h = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
w = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(h, w)

# cv2.CAP_PROP_FRAME_WIDTH  - 3
# cv2.CAP_PROP_FRAME_HEIGHT - 4
capture.set(3, 1280)
capture.set(4, 720)

h = capture.get(3)
w = capture.get(4)
print(h, w)

# indefinitely running loop while capture is opened
while capture.isOpened():
    retain, frame = capture.read()
    if retain:

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
cv2.destroyAllWindows()
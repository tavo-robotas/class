import cv2
import  datetime
# default in-built camera video capture.
# Its likely that your in-built camera as well is indexed with 0
capture = cv2.VideoCapture(0)

# indefinitely running loop while capture is opened
while capture.isOpened():
    retain, frame = capture.read()
    if retain:

        font = cv2.FONT_HERSHEY_COMPLEX
        frame = cv2.putText(frame, str(datetime.datetime.now()), (10,50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('testas', frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

        # if cv2.waitKey(1) and 0xFF == ord('q'):
        #     break
    else:
        break

capture.release()
cv2.destroyAllWindows()
import cv2 as cv
import math

v_source = 0
capture = cv.VideoCapture(v_source)

# cv2.CAP_PROP_FRAME_WIDTH  - 3
# cv2.CAP_PROP_FRAME_HEIGHT - 4
# capture.set(3, 1280)
# capture.set(4, 720)
#
# h = capture.get(3)
# w = capture.get(4)
# print(h, w)


markers = []
alpha   = 0.4
h_theta = 140/2
v_theta = 129/2

center = (0, 0)
target = (0, 0)




def mark_event(ev, x, y, flags, param):
    if ev == cv.EVENT_LBUTTONDOWN:

        target = x, y

        markers.append((x, y))
        cv.arrowedLine(frame, center, target, (255, 255, 255), 2)
        cv.circle(frame, target, 10, (255, 0, 0), -1)

        cv.imshow('testas', frame)
        # if len(markers) >= 2:
        #     cv.rectangle(frame, markers[-1], markers[-2], (255, 255, 0), 2)
        #     cv.imshow('testas', frame)

# indefinitely running loop while capture is opened


def distance(points, mark):
    x_o, y_o = points
    x_t, y_t = mark

    if x_t > x_o :
        return tuple(abs(b - a) for a, b in zip(points, mark))
    else:
        return tuple((b - a) for a, b in zip(points, mark))


def error(coordinates):
    # returns radians
    x, y = coordinates
    x_error = math.degrees(math.atan(((2*x)*math.tan(h_theta))/frame.shape[1]))
    y_error = math.degrees(math.atan(((2*y)*math.tan(v_theta))/frame.shape[0]))

    return x_error, y_error


while capture.isOpened():
    retain, frame = capture.read()

    # memory leak ?
    overlay = frame.copy()
    if retain:

        h, w = frame.shape[:2]

        x_min = 0
        x_max = int(frame.shape[1])
        x_mid = int(frame.shape[1] / 2)
        y_min = 0
        y_max = int(frame.shape[0])
        y_mid = int(frame.shape[0] / 2)
        center = x_mid, y_mid

        cv.line(frame, (x_min, y_mid), (x_max, y_mid), (0, 0, 255), 2)
        cv.line(frame, (x_mid, y_min), (x_mid, y_max), (0, 0, 255), 2)
        cv.circle(frame, (int(x_mid), int(y_mid)), 10, (0, 0, 255), 2)
        cv.setMouseCallback('testas', mark_event)
        if len(markers) >= 1:
            target = distance((x_mid, y_mid), markers[-1])
            angles = error(target)
            print(angles)
        # if len(markers) >= 2:
        #     cv.rectangle(overlay, markers[-1], markers[-2], (0, 0, 255), -1)
        #     x1, y1 = markers[-2]
        #     x2, y2 = markers[-1]
        #     print(x1, y1)
        #     print(x2, y2)
            # [y,x] cut, why not [x ,y] ?
            # ROI = frame[y1:y2, x1:x2]
            # ROI_HSV = cv.cvtColor(ROI, cv.COLOR_BGR2HSV)
            # cv.imshow('ROI', ROI_HSV)

            # color = ('h', 's', 'v')
            # for i, col in enumerate(color):
            #     hist = cv.calcHist([ROI_HSV], [i], None, [256], [0, 256])
            #     plt.plot(hist, color=col)
            #     plt.xlim([0, 256])
            # plt.show()

            # hist = cv.calcHist([ROI_HSV], [0], None, [256], [0, 256])
            # cv.imshow('hist', hist)
            # plt.plot(hist)
            # plt.ion()
            # plt.plot(hist)
            # plt.pause(0.05)
            # plt.show()
        # cover = cv.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        cv.imshow('testas', frame)

        key = cv.waitKey(1)
        if key == 27:
            break

        # if cv2.waitKey(1) and 0xFF == ord('q'):
        #     break
    else:
        break

capture.release()
cv.destroyAllWindows()
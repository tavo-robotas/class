import numpy as np
import cv2

# events = [i for i in dir(cv2) if 'EVENT' in i]
# print(events)
font = cv2.FONT_HERSHEY_COMPLEX

def onclick(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            points.append((x, y))
            if len(points) >= 2:
                cv2.line(image, points[-1], points[-2], (255, 255, 255), 4, cv2.LINE_AA)
            cv2.circle(image,(x, y), 5, (0, 0, 255), -1)
            cv2.imshow('kordinatės', image)

# image = np.zeros((512, 512, 3), np.uint8)
image = cv2.imread('data/me.jpg', 1)
cv2.imshow('kordinatės', image)

points = list()


cv2.setMouseCallback('kordinatės', onclick)
cv2.waitKey(0)
cv2.destroyAllWindows()
import numpy as np
import cv2

# events = [i for i in dir(cv2) if 'EVENT' in i]
# print(events)
font = cv2.FONT_HERSHEY_COMPLEX

def onclick(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            blue = image[x, y, 0]
            green = image[x, y, 1]
            red = image[x, y, 2]

            cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
            color = np.zeros((image.shape), np.uint8)

            color[:] = [blue, green, red]
            cv2.imshow('color', color)

# image = np.zeros((512, 512, 3), np.uint8)
image = cv2.imread('data/me.jpg', 1)
cv2.imshow('kordinatės', image)

points = list()


cv2.setMouseCallback('kordinatės', onclick)
cv2.waitKey(0)
cv2.destroyAllWindows()
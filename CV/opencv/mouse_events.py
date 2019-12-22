import numpy as np
import cv2

# events = [i for i in dir(cv2) if 'EVENT' in i]
# print(events)
font = cv2.FONT_HERSHEY_COMPLEX

def onclick(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            print(x, ', ', y)
            strXY = str(x) + ', ' + str(y)
            cv2.putText(image, strXY, (x, y), font, 0.5, (255, 255, 255), 1)
            cv2.imshow('kordinatės', image)
        if event == cv2.EVENT_RBUTTONDBLCLK:
            blue  = image[y, x, 0]
            green = image[y, x, 1]
            red   = image[y, x, 2]
            strBGR = str(blue) + ', ' + str(green) +', ' + str(red)
            cv2.putText(image, strBGR, (x, y), font, 0.5, (0, 255, 255), 1)
            cv2.imshow('kordinatės', image)


# image = np.zeros((512, 512, 3), np.uint8)
image = cv2.imread('data/me.jpg', 1)
cv2.imshow('kordinatės', image)
cv2.setMouseCallback('kordinatės', onclick)
cv2.waitKey(0)
cv2.destroyAllWindows()
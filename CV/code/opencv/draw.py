import numpy as np
import cv2

#image = cv2.imread('data/me.jpg', 1)

image = np.zeros([650, 650, 3], np.uint8)
image = cv2.line(image, (0, 0), (255, 255), (0, 0, 255), 5)
image = cv2.arrowedLine(image, (640, 0), (0, 255), (0, 255, 0), 5)

image = cv2.rectangle(image, (200, 5), (600, 400), (0, 0, 255), 1)
image = cv2.circle(image, (340, 240), 40, (255, 255, 255), 5)
image = cv2.putText(image, 'Hello', (200, 550), cv2.FONT_HERSHEY_COMPLEX, 4,  (255, 255, 255), 5, cv2.LINE_AA)
# x1, y1 --------------|
# |                    |
# |                    |
# |                    |
# -------------------- x2, y2
cv2.imshow('window', image)
cv2.waitKey(0)
cv2.destroyAllWindows()


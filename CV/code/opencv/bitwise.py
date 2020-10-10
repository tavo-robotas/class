import  numpy as np
import cv2

image = np.zeros((512, 512, 3), np.uint8)
image = cv2.circle(image, (256, 256), 150, (255, 255, 255), -1)
kvadr = cv2.imread('data/square.jpg')

# bit_and = cv2.bitwise_and(image, kvadr)
# bit_or = cv2.bitwise_or(image,kvadr)
# bit_xor = cv2.bitwise_xor(image, kvadr)
bit_not = cv2.bitwise_not(image, kvadr)
#cv2.imshow('l_1', kvadr)
#cv2.imshow('l_2', image)

# cv2.imshow('bitwise',  bit_and)
# cv2.imshow('bitwise', bit_or)
# cv2.imshow('bitwise', bit_xor)
cv2.imshow('bitwise', bit_not)

cv2.waitKey(0)
cv2.destroyAllWindows()
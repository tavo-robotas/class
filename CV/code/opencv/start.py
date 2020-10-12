import cv2

# checks opencv version
print(cv2.__version__)

# read an image, flags
# cv2.IMREAD_COLOR ,    1  Loads a color image
# cv2.IMREAD_GRAYSCALE  0  Loads image in grey scale mode
# cv2.IMREAD_UNCHANGED -1  Loads image as such including alpha channel
image = cv2.imread('data/me.jpg', 1)

# observe the output which suppose to be a matrix of image
# if response is none then cv2.imread() has failed to open image file
print(image)

# images was displayed for a millisecond and disappear
cv2.imshow('testas', image)
# waitKey will postpone image window display
# arguments are milliseconds, in case its 0 then it will keep window displayed all the time
key = cv2.waitKey(0)

# 27 mean ESC key on keyboard
if key == 27:
    cv2.destroyAllWindows()
# to save image press s key on keyboard
elif key == ord('s'):
    cv2.imwrite('data/me_clone.png', image)
    cv2.destroyAllWindows()

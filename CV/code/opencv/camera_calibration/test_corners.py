import cv2 as cv

board = (7, 7)
image = cv.imread('data/03_06/edited/f01.JPG')
gray  = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
found, corners = cv.findChessboardCorners(
    gray,
    board,
    cv.CALIB_CB_ADAPTIVE_THRESH,
    cv.CALIB_CB_NORMALIZE_IMAGE,
)

if found:
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

chess = cv.drawChessboardCorners(image, board, corners2, found)
print("chess shape: \n")
print(chess.shape)
print("chess size: \n")
print(chess.size)
print("data: \n")
print(chess)
print("image shape: \n")
print(image.shape)
cv.circle(image, (147, 147), 10, (0, 0, 255), -1)
cv.imshow('chess', chess)
cv.waitKey(0)

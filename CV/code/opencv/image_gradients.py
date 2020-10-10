import cv2 as cv
from matplotlib import pyplot as plt
import  numpy as np

image = cv.imread('data/sudoku.jpg', cv.IMREAD_GRAYSCALE)

laplacian = cv.Laplacian(image, cv.CV_64F, ksize=3)
laplacian = np.uint8(np.absolute(laplacian))

sobelX  = cv.Sobel(image, cv.CV_64F, 1, 0)
sobelX  = np.uint8(np.absolute(sobelX))
sobelY  = cv.Sobel(image, cv.CV_64F, 0, 1)
sobelY  = np.uint8(np.absolute(sobelY))
sobleXY = cv.bitwise_or(sobelX, sobelY)
canny   = cv.Canny(image, 100, 200)

titles = ['original', 'laplacian', 'sobelX', 'sobelY', 'sobleXY', 'canny']
images = [image, laplacian, sobelX, sobelY, sobleXY, canny]

for i in range(len(images)):
    plt.subplot(2, 3, i+1)
    plt.title(titles[i])
    plt.imshow(images[i], 'gray')
    plt.xticks([]), plt.yticks([])

plt.show()
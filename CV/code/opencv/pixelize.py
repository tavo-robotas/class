import cv2

name = 'AT'

# Input image
input = cv2.imread('data/'+name+'.jpg')

# Get input size
height, width = input.shape[:2]

# Desired "pixelated" size
w, h = (16, 16)

# Resize input to "pixelated" size
temp = cv2.resize(input, (w, h), interpolation=cv2.INTER_LINEAR)

# Initialize output image
output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

cv2.imshow('Input', input)
cv2.imshow('Output', output)

print('press a key inside the image to make a copy')
cv2.waitKey(0)

print('image was copied to folder images/copy')
cv2.imwrite("data/copy/"+name+"-copy.jpg", output)

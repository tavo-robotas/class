import cv2 as cv
import matplotlib.pyplot as plt
import argparse
import numpy as np

ap = argparse.ArgumentParser()

ap.add_argument("-f", "--file", type=str, help="path to video file if not using camera")
ap.add_argument("-c", "--color",type=str, help="color space, default: gray", default="rgb")
ap.add_argument("-b", "--bins", type=int, help="number of bins per channel", default=16)
ap.add_argument("-w", "--width", type=int, help="resize video but maintain aspect", default=0)

args = vars(ap.parse_args())

if not args.get('file', False):
    capture = cv.VideoCapture(0)
else:
    capture = cv.VideoCapture(args.get('file'))

color = args.get('color')
bins  = args.get('bins')
n_width = args.get('width')

fig, ax = plt.subplots()
if color == 'rgb':
    ax.set_title('Histo (RGB)')
else:
    ax.set_title('Histo (GRAY)')

lw = 3
alpha = 0.5

plt.setp(
    ax,
    xlim=(0,bins-1),
    ylim=(0,1),
    xlabel="bins",
    ylabel="freq"

)
if color == 'rgb':
    lineR, = ax.plot(np.arange(bins), np.zeros((bins,)), c='r', lw=lw, alpha=alpha)
    lineG, = ax.plot(np.arange(bins), np.zeros((bins,)), c='g', lw=lw, alpha=alpha)
    lineB, = ax.plot(np.arange(bins), np.zeros((bins,)), c='b', lw=lw, alpha=alpha)

else:
    lineK, = ax.plot(np.arange(bins), np.zeros((bins, 1)), c='k', lw=lw, alpha=alpha)


plt.ion()
plt.show()

while capture.isOpened():
    (ret, frame) = capture.read()
    if ret:
        if n_width > 0:
            h, w = frame.shape[:2]
            n_height = int(float(n_width/h) * h)
            frame = cv.resize(frame, (n_width, n_height), interpolation=cv.INTER_AREA)
        pixel = np.prod(frame.shape[:2])
        if color == 'rgb':
            cv.imshow('rgb', frame)
            (b, g, r) = cv.split(frame) # splits channels
            hisR = cv.calcHist([r], [0], None, [bins], [0, 255]) / pixel
            hisG = cv.calcHist([g], [0], None, [bins], [0, 255]) / pixel
            hisB = cv.calcHist([b], [0], None, [bins], [0, 255]) / pixel
            lineR.set_ydata(hisR)
            lineG.set_ydata(hisG)
            lineB.set_ydata(hisB)
        else:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            cv.imshow('gray', gray)
            hisK = cv.calcHist([gray], [0], None, [bins], [0, 255]) / pixel
            lineK.set_ydata(hisK)

        fig.canvas.draw()
        key = cv.waitKey(1)
        if key == 27:
            break
    else:
        break

capture.release()
cv.destroyAllWindows()
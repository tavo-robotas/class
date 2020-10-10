from threading import Thread
import cv2 as cv


class View:
    def __init__(self, frame=None, name='video', stop=False):
        self.frame = frame
        self.name = name
        self.stopped = stop

    def start(self):
        try:
            Thread(target=self.show, args=(), daemon=True).start()
            return self
        except :
            print('error: failed to start thread')

    def show(self):
        while not self.stopped:
            cv.namedWindow(self.name, cv.WINDOW_AUTOSIZE)
            cv.imshow(self.name, self.frame)
            key = cv.waitKey(1)
            if key == 27 or self.stopped:
                self.stopped = True

    def stop(self):
        self.stopped = True

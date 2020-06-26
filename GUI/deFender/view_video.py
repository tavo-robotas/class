from threading import Thread
import cv2 as cv

import pdb
class ViewVideo():

    def __init__(self, frame=None, stop=False):
        self.frame = frame
        self.stop = stop

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):

        while not self.stop:
            return self.frame
            # cv.imshow("video", self.frame)
            # key = cv.waitKey(1)
            if key == 27 or self.stop:
                self.stop = True

    def stopit(self):
        self.stop =True
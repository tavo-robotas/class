from threading import Thread
import cv2 as cv
from queue import Queue

class Capture():
    """
    Class that continuously gets frames from a video capture object
    with a dedicated thread.
    """

    def __init__(self, src=0, stop=False):
        self.stream = cv.VideoCapture(src)
        self.retain, self.frame = self.stream.read()
        # flag that thread should stop grabbing frames
        self.stop = stop

    def start(self):
        # Creates and starts the thread
        # that executes the get() function
        # which continuously runs a loop that reads frames
        Thread(target=self.get, args=(), daemon=True).start()
        return self

    def get(self):
        while not self.stop:
            if not self.retain:
                self.stopit()
            else:
                self.retain, self.frame = self.stream.read()

    def read(self):
        return self.get()

    def stopit(self):
        self.stop = True

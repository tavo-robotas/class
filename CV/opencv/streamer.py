from threading import Thread
import cv2 as cv
from queue import Queue


class Stream:
    def __init__(self, src=0, stop=False, size=128):
        self.stream = cv.VideoCapture(src)
        self.retain, self.frame = self.stream.read()
        # flag that thread should stop grabbing frames
        self.stopped = stop

        #self.queue = Queue(maxsize=size)

    def start(self):
        try:
            Thread(target=self.update, args=(), daemon=True).start()
            return self
        except:
            print('error: failed to start thread')

    def update(self):
        while not self.stopped:
            if not self.retain:
                self.stop()
            else:
                self.retain, self.frame = self.stream.read()
                # if not self.queue.full():
                #     self.retain, self.frame = self.stream.read()
                #     self.queue.put(self.frame)
                # else:
                #     self.stopit()

    def read(self):
        return self.frame
        #return self.queue.get()

    def more(self):
        return self.queue.qsize() > 0

    def stop(self):
        self.stopped = True

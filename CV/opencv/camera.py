import cv2
import pyrealsense2 as rs
import numpy as np
from threading import Thread


def pipeline():
    cfg = rs.config()
    cfg.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    pipe = rs.pipeline()
    pipe.start(cfg)
    return pipe


def getframe(pipeline):
    frames = pipeline.










































































































































































































































































    ()
    # take owner ship of the frame for further processing

    color_frame = frames.get_color_frame()
    if color_frame:

        data = color_frame.as_frame().get_data()
        color_image = np.asanyarray(data)
        print('returning color')
        return color_image
    else:
        return None



class Stream:

    def __init__(self):
        self.pipeline = pipeline()

        self.video_capture = cv2.VideoCapture(0)
        self.current_frame = self.update_frame()

    # create thread for capturing images
    def start(self):
        Thread(target=self.update_frame, args=()).start().join()


    def update_frame(self):
        while 1:
            self.current_frame = getframe(self.pipeline)


    def get_current_frame(self):
        return self.current_frame

import cv2 as cv
from common import splitfn
import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor

class Processor:
    """
       Class that continuously gets frames from a video capture object
       and processes them by applying chessboard pattern recognition algorithms
    """
    def __init__(self, square_size, pattern_size, debug_dir=False):
        self.square_size = float(square_size)
        self.pattern_size = tuple(pattern_size)
        self.debug_dir = debug_dir

        self.pattern_points = np.zeros((np.prod(self.pattern_size), 3), np.float32)
        self.pattern_points[:, :2] = np.indices(self.pattern_size).T.reshape(-1, 2)
        self.pattern_points *= self.square_size

    def take(self, image):

        if image is None:
            print(f"failed to load {image}")
            return None

        with ProcessPoolExecutor() as executor:
            results = executor.map(self.process_images(image), image)

        return results

    def process_images(self, image):
        found, corners = cv.findChessboardCorners(image, self.pattern_size)
        if found:
            term = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_COUNT, 30, 0.001)
            cv.cornerSubPix(image, corners, (11, 11), (-1, -1), term)

        if self.debug_dir:
            vis = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
            cv.drawChessboardCorners(vis, self.pattern_size, corners, found)
            _path, name, _ext = splitfn(image)
            outfile = os.path.join(self.debug_dir, name + '_chess.png')
            cv.imwrite(outfile, vis)

        if not found:
            print('chessboard not found')
            #return None
        else:
            print('           %s... OK' % image)
            print(self.pattern_size)
            return corners.reshape(-1, 2), self.pattern_points

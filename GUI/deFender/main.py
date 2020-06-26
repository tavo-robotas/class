import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

import pdb

import cv2 as cv
from get_video import Capture
from view_video import ViewVideo
from ui_main_window import *

class MainWindow(QWidget):
    # class constructor
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.cap  = Capture().start()
        self.view = ViewVideo(self.cap.frame).start()
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer)

    # view camera
    def viewCam(self):
        # read image in BGR format

        image = self.cap.frame
        # convert image to RGB format
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_Grayscale8)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():

            self.timer.start(20)
            self.ui.control_bt.setText("Stop")
        else:
            print('stoping')

            self.timer.stop()
            self.cap.stopit()
            print(self.view.stop)
            self.ui.control_bt.setText("Start")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.showMaximized()

    sys.exit(app.exec_())
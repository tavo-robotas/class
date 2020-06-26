from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QSize, QUrl, QDir
from PyQt5.QtQml import QQmlApplicationEngine
import sys

properties = {
    't': 'deFender',
    'u': 100,
    'l': 100,
    'w': 800,
    'h': 600,
    's_i': 'favicon-16x16.png',
    'l_i': 'favicon-32x32.png'
}

names = ['Automatinis rėžimas', 'Būklė', 'Perkauti sistemą', 'Išjungti']

class Window(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.create_button()
        self.init_win()

    def init_win(self):
        self.setWindowIcon(QtGui.QIcon(self.s_i))
        self.setWindowTitle(self.t)
        self.setGeometry(self.u, self.l, self.w, self.h)



        # show() schedules a paint event
        self.show()


    def click_event(self):
        sys.exit()

    def create_button(self):
        button = QPushButton('exit', self)
        button.setGeometry(QRect(100, 100, 100, 50))
        button.setIcon(QtGui.QIcon(self.l_i))
        button.setIconSize(QSize(40, 40))
        button.setToolTip('<h3>This is eye button</h3>')
        button.clicked.connect(self.click_event)


class UI(QDialog):

    def __init__(self, *args, **kwargs):
        super(UI, self).__init__(*args, *kwargs)
        self.vbox = QVBoxLayout()
        self.init_win()

    def init_map(self):
        pass

    
    def init_win(self):
        self.hbox = QHBoxLayout()
        self.setWindowIcon(QtGui.QIcon(self.s_i))
        self.setWindowTitle(self.t)
        # setGeometry (x,y, width, height)
        self.setGeometry(self.u, self.l, self.w, self.h)
        self.addButtons()
        self.show()


    def addButtons(self):
        for _, i in enumerate(range(len(names))):
            button = Button(names[i], self)
            self.hbox.addWidget(button)
        self.setLayout(self.hbox)


for key, value in properties.items():
    setattr(Window, key, value)

for key, value in properties.items():
    setattr(UI, key, value)


class Button(QPushButton):

    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        #self.setGeometry(QRect(80, 40, 40, 50))
        self.setIcon(QtGui.QIcon())
        self.setIconSize(QSize(40, 40))
        self.setMinimumHeight(40)
        self.setToolTip('<h3>This is button</h3>')
        self.clicked.connect(self.click_event)

    def click_event():
        sys.exit()

def main():
    # sys.argv has to be passed because app
    # deals with common command line arguments
    # if application is not going to accept command line arguments
    # us empty list []
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load('main.qml')

    if not engine.rootObjects():
        return -1

    #engine.load(QUrl(QStringLiteral("qrc:/main.qml")))
    # view = QWebEngineView()
    # view.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
    # view.load(QUrl.fromLocalFile(QDir.current().absoluteFilePath('polyline.html')))
    #view.show()

    # ui = UI()
    # sys.exit() allows you to cleanly exit python
    # and release memory when the app terminates
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

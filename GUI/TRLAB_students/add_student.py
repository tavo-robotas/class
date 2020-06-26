from PyQt5.QtWidgets import *

class AddStudent(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Add student")
        self.resize(700, 700)
        self.center()
        self.layout()
        self.show()

    def layout(self):
        self.layout = QVBoxLayout()
        self.top    = QVBoxLayout()
        self.bottom = QFormLayout()
        self.layout.addLayout(self.top)
        self.layout.addLayout(self.bottom)
        self.setLayout(self.layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
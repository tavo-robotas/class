from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from db import DataBase
import sqlite3
from add_student import AddStudent


con = sqlite3.connect('lab.db')
cur = con.cursor()

tabs = ["Bendra", "Studentai", "Finansai"]


class Main(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("TRLab students")
        #self.setWindowState(Qt.WindowMaximized)
        self.resize(700, 700)
        self.center()
        self.students()
        self.layouts()

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()
        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()
        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)
        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def layouts(self):
        self.main_layout = QVBoxLayout()
        self.students_layout = QHBoxLayout()
        self.tabs = QTabWidget()

        self.leftLayout = QFormLayout()
        self.rightLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightButtonLayout = QHBoxLayout()

        self.rightLayout.addLayout(self.rightTopLayout)
        self.rightLayout.addLayout(self.rightButtonLayout)

        self.rightTopLayout.addWidget(self.studentsList)
        self.rightButtonLayout.addWidget(self.add_btn)
        self.rightButtonLayout.addWidget(self.update_btn)
        self.rightButtonLayout.addWidget(self.delete_btn)

        self.students_layout.addLayout(self.leftLayout, 40)
        self.students_layout.addLayout(self.rightLayout, 60)


        for i, name in enumerate(tabs):
            self.tab = QWidget()
            if name == 'Studentai':
                self.tab.setLayout(self.students_layout)
            self.tabs.addTab(self.tab, tabs[i])

        self.main_layout.addWidget(self.tabs)

        self.setLayout(self.main_layout)

    def students(self):
        self.studentsList = QListWidget()
        self.add_btn      = QPushButton("Add")
        self.update_btn   = QPushButton("Update")
        self.delete_btn   = QPushButton("Delete")

        self.add_btn.clicked.connect(self.add_student)

    def add_student(self):
        self.new_student = AddStudent()
        self.close()

def main():
    app = QApplication([])
    #db = DataBase()
    #db.print_db()
    win = Main()
    win.showMaximized()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
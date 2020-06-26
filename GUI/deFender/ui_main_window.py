from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

class Ui_Form(object):

    def setupUi(self, Form):
        Form.resize(800, 800)

        self.mainlayout       = QHBoxLayout()
        self.optionlayout = QHBoxLayout()
        self.maplayout    = QVBoxLayout()
        self.imagelayout  = QVBoxLayout()
        self.videolayout  = QHBoxLayout()

        self.mainlayout.addLayout(self.optionlayout)
        self.mainlayout.addLayout(self.maplayout)
        self.maplayout.addLayout(self.imagelayout)
        self.mainlayout.addLayout(self.videolayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.image_label = QtWidgets.QLabel(Form)
        self.verticalLayout.addWidget(self.image_label)

        self.control_bt = QtWidgets.QPushButton(Form)



        self.verticalLayout.addWidget(self.control_bt)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)




    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "deFender"))
        self.image_label.setText(_translate("Form", "TextLabel"))
        self.control_bt.setText(_translate("Form", "Start"))
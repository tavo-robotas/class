import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

def app():
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.setWindowTitle('XO')
    widget.show()
    sys.exit(app.exec_())
app()
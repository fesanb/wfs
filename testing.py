from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        widget = QLabel("Hello")
        widget.setPixmap(QPixmap("wind-circle.png"))
        widget.setScaledContents(True)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = QMainWindow()
window.show() # IMPORTANT!!!!! Windows are hidden by default.
# Start the event loop.
app.exec_()

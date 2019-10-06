import sys, os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import pyqtgraph as pg
import mysql.connector
import threading
import time
from datetime import datetime
from datetime import timedelta


class Color(QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


def graph():
    x = 2, 5, 6, 10
    y = 1, 2, 3, 6
    graph.data_X = x
    graph.data_Y = y


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)

        self.setWindowTitle("My Awesome App")

        self.layout = QVBoxLayout()

        self.button = QPushButton("OK", self)
        self.button.setCheckable(True)
        self.button.resize(50, 32)
        self.button.move(50, 50)
        self.button.clicked.connect(self.clickMethod)

        x = 2, 5, 6, 10
        y = 1, 2, 3, 6
        self.layout.addWidget(pg.plot(x, y))
        self.layout.addWidget(self.button)

    def clickMethod(self):
        MainWindow.initUI.l.setText("CHANGE")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

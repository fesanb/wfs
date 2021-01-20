import sys, os

from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

class App(QWidget):

	def __init__(self, parent=None):
		super(App, self).__init__(parent=parent)
		self.title = "WFS - Weather Forecast Station"
		self.setWindowIcon(QIcon("img/drawing.svg.png"))
		self.setWindowTitle(self.title)
		# self.setStyleSheet("color: white; background-color: black;")

		self.left = 0
		self.top = 0
		self.width = 720
		self.height = 480
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.initUI()

	def initUI(self):
		self.O1 = QVBoxLayout(self)

		self.gwb = QPushButton()
		self.gwb.setText("WIND")
		self.gwb.setCheckable(True)
		self.gwb.clicked.connect(data)
		self.O1.addWidget(self.gwb)


def data():
	print("test")
	gwb.setText("clicked")

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.show()

	sys.exit(app.exec_())



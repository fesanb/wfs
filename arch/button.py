import sys, os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QSize


class App(QWidget):

	def __init__(self, parent=None):
		super(App, self).__init__(parent=parent)
		self.title = "WFS - Weather Forecast Station"
		self.setWindowIcon(QIcon("img/drawing.svg.png"))
		self.left = 0
		self.top = 0
		self.width = 720
		self.height = 480
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setStyleSheet("color: white; background-color: #666666;")
		self.initUI()

		self.win = QWidget()

	def initUI(self):
		self.O1 = QVBoxLayout(self)
		self.mainContainer = QHBoxLayout(self)
		self.button = QPushButton("OK", self)
		self.button.setCheckable(True)
		self.button.resize(50, 32)
		self.button.move(50, 50)
		self.button.clicked.connect(self.clickMethod)
		self.mainContainer.addWidget(self.button)

		self.test()

		self.O1.addLayout(self.mainContainer)

	def test(self):
		self.l = QLabel("TEST")
		self.mainContainer.addWidget(self.l)

	def clickMethod(self):
		App.initUI.l.setText("CHANGE")


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.show()

	sys.exit(app.exec_())

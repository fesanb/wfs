import sys
#from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import mysql.connector
import threading
import time


class GetData(object):
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.mysql_fetch, args=())
        thread.daemon = True
        thread.start()

        #self.db_wind = ""

    def mysql_fetch(self):
        while True:
            cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
            cursor = cnx.cursor()

            get_wind = "SELECT * FROM wind WHERE id=(SELECT MAX(id) FROM wind)"
            cursor.execute(get_wind)
            db_wind = cursor.fetchone()
            self.wind = str(db_wind[1])

            print("Thread Running")
            print(self.wind)

            time.sleep(self.interval)


data = GetData()


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "WFS - Weather Forecast Station"
        self.setWindowIcon(QIcon("drawing.svg.png"))
        self.left = 475
        self.top = 650
        self.width = 450
        self.height = 350
        self.initUI()

        #self.wind_label = ""

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.wind_label = QLabel("wind: " + data.wind + "m/s", self)
        self.wind_label.move(50, 50)
        self.wind_label.adjustSize()

        self.show()

    def update_label(self):
        #wind = str(data.wind[1])
        #print("test " + wind)
        #a = app()
        self.wind_label.setText(data.wind)  # <<< My line of problem. :)
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    timer = QTimer()
    timer.timeout.connect(ex.update_label)
    timer.start(1000)

    sys.exit(app.exec_())

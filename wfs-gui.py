import sys
from PyQt5.QtGui import *
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

    def mysql_fetch(self):
        while True:
            cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
            cursor = cnx.cursor()

            get_wind = "SELECT * FROM wind WHERE id=(SELECT MAX(id) FROM wind)"
            cursor.execute(get_wind)
            db_wind = cursor.fetchone()
            self.wind = str(db_wind[1])
            self.wind_timestamp = str(db_wind[2])

            get_sens = "SELECT * FROM sens WHERE id=(SELECT MAX(id) FROM sens)"
            cursor.execute(get_sens)
            db_sens = cursor.fetchone()
            self.temp = str(db_sens[1])
            self.hum = str(db_sens[2])
            self.atp = str(db_sens[3])
            self.sens_timestamp = str(db_sens[4])

            get_gps = "SELECT * FROM gps WHERE id=(SELECT MAX(id) FROM gps)"
            cursor.execute(get_gps)
            db_gps = cursor.fetchone()
            self.lat = str(db_gps[1])
            self.long = str(db_gps[2])
            self.alt = str(db_gps[3])
            self.gps_timestamp = str(db_gps[4])

            #print("Thread Running")

            time.sleep(self.interval)


data = GetData()


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "WFS - Weather Forecast Station"
        self.setWindowIcon(QIcon("drawing.svg.png"))
        self.left = 475
        self.top = 650
        self.width = 480
        self.height = 720
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.wind_circle_label = QLabel(self)
        self.wind_circle = QPixmap("wind-circle.png")
        self.wind_circle.scaled(1, 1, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.wind_circle_label.setPixmap(self.wind_circle)
        self.wind_circle_label.move(200, 200)

        self.wind_label = QLabel("wind: " + data.wind + " m/s", self)
        self.wind_label.move(50, 50)
        self.wind_label.adjustSize()

        self.temp_label = QLabel("Temperature: " + data.temp + " °C", self)
        self.temp_label.move(50, 75)
        self.temp_label.adjustSize()

        self.hum_label = QLabel("Humidity: " + data.hum + " %", self)
        self.hum_label.move(50, 100)
        self.hum_label.adjustSize()

        self.atp_label = QLabel("Atm. Pressure: " + data.atp + " mbar", self)
        self.atp_label.move(50, 125)
        self.atp_label.adjustSize()

        self.lat_label = QLabel("Latitude: " + data.lat, self)
        self.lat_label.move(50, 150)
        self.lat_label.adjustSize()

        self.long_label = QLabel("Longitude: " + data.long, self)
        self.long_label.move(50, 175)
        self.long_label.adjustSize()

        self.alt_label = QLabel("Altitude: " + data.alt + " m", self)
        self.alt_label.move(50, 200)
        self.alt_label.adjustSize()

        self.show()

    def update_label(self):
        self.wind_label.setText("wind: " + data.wind + "m/s")
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    timer = QTimer()
    timer.timeout.connect(ex.update_label)
    timer.start(1000)

    sys.exit(app.exec_())

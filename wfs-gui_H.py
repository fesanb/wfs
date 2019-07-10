import sys
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

#Wind
get_wind = "SELECT * FROM wind WHERE id=(SELECT MAX(id) FROM wind)"
get_mean_wind = "SELECT AVG(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 10 MINUTE)"

# GRAPH
get_graph_wind = "SELECT id, ROUND(wind, 0) FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
get_graph_wind_timestamp = "SELECT CAST(tmestmp AS CHAR) FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"

#SENS
get_sens = "SELECT * FROM sens WHERE id=(SELECT MAX(id) FROM sens)"
get_gps = "SELECT * FROM gps WHERE id=(SELECT MAX(id) FROM gps)"

def fetch_wind():
    while True:
        try:
            cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
            cursor = cnx.cursor(buffered=True)

            cursor.execute(get_wind)
            if cursor.rowcount > 0:
                db_wind = cursor.fetchone()
                fetch_wind.wind = str(db_wind[1])
                fetch_wind.timestamp = db_wind[2]
            else:
                fetch_wind.wind = "-.-"

            if fetch_wind.timestamp < datetime.now() - timedelta(minutes=1):
                fetch_wind.wind = "-.-"

            cursor.execute(get_mean_wind)
            db_mean_wind = cursor.fetchone()
            if db_mean_wind[0] is None:  # cursor.rowcount is 0 and
                fetch_wind.meanwind = "0"
            else:
                # print(db_mean_wind[0])
                fetch_wind.meanwind = round(float(db_mean_wind[0]), 0)

            beaufort = [
                "Beaufort 0 - Calm",
                "Beaufort 1 - Light Air",
                "Beaufort 2 - Light breeze",
                "Beaufort 3 - Gentle breeze",
                "Beaufort 4 - Moderate breeze",
                "Beaufort 5 - Fresh breeze",
                "Beaufort 6 - Strong breeze",
                "Beaufort 7 - Moderate gale",
                "Beaufort 8 - Fresh Gale",
                "Beaufort 9 - Strong Gale",
                "Beaufort 10 - Storm",
                "Beaufort 11 - Violent Storm",
                "Beaufort 12 - Hurricane"]

            if float(fetch_wind.meanwind) < 0.3:
                fetch_wind.beaufortLS = beaufort[0]
            elif float(fetch_wind.meanwind) > 32.7:
                fetch_wind.beaufortLS = beaufort[12]
            elif float(fetch_wind.meanwind) > 28.5:
                fetch_wind.beaufortLS = beaufort[11]
            elif float(fetch_wind.meanwind) > 24.5:
                fetch_wind.beaufortLS = beaufort[10]
            elif float(fetch_wind.meanwind) > 20.8:
                fetch_wind.beaufortLS = beaufort[9]
            elif float(fetch_wind.meanwind) > 17.2:
                fetch_wind.beaufortLS = beaufort[8]
            elif float(fetch_wind.meanwind) > 13.9:
                fetch_wind.beaufortLS = beaufort[7]
            elif float(fetch_wind.meanwind) > 10.8:
                fetch_wind.beaufortLS = beaufort[6]
            elif float(fetch_wind.meanwind) > 8.0:
                fetch_wind.beaufortLS = beaufort[5]
            elif float(fetch_wind.meanwind) > 5.5:
                fetch_wind.beaufortLS = beaufort[4]
            elif float(fetch_wind.meanwind) > 3.4:
                fetch_wind.beaufortLS = beaufort[3]
            elif float(fetch_wind.meanwind) > 1.6:
                fetch_wind.beaufortLS = beaufort[2]
            elif float(fetch_wind.meanwind) > 0.3:
                fetch_wind.beaufortLS = beaufort[1]

            time.sleep(1)
        except Exception as e:
            print(repr(e))


def fetch_sens():
    while True:
        try:
            cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
            cursor = cnx.cursor(buffered=True)

            cursor.execute(get_sens)
            if cursor.rowcount > 0:
                db_sens = cursor.fetchone()
                fetch_sens.temp = str(db_sens[1])
                fetch_sens.hum = str(round(db_sens[2]))
                fetch_sens.atp = str(db_sens[3])
                fetch_sens.sens_timestamp = str(db_sens[4])
            else:
                fetch_sens.temp = "0"
                fetch_sens.hum = "0"
                fetch_sens.atp = "0"
                fetch_sens.sens_timestamp = "0"

            time.sleep(45)
            # print(thread2.name)
        except Exception as e:
            print(repr(e))


def fetch_gps():
    while True:
        try:
            cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
            cursor = cnx.cursor(buffered=True)

            cursor.execute(get_gps)
            if cursor.rowcount > 0:
                db_gps = cursor.fetchone()
                fetch_gps.lat = str(db_gps[1])
                fetch_gps.long = str(db_gps[2])
                fetch_gps.alt = str(db_gps[3])
                fetch_gps.gps_timestamp = str(db_gps[4])
            else:
                fetch_gps.lat = "No gps signal"
                fetch_gps.long = "No gps signal"
                fetch_gps.alt = "No gps signal"
                fetch_gps.gps_timestamp = "-"

            time.sleep(45)
            # print(thread3.name)
        except Exception as e:
            print(repr(e))


def fetch_graph():
    while True:
        try:
            cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
            cursor = cnx.cursor(buffered=True)

            cursor.execute(get_graph_wind)
            if cursor.rowcount > 0:
                db_graph_wind = cursor.fetchall()
                fetch_graph.graphwind_X = np.ravel(db_graph_wind[2])
                fetch_graph.graphwind_Y = np.ravel(db_graph_wind[1])
            else:
                fetch_graph.graphwind_X = [0]
                fetch_graph.graphwind_Y = [0]

            time.sleep(45)
            # print(thread4.name)
        except Exception as e:
            print(repr(e))


thread1 = threading.Thread(target=fetch_wind, args=())
thread1.daemon = True
thread1.start()

thread2 = threading.Thread(target=fetch_sens, args=())
thread2.daemon = True
thread2.start()

thread3 = threading.Thread(target=fetch_gps, args=())
thread3.daemon = True
thread3.start()

thread4 = threading.Thread(target=fetch_graph, args=())
thread4.daemon = True
thread4.start()

class App(QWidget):

    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)
        self.title = "WFS - Weather Forecast Station"
        self.setWindowIcon(QIcon("img/drawing.svg.png"))
        # self.left = 0
        # self.top = 0
        # self.width = 720
        # self.height = 480
        self.showFullScreen()
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("color: white; background-color: #000000;")
        self.initUI()

        self.win = QWidget()

    def initUI(self):

        self.O1 = QVBoxLayout(self)
        self.mainContainer = QHBoxLayout(self)
        self.windContainer = QVBoxLayout(self)

        try:
            self.windHeader = QHBoxLayout()
            self.windHL = QLabel("WIND")
            self.windHL.setFont(QFont('Arial', 20))
            self.windHL.setAlignment(Qt.AlignCenter)
            self.windHeader.addWidget(self.windHL)
            self.meanHL = QLabel("MEAN")
            self.meanHL.setFont(QFont('Arial', 20))
            self.meanHL.setAlignment(Qt.AlignCenter)
            self.windHeader.addWidget(self.meanHL)
            self.sensHL = QLabel("SENSOR")
            self.sensHL.setFont(QFont('Arial', 20))
            self.sensHL.setAlignment(Qt.AlignCenter)
            self.windHeader.addWidget(self.sensHL)
            self.windContainer.addLayout(self.windHeader)

            self.windBox = QHBoxLayout()
            self.windFrame = QFrame(self)
            self.wind_VL = QVBoxLayout(self.windFrame)
            self.windL = QLabel(fetch_wind.wind, self.windFrame)
            self.windL.setStyleSheet("background-image: url('img/wind-circle.png'); background-repeat: no-repeat; background-position: center")
            self.windL.setAlignment(Qt.AlignCenter)
            self.windL.setMinimumHeight(200)
            self.windL.setFont(QFont('Arial', 50))
            self.wind_VL.addWidget(self.windL)
            self.windBox.addWidget(self.windFrame)

            self.meanFrame = QFrame(self)
            self.mean_VL = QVBoxLayout(self.meanFrame)
            self.meanL = QLabel(str(fetch_wind.meanwind), self.meanFrame)
            self.meanL.setStyleSheet("background-image: url('img/wind-circle.png'); background-repeat: no-repeat; background-position: center")
            self.meanL.setAlignment(Qt.AlignCenter)
            self.meanL.setMinimumHeight(200)
            self.meanL.setFont(QFont('Arial', 50))
            self.mean_VL.addWidget(self.meanL)
            self.windBox.addWidget(self.meanFrame)

            self.windContainer.addLayout(self.windBox)

        except Exception as e:
            print(repr(e))

        #Bauforth box
        self.beaufortbox = QHBoxLayout()
        self.beaufortL = QLabel(str(fetch_wind.beaufortLS))
        self.beaufortL.setAlignment(Qt.AlignHCenter)
        self.beaufortL.setMinimumHeight(50)
        self.beaufortL.setFont(QFont('Arial', 20))
        self.beaufortbox.addWidget(self.beaufortL)
        self.mainContainer.addLayout(self.beaufortbox)

        #GRAPH
        self.graphContainer = QVBoxLayout()
        pg.setConfigOption('background', '#000000')
        self.graph = pg.PlotWidget()
        self.graphContainer.addWidget(self.graph)
        x = [1, 3, 6, 8, 9]
        y = [3, 6, 1, 7, 9]
        try:
            self.graph.plot(fetch_graph.graphwind_X, fetch_graph.graphwind_Y)
        except Exception as e:
            print(repr(e))

        self.windContainer.addLayout(self.graphContainer)
        self.windContainer.addStretch()
        self.mainContainer.addLayout(self.windContainer)

        #sens container
        self.sensFrame1 = QFrame(self)
        self.sensBox1 = QVBoxLayout(self.sensFrame1)

        self.sensFrame = QFrame(self)
        self.sensBox = QHBoxLayout(self.sensFrame)
        self.temp = QLabel(fetch_sens.temp + " °C")
        self.hum = QLabel(fetch_sens.hum + "%")
        self.atp = QLabel(fetch_sens.atp + " mbar")
        self.temp.setFont(QFont('Arial', 20))
        self.hum.setFont(QFont('Arial', 20))
        self.atp.setFont(QFont('Arial', 20))

        self.sensBox.addWidget(self.temp)
        self.sensBox.addWidget(self.hum)
        self.sensBox.addWidget(self.atp)
        self.sensBox1.addWidget(self.sensFrame)

        #GPS container
        self.gpsFrame = QFrame(self)
        self.gpsBox = QVBoxLayout(self.gpsFrame)
        self.latitude = QLabel("Latitude: " + fetch_gps.lat)
        self.longitude = QLabel("Longitude: " + fetch_gps.long)
        self.altitude = QLabel("Altitude: " + fetch_gps.alt)

        self.gpsBox.addWidget(self.latitude)
        self.gpsBox.addWidget(self.longitude)
        self.gpsBox.addWidget(self.altitude)
        self.sensBox1.addWidget(self.gpsFrame)

        self.mainContainer.addWidget(self.sensFrame1)

        self.O1.addLayout(self.mainContainer)

        #footer box
        self.footerbox = QHBoxLayout()
        self.credit = QLabel("Creator: Stefan Bahrawy")
        self.winddate = QLabel("W: " + str(fetch_wind.timestamp))
        self.sensdate = QLabel("S: " + str(fetch_sens.sens_timestamp))
        self.gpsdate = QLabel("G: " + str(fetch_gps.gps_timestamp))
        self.footerbox.addWidget(self.credit)
        self.footerbox.addWidget(self.winddate)
        self.footerbox.addWidget(self.sensdate)
        self.footerbox.addWidget(self.gpsdate)
        self.O1.addLayout((self.footerbox))

    def update_wind(self):
        try:
            self.windL.setText(fetch_wind.wind)
            self.meanL.setText(str(fetch_wind.meanwind))
            self.winddate.setText("W: " + str(fetch_wind.timestamp))
            self.beaufortL.setText(fetch_wind.beaufortLS)
        except Exception as e:
            print(repr(e))
        QApplication.processEvents()


    def update_sens(self):
        try:
            self.temp.setText(fetch_sens.temp + " °C")
            self.hum.setText(fetch_sens.hum + "%")
            self.atp.setText(fetch_sens.atp + " mbar")

            self.latitude.setText("Latitude: " + fetch_gps.lat)
            self.longitude.setText("Longitude: " + fetch_gps.long)
            self.altitude.setText("Altitude: " + fetch_gps.alt)

            self.graph.plot(fetch_graph.graphwind_X, fetch_graph.graphwind_Y, clear=True)

            self.sensgridtimestamp.setText("S: " + str(fetch_sens.sens_timestamp))
            self.sensgridtimestamp.setText("G: " + str(fetch_gps.gps_timestamp))

        except Exception as e:
            print(repr(e))
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()

    timer1 = QTimer()
    timer1.timeout.connect(ex.update_wind)
    timer1.start(1000)

    timer2 = QTimer()
    timer2.timeout.connect(ex.update_sens)
    timer2.start(60000)

    sys.exit(app.exec_())

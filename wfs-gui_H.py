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

sys.settrace
#test

get_wind = "SELECT * FROM wind WHERE id=(SELECT MAX(id) FROM wind)"
get_max_wind_12 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
get_max_wind_24 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
get_max_wind = "SELECT MAX(wind) FROM wind"

get_min_wind_12 = "SELECT MIN(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
get_min_wind_24 = "SELECT MIN(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"

get_mean_wind = "SELECT AVG(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 10 MINUTE)"

get_max_wind01 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 1 MINUTE)"
get_max_wind05 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 5 MINUTE)"
get_max_wind010 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 10 MINUTE)"
get_max_wind030 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 30 MINUTE)"
get_max_wind1 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)"
get_max_wind2 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 2 HOUR)"
get_max_wind4 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 4 HOUR)"
get_max_wind6 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 6 HOUR)"

get_graph_wind = "SELECT ROUND(wind, 0) FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
get_graph_wind_timestamp = "SELECT CAST(tmestmp AS CHAR) FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
get_graph_atp = "SELECT atp FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
get_graph_atp_timestamp = "SELECT CAST(tmestmp AS CHAR) FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"

get_sens = "SELECT * FROM sens WHERE id=(SELECT MAX(id) FROM sens)"
get_gps = "SELECT * FROM gps WHERE id=(SELECT MAX(id) FROM gps)"

# TEMP
get_max_temp_12 = "SELECT MAX(temp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
get_max_temp_24 = "SELECT MAX(temp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
get_max_temp = "SELECT MAX(temp) FROM sens"

get_min_temp_12 = "SELECT MIN(temp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
get_min_temp_24 = "SELECT MIN(temp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
get_min_temp = "SELECT MIN(temp) FROM sens"

# HUM
get_max_hum_12 = "SELECT MAX(hum) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
get_max_hum_24 = "SELECT MAX(hum) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
get_max_hum = "SELECT MAX(hum) FROM sens"

get_min_hum_12 = "SELECT MIN(hum) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
get_min_hum_24 = "SELECT MIN(hum) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
get_min_hum = "SELECT MIN(hum) FROM sens"

# ATP
get_max_atp_12 = "SELECT MAX(atp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
get_max_atp_24 = "SELECT MAX(atp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
get_max_atp = "SELECT MAX(atp) FROM sens"

get_min_atp_12 = "SELECT MIN(atp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
get_min_atp_24 = "SELECT MIN(atp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
get_min_atp = "SELECT MIN(atp) FROM sens"


def fetch_wind():
    while True:
        cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
        cursor = cnx.cursor(buffered=True)

        cursor.execute(get_wind)
        if cursor.rowcount > 0:
            db_wind = cursor.fetchone()
            fetch_wind.wind = str(db_wind[1])
            # wind_timestamp = str(db_wind[2])
        else:
            fetch_wind.wind = "0"

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


def fetch_sens():
    while True:
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

        time.sleep(1)
        # print(thread2.name)


def fetch_gps():
    while True:
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
            fetch_gps.lat = "0"
            fetch_gps.long = "0"
            fetch_gps.alt = "0"
            fetch_gps.gps_timestamp = "0"

        time.sleep(1)
        # print(thread3.name)


def fetch_graph():
    while True:
        cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
        cursor = cnx.cursor(buffered=True)

        cursor.execute(get_graph_wind)
        if cursor.rowcount > 0:
            db_graph_wind = cursor.fetchall()
            fetch_graph.graphwind_Y = np.ravel(db_graph_wind)
        else:
            fetch_graph.graphwind_Y = [0]

        cursor.execute(get_graph_wind_timestamp)
        if cursor.rowcount > 0:
            db_graph_timestamp = cursor.fetchall()
            print(db_graph_timestamp[0])
            for row in db_graph_timestamp:
                t = datetime.strptime(str(row), "%Y-%m-%d %H:%M:%S")
            fetch_graph.graphwind_X = t
        else:
            fetch_graph.graphwind_X = [0]

        cursor.execute(get_graph_atp)
        if cursor.rowcount > 0:
            db_graph_atp = cursor.fetchall()
            fetch_graph.graphatp_Y = np.ravel(db_graph_atp)
        else:
            fetch_graph.graphatp_Y = [0]

        cursor.execute(get_graph_atp_timestamp)
        if cursor.rowcount > 0:
            db_graph_atp_timestamp = cursor.fetchall()
            # np.ravel(db_graph_atp_timestamp)
            for row in db_graph_atp_timestamp:
                t = datetime.strptime(row, "%Y-%m-%d %H:%M:%S").date()
            fetch_graph.graphatp_X = t
        else:
            fetch_graph.graphatp_X = [0]

        time.sleep(1)
        # print(thread4.name)


def fetch_grid():
    while True:
        cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
        cursor = cnx.cursor(buffered=True)

        #   Wind History Max list
        cursor.execute(get_max_wind01)
        db_max_wind01 = cursor.fetchone()
        if db_max_wind01[0] is None:
            fetch_grid.maxwind01 = "0"
        else:
            fetch_grid.maxwind01 = str(round(db_max_wind01[0], 1))

        cursor.execute(get_max_wind05)
        db_max_wind05 = cursor.fetchone()
        if db_max_wind05[0] is None:
            fetch_grid.maxwind05 = "0"
        else:
            fetch_grid.maxwind05 = str(round(db_max_wind05[0], 1))

        cursor.execute(get_max_wind010)
        db_max_wind010 = cursor.fetchone()
        if db_max_wind010[0] is None:
            fetch_grid.maxwind010 = "0"
        else:
            fetch_grid.maxwind010 = str(round(db_max_wind010[0], 1))

        cursor.execute(get_max_wind030)
        db_max_wind030 = cursor.fetchone()
        if db_max_wind030[0] is None:
            fetch_grid.maxwind030 = "0"
        else:
            fetch_grid.maxwind030 = str(round(db_max_wind030[0], 1))

        cursor.execute(get_max_wind1)
        db_max_wind1 = cursor.fetchone()
        if db_max_wind1[0] is None:
            fetch_grid.maxwind1 = "0"
        else:
            fetch_grid.maxwind1 = str(round(db_max_wind1[0], 1))

        cursor.execute(get_max_wind2)
        db_max_wind2 = cursor.fetchone()
        if db_max_wind2[0] is None:
            fetch_grid.maxwind2 = "0"
        else:
            fetch_grid.maxwind2 = str(round(db_max_wind2[0], 1))

        cursor.execute(get_max_wind4)
        db_max_wind4 = cursor.fetchone()
        if db_max_wind4[0] is None:
            fetch_grid.maxwind4 = "0"
        else:
            fetch_grid.maxwind4 = str(round(db_max_wind4[0], 1))

        cursor.execute(get_max_wind6)
        db_max_wind6 = cursor.fetchone()
        if db_max_wind6[0] is None:
            fetch_grid.maxwind6 = "0"
        else:
            fetch_grid.maxwind6 = str(round(db_max_wind6[0], 1))

        #   MAX
        cursor.execute(get_max_temp)
        db_max_temp = cursor.fetchone()
        if db_max_temp[0] is None:
            fetch_grid.maxtemp = "0"
        else:
            fetch_grid.maxtemp = str(round(db_max_temp[0], 1))

        cursor.execute(get_max_hum)
        db_max_hum = cursor.fetchone()
        if db_max_hum[0] is None:
            fetch_grid.maxhum = "0"
        else:
            fetch_grid.maxhum = str(round(db_max_hum[0]))

        cursor.execute(get_max_atp)
        db_max_atp = cursor.fetchone()
        if db_max_atp[0] is None:
            fetch_grid.maxatp = "0"
        else:
            fetch_grid.maxatp = str(round(db_max_atp[0]))

        #   MIN
        cursor.execute(get_min_temp)
        db_min_temp = cursor.fetchone()
        if db_min_temp[0] is None:
            fetch_grid.mintemp = "0"
        else:
            fetch_grid.mintemp = str(round(db_min_temp[0], 1))

        cursor.execute(get_min_hum)
        db_min_hum = cursor.fetchone()
        if db_min_hum[0] is None:
            fetch_grid.minhum = "0"
        else:
            fetch_grid.minhum = str(round(db_min_hum[0]))

        cursor.execute(get_min_atp)
        db_min_atp = cursor.fetchone()
        if db_min_atp[0] is None:
            fetch_grid.minatp = "0"
        else:
            fetch_grid.minatp = str(round(db_min_atp[0]))

        #   MAX12
        cursor.execute(get_max_temp_12)
        db_max_temp_12 = cursor.fetchone()
        if db_max_temp_12[0] is None:
            fetch_grid.max12temp = "0"
        else:
            fetch_grid.max12temp = str(round(db_max_temp_12[0], 1))

        cursor.execute(get_max_hum_12)
        db_max_hum_12 = cursor.fetchone()
        if db_max_hum_12[0] is None:
            fetch_grid.max12hum = "0"
        else:
            fetch_grid.max12hum = str(round(db_max_hum_12[0]))

        cursor.execute(get_max_atp_12)
        db_max_atp_12 = cursor.fetchone()
        if db_max_atp_12[0] is None:
            fetch_grid.max12atp = "0"
        else:
            fetch_grid.max12atp = str(round(db_max_atp_12[0]))

        #   MIN12
        cursor.execute(get_min_temp_12)
        db_min_temp_12 = cursor.fetchone()
        if db_min_temp_12[0] is None:
            fetch_grid.min12temp = "0"
        else:
            fetch_grid.min12temp = str(round(db_min_temp_12[0], 1))

        cursor.execute(get_min_hum_12)
        db_min_hum_12 = cursor.fetchone()
        if db_min_hum_12[0] is None:
            fetch_grid.min12hum = "0"
        else:
            fetch_grid.min12hum = str(round(db_min_hum_12[0]))

        cursor.execute(get_min_atp_12)
        db_min_atp_12 = cursor.fetchone()
        if db_min_atp_12[0] is None:
            fetch_grid.min12atp = "0"
        else:
            fetch_grid.min12atp = str(round(db_min_atp_12[0]))

        #   MAX24
        cursor.execute(get_max_temp_24)
        db_max_temp_24 = cursor.fetchone()
        if db_max_temp_24[0] is None:
            fetch_grid.max24temp = "0"
        else:
            fetch_grid.max24temp = str(round(db_max_temp_24[0], 1))

        cursor.execute(get_max_hum_24)
        db_max_hum_24 = cursor.fetchone()
        if db_max_hum_24[0] is None:
            fetch_grid.max24hum = "0"
        else:
            fetch_grid.max24hum = str(round(db_max_hum_24[0]))

        cursor.execute(get_max_atp_24)
        db_max_atp_24 = cursor.fetchone()
        if db_max_atp_24[0] is None:
            fetch_grid.max24atp = "0"
        else:
            fetch_grid.max24atp = str(round(db_max_atp_24[0]))

        #   MIN24
        cursor.execute(get_min_temp_24)
        db_min_temp_24 = cursor.fetchone()
        if db_min_temp_24[0] is None:
            fetch_grid.min24temp = "0"
        else:
            fetch_grid.min24temp = str(round(db_min_temp_24[0], 1))

        cursor.execute(get_min_hum_24)
        db_min_hum_24 = cursor.fetchone()
        if db_min_hum_24[0] is None:
            fetch_grid.min24hum = "0"
        else:
            fetch_grid.min24hum = str(round(db_min_hum_24[0]))

        cursor.execute(get_min_atp_24)
        db_min_atp_24 = cursor.fetchone()
        if db_min_atp_24[0] is None:
            fetch_grid.min24atp = "0"
        else:
            fetch_grid.min24atp = str(round(db_min_atp_24[0]))

        time.sleep(1)
        # print(thread5.name)

# print("Thread Running")
# data = fetch_wind()


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

thread5 = threading.Thread(target=fetch_grid, args=())
thread5.daemon = True
thread5.start()


class App(QWidget):

    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)
        self.title = "WFS - Weather Forecast Station"
        self.setWindowIcon(QIcon("drawing.svg.png"))
        self.left = 0
        self.top = 0
        self.width = 720
        self.height = 480
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("color: white; background-color: #152025;")
        self.initUI()

        self.win = QWidget()

    def initUI(self):

        self.mainContainer = QVBoxLayout(self)

        self.windHeader = QHBoxLayout()
        self.windHL = QLabel("WIND")
        self.windHL.setFont(QFont('Arial', 20))
        self.windHL.setAlignment(Qt.AlignCenter)
        self.windHeader.addWidget(self.windHL)
        self.meanHL = QLabel("MEAN")
        self.meanHL.setFont(QFont('Arial', 20))
        self.meanHL.setAlignment(Qt.AlignCenter)
        self.windHeader.addWidget(self.meanHL)
        self.mainContainer.addLayout(self.windHeader)

        self.windContainer = QHBoxLayout()
        self.windFrame = QFrame(self)
        self.wind_VL = QVBoxLayout(self.windFrame)
        self.windL = QLabel(fetch_wind.wind, self.windFrame)
        self.windL.setStyleSheet("background-image: url('wind-circle.png'); background-repeat: no-repeat;")
        self.windL.setAlignment(Qt.AlignCenter)
        self.windL.setMinimumHeight(200)
        self.windL.setFont(QFont('Arial', 50))
        self.wind_VL.addWidget(self.windL)
        self.windContainer.addWidget(self.windFrame)

        self.meanFrame = QFrame(self)
        self.mean_VL = QVBoxLayout(self.meanFrame)
        self.meanL = QLabel(str(fetch_wind.meanwind), self.meanFrame)
        self.meanL.setStyleSheet("background-image: url('wind-circle.png'); background-repeat: no-repeat;")
        self.meanL.setAlignment(Qt.AlignCenter)
        self.meanL.setMinimumHeight(200)
        self.meanL.setFont(QFont('Arial', 50))
        self.mean_VL.addWidget(self.meanL)
        self.windContainer.addWidget(self.meanFrame)

        self.mainContainer.addLayout(self.windContainer)

        self.beaufortbox = QHBoxLayout()
        self.beaufortL = QLabel(str(fetch_wind.beaufortLS))
        self.beaufortL.setAlignment(Qt.AlignHCenter)
        self.beaufortL.setMinimumHeight(50)
        self.beaufortL.setFont(QFont('Arial', 20))
        self.beaufortbox.addWidget(self.beaufortL)
        self.mainContainer.addLayout(self.beaufortbox)


        self.windHistoryContainer = QVBoxLayout()
        self.windHistoryHeader = QHBoxLayout()
        self.windHHLS = "Max Wind History:"
        self.windHHL = QLabel(self.windHHLS)
        self.windHHL.setFont(QFont('Arial', 15))
        self.windHistoryHeader.addWidget(self.windHHL)
        self.windHistoryContainer.addLayout(self.windHistoryHeader)

        self.windHG = QGridLayout()
        self.windHG.addWidget(QLabel("1min"), 0, 0)
        self.windHG.addWidget(QLabel("5min"), 0, 1)
        self.windHG.addWidget(QLabel("10min"), 0, 2)
        self.windHG.addWidget(QLabel("30min"), 0, 3)
        self.windHG.addWidget(QLabel("1hr"), 0, 4)
        self.windHG.addWidget(QLabel("2hr"), 0, 5)
        self.windHG.addWidget(QLabel("4hr"), 0, 6)
        self.windHG.addWidget(QLabel("6hr"), 0, 7)


        self.windmax01 = QLabel(fetch_grid.maxwind01)
        self.windmax01.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax01, 1, 0)

        self.windmax05 = QLabel(fetch_grid.maxwind05)
        self.windmax05.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax05, 1, 1)

        self.windmax010 = QLabel(fetch_grid.maxwind010)
        self.windmax010.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax010, 1, 2)

        self.windmax030 = QLabel(fetch_grid.maxwind030)
        self.windmax030.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax030, 1, 3)

        self.windmax1 = QLabel(fetch_grid.maxwind1)
        self.windmax1.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax1, 1, 4)

        self.windmax2 = QLabel(fetch_grid.maxwind2)
        self.windmax2.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax2, 1, 5)

        self.windmax4 = QLabel(fetch_grid.maxwind4)
        self.windmax4.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax4, 1, 6)

        self.windmax6 = QLabel(fetch_grid.maxwind6)
        self.windmax6.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax6, 1, 7)

        self.windHistoryContainer.addLayout(self.windHG)
        self.mainContainer.addLayout(self.windHistoryContainer)


        self.graphContainer = QVBoxLayout()
        pg.setConfigOption('background', '#152025')
        self.graph = pg.PlotWidget()
        self.graphContainer.addWidget(self.graph)
        x = [1, 3, 6, 8, 9]
        y = [3, 6, 1, 7, 9]
        self.graph.plot(fetch_graph.graphwind_X, fetch_graph.graphwind_Y)
        self.graph.plot(fetch_graph.graphatp_X, fetch_graph.graphatp_Y)
        self.mainContainer.addLayout(self.graphContainer)

        self.sensContainer = QVBoxLayout()
        self.sensContainer.setSpacing(0)
        self.sensFrame = QFrame(self)
        self.sensgrid = QGridLayout(self.sensFrame)

        self.sensgrid.addWidget(QLabel("Temp (°C)"), 0, 1)
        self.sensgrid.addWidget(QLabel("Humid (%)"), 0, 2)
        self.sensgrid.addWidget(QLabel("ATP (mBar)"), 0, 3)

        self.sensgrid.addWidget(QLabel("Current"), 1, 0)
        self.sensgrid.addWidget(QLabel("Max 12hrs"), 2, 0)
        self.sensgrid.addWidget(QLabel("Min 12hrs"), 3, 0)
        self.sensgrid.addWidget(QLabel("Max 24hrs"), 4, 0)
        self.sensgrid.addWidget(QLabel("Min 24hrs"), 5, 0)
        self.sensgrid.addWidget(QLabel("Max all time"), 6, 0)
        self.sensgrid.addWidget(QLabel("Min all time"), 7, 0)

        self.tempL = QLabel(fetch_sens.temp)
        self.sensgrid.addWidget(self.tempL, 1, 1)
        self.humL = QLabel(fetch_sens.hum)
        self.sensgrid.addWidget(self.humL, 1, 2)
        self.atpL = QLabel(fetch_sens.atp)
        self.sensgrid.addWidget(self.atpL, 1, 3)

        self.max12tempL = QLabel(fetch_grid.max12temp)
        self.sensgrid.addWidget(self.max12tempL, 2, 1)
        self.max12humL = QLabel(fetch_grid.max12hum)
        self.sensgrid.addWidget(self.max12humL, 2, 2)
        self.max12atpL = QLabel(fetch_grid.max12atp)
        self.sensgrid.addWidget(self.max12atpL, 2, 3)

        self.min12tempL = QLabel(fetch_grid.min12temp)
        self.sensgrid.addWidget(self.min12tempL, 3, 1)
        self.min12humL = QLabel(fetch_grid.min12hum)
        self.sensgrid.addWidget(self.min12humL, 3, 2)
        self.min12atpL = QLabel(fetch_grid.min12atp)
        self.sensgrid.addWidget(self.min12atpL, 3, 3)

        self.max24tempL = QLabel(fetch_grid.max24temp)
        self.sensgrid.addWidget(self.max24tempL, 4, 1)
        self.max24humL = QLabel(fetch_grid.max24hum)
        self.sensgrid.addWidget(self.max24humL, 4, 2)
        self.max24atpL = QLabel(fetch_grid.max24atp)
        self.sensgrid.addWidget(self.max24atpL, 4, 3)

        self.min24tempL = QLabel(fetch_grid.min24temp)
        self.sensgrid.addWidget(self.min24tempL, 5, 1)
        self.min24humL = QLabel(fetch_grid.min24hum)
        self.sensgrid.addWidget(self.min24humL, 5, 2)
        self.min24atpL = QLabel(fetch_grid.min24atp)
        self.sensgrid.addWidget(self.min24atpL, 5, 3)

        self.maxtempL = QLabel(fetch_grid.maxtemp)
        self.sensgrid.addWidget(self.maxtempL, 6, 1)
        self.maxhumL = QLabel(fetch_grid.maxhum)
        self.sensgrid.addWidget(self.maxhumL, 6, 2)
        self.maxatpL = QLabel(fetch_grid.maxatp)
        self.sensgrid.addWidget(self.maxatpL, 6, 3)

        self.mintempL = QLabel(fetch_grid.mintemp)
        self.sensgrid.addWidget(self.mintempL, 7, 1)
        self.minhumL = QLabel(fetch_grid.minhum)
        self.sensgrid.addWidget(self.minhumL, 7, 2)
        self.minatpL = QLabel(fetch_grid.minatp)
        self.sensgrid.addWidget(self.minatpL, 7, 3)

        self.sensContainer.addWidget(self.sensFrame)
        self.mainContainer.addLayout(self.sensContainer)
        self.mainContainer.addStretch()

    def update_label(self):
        try:
            self.windL.setText(fetch_wind.wind)
            self.meanL.setText(str(fetch_wind.meanwind))

            self.beaufortL.setText(fetch_wind.beaufortLS)

            self.tempL.setText(fetch_sens.temp)
            self.humL.setText(fetch_sens.hum)
            self.atpL.setText(fetch_sens.atp)

            self.graph.plot(fetch_graph.graphwind_X, fetch_graph.graphwind_Y, clear=True)
            self.graph.plot(fetch_graph.graphatp_X, fetch_graph.graphatp_Y)

            self.max12tempL.setText(fetch_grid.max12temp)
            self.max12humL.setText(fetch_grid.max12hum)
            self.max12atpL.setText(fetch_grid.max12atp)

            self.min12tempL.setText(fetch_grid.min12temp)
            self.min12humL.setText(fetch_grid.min12hum)
            self.min12atpL.setText(fetch_grid.min12atp)

            self.max24tempL.setText(fetch_grid.max24temp)
            self.max24humL.setText(fetch_grid.max24hum)
            self.max24atpL.setText(fetch_grid.max24atp)

            self.min24tempL.setText(fetch_grid.min24temp)
            self.min24humL.setText(fetch_grid.min24hum)
            self.min24atpL.setText(fetch_grid.min24atp)

            self.maxtempL.setText(fetch_grid.maxtemp)
            self.maxhumL.setText(fetch_grid.maxhum)
            self.maxatpL.setText(fetch_grid.maxatp)

            self.mintempL.setText(fetch_grid.mintemp)
            self.minhumL.setText(fetch_grid.minhum)
            self.minatpL.setText(fetch_grid.minatp)

            self.windmax01.setText(fetch_grid.maxwind01)
            self.windmax05.setText(fetch_grid.maxwind05)
            self.windmax010.setText(fetch_grid.maxwind010)
            self.windmax030.setText(fetch_grid.maxwind030)
            self.windmax1.setText(fetch_grid.maxwind1)
            self.windmax2.setText(fetch_grid.maxwind2)
            self.windmax4.setText(fetch_grid.maxwind4)
            self.windmax6.setText(fetch_grid.maxwind6)
        except Exception as e:
            print(repr(e))
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()

    timer = QTimer()
    timer.timeout.connect(ex.update_label)
    timer.start(1000)

    sys.exit(app.exec_())

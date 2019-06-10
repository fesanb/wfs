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

# GRAPH
get_graph_wind = "SELECT ROUND(wind, 0) FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
get_graph_wind_id = "SELECT id FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
get_graph_wind_timestamp = "SELECT CAST(tmestmp AS CHAR) FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
get_graph_atp = "SELECT atp FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
get_graph_atp_id = "SELECT id FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
get_graph_atp_timestamp = "SELECT CAST(tmestmp AS CHAR) FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"

get_sens = "SELECT * FROM sens WHERE id=(SELECT MAX(id) FROM sens)"
get_gps = "SELECT * FROM gps WHERE id=(SELECT MAX(id) FROM gps)"

# TEMP
get_max_temp_30 = "SELECT MAX(temp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 30 MINUTE)"
get_max_temp_60 = "SELECT MAX(temp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)"
get_max_temp_120 = "SELECT MAX(temp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 2 HOUR)"
get_max_temp = "SELECT MAX(temp) FROM sens"

# HUM
get_max_hum_30 = "SELECT MAX(hum) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 30 MINUTE)"
get_max_hum_60 = "SELECT MAX(hum) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)"
get_max_hum_120 = "SELECT MAX(hum) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 2 HOUR)"
get_max_hum = "SELECT MAX(hum) FROM sens"

# ATP
get_max_atp_30 = "SELECT MAX(atp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 30 MINUTE)"
get_max_atp_60 = "SELECT MAX(atp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)"
get_max_atp_120 = "SELECT MAX(atp) FROM sens  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 2 HOUR)"
get_max_atp = "SELECT MAX(atp) FROM sens"

def fetch_wind():
    while True:
        try:
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
                
            # #   MAX
            # cursor.execute(get_max_temp)
            # db_max_temp = cursor.fetchone()
            # if db_max_temp[0] is None:
            #     fetch_sens.maxtemp = "0"
            # else:
            #     fetch_sens.maxtemp = str(round(db_max_temp[0], 1))
            #
            # cursor.execute(get_max_hum)
            # db_max_hum = cursor.fetchone()
            # if db_max_hum[0] is None:
            #     fetch_sens.maxhum = "0"
            # else:
            #     fetch_sens.maxhum = str(round(db_max_hum[0]))
            #
            # cursor.execute(get_max_atp)
            # db_max_atp = cursor.fetchone()
            # if db_max_atp[0] is None:
            #     fetch_sens.maxatp = "0"
            # else:
            #     fetch_sens.maxatp = str(round(db_max_atp[0]))

            #   SENS 30
            cursor.execute(get_max_temp_30)
            db_max_temp_30 = cursor.fetchone()
            if db_max_temp_30[0] is None:
                fetch_sens.max30temp = "0"
            else:
                fetch_sens.max30temp = str(round(db_max_temp_30[0], 1))

            cursor.execute(get_max_hum_30)
            db_max_hum_30 = cursor.fetchone()
            if db_max_hum_30[0] is None:
                fetch_sens.max30hum = "0"
            else:
                fetch_sens.max30hum = str(round(db_max_hum_30[0]))

            cursor.execute(get_max_atp_30)
            db_max_atp_30 = cursor.fetchone()
            if db_max_atp_30[0] is None:
                fetch_sens.max30atp = "0"
            else:
                fetch_sens.max30atp = str(round(db_max_atp_30[0]))

            #   SENS 60
            cursor.execute(get_max_temp_60)
            db_max_temp_60 = cursor.fetchone()
            if db_max_temp_60[0] is None:
                fetch_sens.max60temp = "0"
            else:
                fetch_sens.max60temp = str(round(db_max_temp_60[0], 1))

            cursor.execute(get_max_hum_60)
            db_max_hum_60 = cursor.fetchone()
            if db_max_hum_60[0] is None:
                fetch_sens.max60hum = "0"
            else:
                fetch_sens.max60hum = str(round(db_max_hum_60[0]))

            cursor.execute(get_max_atp_60)
            db_max_atp_60 = cursor.fetchone()
            if db_max_atp_60[0] is None:
                fetch_sens.max60atp = "0"
            else:
                fetch_sens.max60atp = str(round(db_max_atp_60[0]))

            #   SENS 120
            cursor.execute(get_max_temp_120)
            db_max_temp_120 = cursor.fetchone()
            if db_max_temp_120[0] is None:
                fetch_sens.max120temp = "0"
            else:
                fetch_sens.max120temp = str(round(db_max_temp_120[0], 1))

            cursor.execute(get_max_hum_120)
            db_max_hum_120 = cursor.fetchone()
            if db_max_hum_120[0] is None:
                fetch_sens.max120hum = "0"
            else:
                fetch_sens.max120hum = str(round(db_max_hum_120[0]))

            cursor.execute(get_max_atp_120)
            db_max_atp_120 = cursor.fetchone()
            if db_max_atp_120[0] is None:
                fetch_sens.max120atp = "0"
            else:
                fetch_sens.max120atp = str(round(db_max_atp_120[0]))

            time.sleep(1)
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
                fetch_gps.lat = "0"
                fetch_gps.long = "0"
                fetch_gps.alt = "0"
                fetch_gps.gps_timestamp = "0"

            time.sleep(1)
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
                fetch_graph.graphwind_Y = np.ravel(db_graph_wind)
            else:
                fetch_graph.graphwind_Y = [0]

            cursor.execute(get_graph_wind_id)
            if cursor.rowcount > 0:
                db_graph_id = cursor.fetchall()
                fetch_graph.graphwind_X = np.ravel(db_graph_id)
            else:
                fetch_graph.graphwind_X = [0]

            cursor.execute(get_graph_atp)
            if cursor.rowcount > 0:
                db_graph_atp = cursor.fetchall()
                fetch_graph.graphatp_Y = np.ravel(db_graph_atp)
            else:
                fetch_graph.graphatp_Y = [0]

            cursor.execute(get_graph_atp_id)
            if cursor.rowcount > 0:
                db_graph_atp_id = cursor.fetchall()
                fetch_graph.graphatp_X = np.ravel(db_graph_atp_id)
            else:
                fetch_graph.graphatp_X = [0]

            time.sleep(1)
            # print(thread4.name)
        except Exception as e:
            print(repr(e))


# def fetch_grid():
#     while True:
#         try:
#             cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
#             cursor = cnx.cursor(buffered=True)
#
#             #   Wind History Max list
#             cursor.execute(get_max_wind01)
#             db_max_wind01 = cursor.fetchone()
#             if db_max_wind01[0] is None:
#                 fetch_grid.maxwind01 = "0"
#             else:
#                 fetch_grid.maxwind01 = str(round(db_max_wind01[0], 1))
#
#             cursor.execute(get_max_wind05)
#             db_max_wind05 = cursor.fetchone()
#             if db_max_wind05[0] is None:
#                 fetch_grid.maxwind05 = "0"
#             else:
#                 fetch_grid.maxwind05 = str(round(db_max_wind05[0], 1))
#
#             cursor.execute(get_max_wind010)
#             db_max_wind010 = cursor.fetchone()
#             if db_max_wind010[0] is None:
#                 fetch_grid.maxwind010 = "0"
#             else:
#                 fetch_grid.maxwind010 = str(round(db_max_wind010[0], 1))
#
#             cursor.execute(get_max_wind030)
#             db_max_wind030 = cursor.fetchone()
#             if db_max_wind030[0] is None:
#                 fetch_grid.maxwind030 = "0"
#             else:
#                 fetch_grid.maxwind030 = str(round(db_max_wind030[0], 1))
#
#             cursor.execute(get_max_wind1)
#             db_max_wind1 = cursor.fetchone()
#             if db_max_wind1[0] is None:
#                 fetch_grid.maxwind1 = "0"
#             else:
#                 fetch_grid.maxwind1 = str(round(db_max_wind1[0], 1))
#
#             cursor.execute(get_max_wind2)
#             db_max_wind2 = cursor.fetchone()
#             if db_max_wind2[0] is None:
#                 fetch_grid.maxwind2 = "0"
#             else:
#                 fetch_grid.maxwind2 = str(round(db_max_wind2[0], 1))
#
#             cursor.execute(get_max_wind4)
#             db_max_wind4 = cursor.fetchone()
#             if db_max_wind4[0] is None:
#                 fetch_grid.maxwind4 = "0"
#             else:
#                 fetch_grid.maxwind4 = str(round(db_max_wind4[0], 1))
#
#             cursor.execute(get_max_wind6)
#             db_max_wind6 = cursor.fetchone()
#             if db_max_wind6[0] is None:
#                 fetch_grid.maxwind6 = "0"
#             else:
#                 fetch_grid.maxwind6 = str(round(db_max_wind6[0], 1))
#
#             time.sleep(1)
#             # print(thread5.name)
#         except Exception as e:
#             print(repr(e))


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

# thread5 = threading.Thread(target=fetch_grid, args=())
# thread5.daemon = True
# thread5.start()


class App(QWidget):

    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)
        self.title = "WFS - Weather Forecast Station"
        self.setWindowIcon(QIcon("drawing.svg.png"))
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
        self.sensHL = QLabel("SENSOR")
        self.sensHL.setFont(QFont('Arial', 20))
        self.sensHL.setAlignment(Qt.AlignCenter)
        self.windHeader.addWidget(self.sensHL)
        self.mainContainer.addLayout(self.windHeader)

        self.windContainer = QHBoxLayout()
        self.windFrame = QFrame(self)
        self.wind_VL = QVBoxLayout(self.windFrame)
        self.windL = QLabel(fetch_wind.wind, self.windFrame)
        self.windL.setStyleSheet("background-image: url('img/wind-circle.png'); background-repeat: no-repeat; background-position: center")
        self.windL.setAlignment(Qt.AlignCenter)
        self.windL.setMinimumHeight(200)
        self.windL.setFont(QFont('Arial', 50))
        self.wind_VL.addWidget(self.windL)
        self.windContainer.addWidget(self.windFrame)

        self.meanFrame = QFrame(self)
        self.mean_VL = QVBoxLayout(self.meanFrame)
        self.meanL = QLabel(str(fetch_wind.meanwind), self.meanFrame)
        self.meanL.setStyleSheet("background-image: url('img/wind-circle.png'); background-repeat: no-repeat; background-position: center")
        self.meanL.setAlignment(Qt.AlignCenter)
        self.meanL.setMinimumHeight(200)
        self.meanL.setFont(QFont('Arial', 50))
        self.mean_VL.addWidget(self.meanL)
        self.windContainer.addWidget(self.meanFrame)

        #
        self.sensFrame2 = QFrame(self)
        self.sensDataContainer = QVBoxLayout(self.sensFrame2)

        self.sensorG = QGridLayout()

        self.sensorG.addWidget(QLabel("NOW"), 0, 1)
        self.sensorG.addWidget(QLabel("30min"), 0, 2)
        self.sensorG.addWidget(QLabel("1hr"), 0, 3)
        self.sensorG.addWidget(QLabel("2hr"), 0, 4)

        self.sensorG.addWidget(QLabel("Temp: "), 1, 0)
        self.sensorG.addWidget(QLabel("Hum: "), 2, 0)
        self.sensorG.addWidget(QLabel("ATP: "), 3, 0)

        try:
            self.sensdataT = QLabel(fetch_sens.temp)
            # self.sensdataT.setAlignment(Qt.AlignHCenter)
            self.sensorG.addWidget(self.sensdataT, 1, 1)

            self.sensdataH = QLabel(fetch_sens.hum)
            self.sensorG.addWidget(self.sensdataH, 2, 1)

            self.sensdataA = QLabel(fetch_sens.atp)
            self.sensorG.addWidget(self.sensdataA, 3, 1)

            self.sensgridTemp30 = QLabel(fetch_sens.max30temp)
            self.sensorG.addWidget(self.sensgridTemp30, 1, 2)

            self.sensgridTemp60 = QLabel(fetch_sens.max60temp)
            self.sensorG.addWidget(self.sensgridTemp60, 1, 3)

            self.sensgridTemp120 = QLabel(fetch_sens.max120temp)
            self.sensorG.addWidget(self.sensgridTemp120, 1, 4)

            self.sensgridHum30 = QLabel(fetch_sens.max30hum)
            self.sensorG.addWidget(self.sensgridHum30, 2, 2)

            self.sensgridHum60 = QLabel(fetch_sens.max60hum)
            self.sensorG.addWidget(self.sensgridHum60, 2, 3)

            self.sensgridHum120 = QLabel(fetch_sens.max120hum)
            self.sensorG.addWidget(self.sensgridHum120, 2, 4)

            self.sensgridatp30 = QLabel(fetch_sens.max30atp)
            self.sensorG.addWidget(self.sensgridatp30, 3, 2)

            self.sensgridatp60 = QLabel(fetch_sens.max60atp)
            self.sensorG.addWidget(self.sensgridatp60, 3, 3)

            self.sensgridatp120 = QLabel(fetch_sens.max120atp)
            self.sensorG.addWidget(self.sensgridatp120, 3, 4)

            self.sensgridtimestamp = QLabel(fetch_sens.sens_timestamp)
            self.sensorG.addWidget(self.sensgridtimestamp, 4, 0)

            gps = "Lat: " + fetch_gps.lat + " Lon: " + fetch_gps.long + " Alt: " + fetch_gps.alt + " Time: " + fetch_gps.gps_timestamp
            self.sensgridgps = QLabel(gps)
            self.sensorG.addWidget(self.sensgridgps, 5, 0)

        except Exception as e:
            print(repr(e))

        self.sensDataContainer.addLayout(self.sensorG)
        self.windContainer.addWidget(self.sensFrame2)
        self.mainContainer.addLayout(self.windContainer)

        #Bauforth box
        self.beaufortbox = QHBoxLayout()
        self.beaufortL = QLabel(str(fetch_wind.beaufortLS))
        self.beaufortL.setAlignment(Qt.AlignHCenter)
        self.beaufortL.setMinimumHeight(50)
        self.beaufortL.setFont(QFont('Arial', 20))
        self.beaufortbox.addWidget(self.beaufortL)
        self.mainContainer.addLayout(self.beaufortbox)

        #Wind grid box
        # self.windHistoryContainer = QVBoxLayout()
        # self.windHistoryHeader = QHBoxLayout()
        # self.windHHLS = "Max Wind History:"
        # self.windHHL = QLabel(self.windHHLS)
        # self.windHHL.setFont(QFont('Arial', 15))
        # self.windHistoryHeader.addWidget(self.windHHL)
        # self.windHistoryContainer.addLayout(self.windHistoryHeader)
        #
        # self.windHG = QGridLayout()
        # self.windHG.addWidget(QLabel("1min"), 0, 0)
        # self.windHG.addWidget(QLabel("5min"), 0, 1)
        # self.windHG.addWidget(QLabel("10min"), 0, 2)
        # self.windHG.addWidget(QLabel("30min"), 0, 3)
        # self.windHG.addWidget(QLabel("1hr"), 0, 4)
        # self.windHG.addWidget(QLabel("2hr"), 0, 5)
        # self.windHG.addWidget(QLabel("4hr"), 0, 6)
        # self.windHG.addWidget(QLabel("6hr"), 0, 7)
        #
        # try:
        #     self.windmax01 = QLabel(fetch_grid.maxwind01)
        #     self.windmax01.setAlignment(Qt.AlignHCenter)
        #     self.windHG.addWidget(self.windmax01, 1, 0)
        #
        #     self.windmax05 = QLabel(fetch_grid.maxwind05)
        #     self.windmax05.setAlignment(Qt.AlignHCenter)
        #     self.windHG.addWidget(self.windmax05, 1, 1)
        #
        #     self.windmax010 = QLabel(fetch_grid.maxwind010)
        #     self.windmax010.setAlignment(Qt.AlignHCenter)
        #     self.windHG.addWidget(self.windmax010, 1, 2)
        #
        #     self.windmax030 = QLabel(fetch_grid.maxwind030)
        #     self.windmax030.setAlignment(Qt.AlignHCenter)
        #     self.windHG.addWidget(self.windmax030, 1, 3)
        #
        #     self.windmax1 = QLabel(fetch_grid.maxwind1)
        #     self.windmax1.setAlignment(Qt.AlignHCenter)
        #     self.windHG.addWidget(self.windmax1, 1, 4)
        #
        #     self.windmax2 = QLabel(fetch_grid.maxwind2)
        #     self.windmax2.setAlignment(Qt.AlignHCenter)
        #     self.windHG.addWidget(self.windmax2, 1, 5)
        #
        #     self.windmax4 = QLabel(fetch_grid.maxwind4)
        #     self.windmax4.setAlignment(Qt.AlignHCenter)
        #     self.windHG.addWidget(self.windmax4, 1, 6)
        #
        #     self.windmax6 = QLabel(fetch_grid.maxwind6)
        #     self.windmax6.setAlignment(Qt.AlignHCenter)
        #     self.windHG.addWidget(self.windmax6, 1, 7)
        #
        # except Exception as e:
        #     print(repr(e))
        #
        # self.windHistoryContainer.addLayout(self.windHG)
        # self.mainContainer.addLayout(self.windHistoryContainer)

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
        # self.graph.plot(fetch_graph.graphatp_X, fetch_graph.graphatp_Y)
        self.mainContainer.addLayout(self.graphContainer)
        self.mainContainer.addStretch()

    def update_label(self):
        try:
            self.windL.setText(fetch_wind.wind)
            self.meanL.setText(str(fetch_wind.meanwind))

            self.beaufortL.setText(fetch_wind.beaufortLS)

            self.sensdataT.setText(fetch_sens.temp)
            self.sensdataH.setText(fetch_sens.hum)
            self.sensdataA.setText(fetch_sens.atp)

            self.graph.plot(fetch_graph.graphwind_X, fetch_graph.graphwind_Y, clear=True)
            # self.graph.plot(fetch_graph.graphatp_X, fetch_graph.graphatp_Y)

            # self.windmax01.setText(fetch_grid.maxwind01)
            # self.windmax05.setText(fetch_grid.maxwind05)
            # self.windmax010.setText(fetch_grid.maxwind010)
            # self.windmax030.setText(fetch_grid.maxwind030)
            # self.windmax1.setText(fetch_grid.maxwind1)
            # self.windmax2.setText(fetch_grid.maxwind2)
            # self.windmax4.setText(fetch_grid.maxwind4)
            # self.windmax6.setText(fetch_grid.maxwind6)

            self.sensdataT.setText(fetch_sens.temp)
            self.sensdataH.setText(fetch_sens.hum)
            self.sensdataA.setText(fetch_sens.atp)
            self.sensgridTemp30.setText(fetch_sens.max30temp)
            self.sensgridTemp60.setText(fetch_sens.max60temp)
            self.sensgridTemp120.setText(fetch_sens.max120temp)
            self.sensgridHum30.setText(fetch_sens.max30hum)
            self.sensgridHum60.setText(fetch_sens.max60hum)
            self.sensgridHum120.setText(fetch_sens.max120hum)
            self.sensgridatp30.setText(fetch_sens.max30atp)
            self.sensgridatp60.setText(fetch_sens.max60atp)
            self.sensgridatp120.setText(fetch_sens.max120atp)
            self.sensgridtimestamp.setText(fetch_sens.sens_timestamp)
            self.sensgridgps.setText("Lat: " + fetch_gps.lat + " Lon: " + fetch_gps.long + " Alt: " + fetch_gps.alt + " Time: " + fetch_gps.gps_timestamp)

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

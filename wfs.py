# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import sys, os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import pyqtgraph as pg
import mysql.connector
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
#custom imports
from wfs_sub_graph import *
from wfs_error_handling import error_handle
from wfs_forecast import *



#Wind
get_wind = "SELECT * FROM wind WHERE id=(SELECT MAX(id) FROM wind)"
get_mean_wind = "SELECT AVG(mean) FROM mean  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 10 MINUTE)"

# GRAPH
interval = 5500
get_graph_wind = "SELECT mean, UNIX_TIMESTAMP(tmestmp) FROM mean WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL {} HOUR)".format(interval)
get_graph_atp = "SELECT atp, UNIX_TIMESTAMP(tmestmp) FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL {} HOUR)".format(interval)
get_graph_hum = "SELECT hum, UNIX_TIMESTAMP(tmestmp) FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL {} HOUR)".format(interval)
get_graph_temp = "SELECT temp, UNIX_TIMESTAMP(tmestmp) FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL {} HOUR)".format(interval)


#SENS
get_sens = "SELECT * FROM sens WHERE id=(SELECT MAX(id) FROM sens) AND tmestmp >= DATE_SUB(NOW(), INTERVAL 5 MINUTE)"
get_gps = "SELECT * FROM gps WHERE id=(SELECT MAX(id) FROM gps) AND tmestmp >= DATE_SUB(NOW(), INTERVAL 65 MINUTE)"

#Max
get_max_wind12 = "SELECT MAX(wind) FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
get_max_wind1 = "SELECT MAX(wind) FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)"

global gbp
gbp = 0

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

            if fetch_wind.timestamp < datetime.now() - timedelta(minutes=0.25):
                fetch_wind.wind = "-.-"

            time.sleep(0.9 )
        except Exception as e:
            filename = Path(__file__).name
            error_handle(e, filename)

def make_mean():
    while True:
        try:
            cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
            cursor = cnx.cursor(buffered=True)

            cursor.execute("SELECT AVG(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 1 MINUTE)")
            db_mean_wind_1min = cursor.fetchone()
            if db_mean_wind_1min[0] is None:
                pass
            else:
                add_mean = (u'''INSERT INTO mean(mean) VALUES (%s)''' % (round(db_mean_wind_1min[0],2)))
                cursor.execute(add_mean)
                emp_no = cursor.lastrowid
                cnx.commit()
        except Exception as e:
            filename = Path(__file__).name
            error_handle(e, filename)

        time.sleep(60)

def fetch_mean():
    while True:
        try:
            cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
            cursor = cnx.cursor(buffered=True)

            cursor.execute(get_mean_wind)
            db_mean_wind = cursor.fetchone()
            if db_mean_wind[0] is None:  # cursor.rowcount is 0 and
                fetch_mean.meanwind = 0
            else:
                fetch_mean.meanwind = round(float(db_mean_wind[0]), 1)

            if float(fetch_mean.meanwind) < 0.3:
                fetch_mean.beaufortLS = "Beaufort 0 - Calm"
            elif float(fetch_mean.meanwind) > 32.7:
                fetch_mean.beaufortLS = "Beaufort 12 - Hurricane"
            elif float(fetch_mean.meanwind) > 28.5:
                fetch_mean.beaufortLS = "Beaufort 11 - Violent Storm"
            elif float(fetch_mean.meanwind) > 24.5:
                fetch_mean.beaufortLS = "Beaufort 10 - Storm"
            elif float(fetch_mean.meanwind) > 20.8:
                fetch_mean.beaufortLS = "Beaufort 9 - Strong Gale"
            elif float(fetch_mean.meanwind) > 17.2:
                fetch_mean.beaufortLS = "Beaufort 8 - Fresh Gale"
            elif float(fetch_mean.meanwind) > 13.9:
                fetch_mean.beaufortLS = "Beaufort 7 - Moderate gale"
            elif float(fetch_mean.meanwind) > 10.8:
                fetch_mean.beaufortLS = "Beaufort 6 - Strong breeze"
            elif float(fetch_mean.meanwind) > 8.0:
                fetch_mean.beaufortLS = "Beaufort 5 - Fresh breeze"
            elif float(fetch_mean.meanwind) > 5.5:
                fetch_mean.beaufortLS = "Beaufort 4 - Moderate breeze"
            elif float(fetch_mean.meanwind) > 3.4:
                fetch_mean.beaufortLS = "Beaufort 3 - Gentle breeze"
            elif float(fetch_mean.meanwind) > 1.6:
                fetch_mean.beaufortLS = "Beaufort 2 - Light breeze"
            elif float(fetch_mean.meanwind) > 0.3:
                fetch_mean.beaufortLS = "Beaufort 1 - Light Air"

        except Exception as e:
            filename = Path(__file__).name
            error_handle(e, filename)

        time.sleep(5)

def fetch_sens():
    try:
        cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
        cursor = cnx.cursor(buffered=True)

        cursor.execute(get_sens)
        if cursor.rowcount > 0:
            db_sens = cursor.fetchone()
            fetch_sens.temp = str(db_sens[1])
            fetch_sens.hum = str(db_sens[2])
            fetch_sens.atp = str(db_sens[3])
            fetch_sens.sens_timestamp = str(db_sens[5])
            fetch_sens.current_sens = []
            for i in db_sens:
                fetch_sens.current_sens.append(i)


        else:
            fetch_sens.temp = "0"
            fetch_sens.hum = "0"
            fetch_sens.atp = "0"
            fetch_sens.sens_timestamp = "0"
            fetch_sens.current_sens = []

    except Exception as e:
        filename = Path(__file__).name
        error_handle(e, filename)

def fetch_gps():
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

    except Exception as e:
        filename = Path(__file__).name
        error_handle(e, filename)

def fetch_graph():
    print("fetch graph")
    try:
        cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
        cursor = cnx.cursor(buffered=True)
        
        # wind
        cursor.execute(get_graph_wind)
        if cursor.rowcount > 0:
            db_graph_wind = cursor.fetchall()
            fetch_graph.wind_graph_X = []
            fetch_graph.wind_graph_Y = []

            for i in db_graph_wind:
                fetch_graph.wind_graph_X.append(i[1])
                fetch_graph.wind_graph_Y.append(i[0])

        else:
            fetch_graph.wind_graph_X = []
            fetch_graph.wind_graph_Y = []
            fetch_graph.wind_graph_X.append(time.time())
            fetch_graph.wind_graph_Y.append(0)
        
        # atp 
        cursor.execute(get_graph_atp)
        if cursor.rowcount > 0:
            db_graph_atp = cursor.fetchall()
            fetch_graph.atp_graph_X = []
            fetch_graph.atp_graph_Y = []

            for i in db_graph_atp:
                fetch_graph.atp_graph_X.append(i[1])
                fetch_graph.atp_graph_Y.append(i[0])

        else:
            fetch_graph.atp_graph_X = []
            fetch_graph.atp_graph_Y = []
            fetch_graph.atp_graph_X.append(time.time())
            fetch_graph.atp_graph_Y.append(0)
        
        # hum    
        cursor.execute(get_graph_hum)
        if cursor.rowcount > 0:
            db_graph_hum = cursor.fetchall()
            fetch_graph.hum_graph_X = []
            fetch_graph.hum_graph_Y = []

            for i in db_graph_hum:
                fetch_graph.hum_graph_X.append(i[1])
                fetch_graph.hum_graph_Y.append(i[0])

        else:
            fetch_graph.hum_graph_X = []
            fetch_graph.hum_graph_Y = []
            fetch_graph.hum_graph_X.append(time.time())
            fetch_graph.hum_graph_Y.append(0)
        # temp            
        cursor.execute(get_graph_temp)
        if cursor.rowcount > 0:
            db_graph_temp = cursor.fetchall()
            fetch_graph.temp_graph_X = []
            fetch_graph.temp_graph_Y = []

            for i in db_graph_temp:
                fetch_graph.temp_graph_X.append(i[1])
                fetch_graph.temp_graph_Y.append(i[0])

        else:
            fetch_graph.temp_graph_X = []
            fetch_graph.temp_graph_Y = []
            fetch_graph.temp_graph_X.append(time.time())
            fetch_graph.temp_graph_Y.append(0)

    except Exception as e:
        filename = Path(__file__).name
        error_handle(e, filename)


def sens_arrow(sens_number):
    fetch_last_sens = "SELECT * FROM sens ORDER BY id DESC LIMIT 1, 1"

    try:
        cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
        cursor = cnx.cursor(buffered=True)

        cursor.execute(fetch_last_sens)
        if cursor.rowcount > 0:
            db_last_sens = cursor.fetchone()
            temp = str(db_last_sens[1])
            hum = str(round(db_last_sens[2]))
            atp = str(db_last_sens[3])
        else:
            print("error")
    except Exception as e:
        filename = Path(__file__).name
        error_handle(e, filename)

    if len(fetch_sens.current_sens) > 0:
        last_sens = db_last_sens[sens_number]
        current_sens = fetch_sens.current_sens[sens_number]
        if last_sens < current_sens:
            img = "arrow_up.png"
            return img
        elif last_sens > current_sens:
            img = "arrow_down.png"
            return img
        elif last_sens == current_sens:
            img = "arrow_flat.png"
            return img
    else:
        img = "arrow_flat.png"
        return img


thread_fetch_wind = threading.Thread(target=fetch_wind, args=())
thread_fetch_wind.daemon = True
thread_fetch_wind.start()

thread_make_mean = threading.Thread(target=make_mean, args=())
thread_make_mean.daemon = True
thread_make_mean.start()

thread_mean = threading.Thread(target=fetch_mean, args=())
thread_mean.daemon = True
thread_mean.start()

thread_fetch_sens = threading.Thread(target=fetch_sens, args=())
thread_fetch_sens.daemon = True
thread_fetch_sens.start()

thread_fetch_gps = threading.Thread(target=fetch_gps, args=())
thread_fetch_gps.daemon = True
thread_fetch_gps.start()

thread_fetch_graph = threading.Thread(target=fetch_graph, args=())
thread_fetch_graph.daemon = True
thread_fetch_graph.start()

# thread_db_cleanup = threading.Thread(target=db_cleanup, args=())
# thread_db_cleanup.daemon = True
# thread_db_cleanup.start()

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

        path = str(Path(__file__).parent.absolute())

        self.O1 = QVBoxLayout(self)
        self.mainContainer = QHBoxLayout(self)
        self.windContainer = QVBoxLayout(self)

        try: #Wind box
            self.windHeader = QHBoxLayout()
            self.windHL = QLabel("WIND")
            self.windHL.setFont(QFont('Arial', 20))
            self.windHL.setAlignment(Qt.AlignCenter)
            self.windHeader.addWidget(self.windHL)
            self.meanHL = QLabel("MEAN")
            self.meanHL.setFont(QFont('Arial', 20))
            self.meanHL.setAlignment(Qt.AlignCenter)
            self.windHeader.addWidget(self.meanHL)
            self.windContainer.addLayout(self.windHeader)

            self.windBox = QHBoxLayout()
            self.windFrame = QFrame(self)
            self.wind_VL = QVBoxLayout(self.windFrame)
            self.windL = QLabel(fetch_wind.wind, self.windFrame)
            img = "/img/wind-circle.png"
            self.windL.setStyleSheet("background-image: url({}); "
                                     "background-repeat: no-repeat; "
                                     "background-position: center".format(path + img))
            self.windL.setAlignment(Qt.AlignCenter)
            self.windL.setMinimumHeight(200)
            self.windL.setFont(QFont('Arial', 50))
            self.wind_VL.addWidget(self.windL)
            self.windBox.addWidget(self.windFrame)

            self.meanFrame = QFrame(self)
            self.mean_VL = QVBoxLayout(self.meanFrame)
            self.meanL = QLabel(str(fetch_mean.meanwind), self.meanFrame)
            self.meanL.setStyleSheet("background-image: url({}); "
                                     "background-repeat: no-repeat; "
                                     "background-position: center".format(path + img))
            self.meanL.setAlignment(Qt.AlignCenter)
            self.meanL.setMinimumHeight(200)
            self.meanL.setFont(QFont('Arial', 50))
            self.mean_VL.addWidget(self.meanL)
            self.windBox.addWidget(self.meanFrame)

            self.windContainer.addLayout(self.windBox)

        except Exception as e:
            filename = Path(__file__).name
            error_handle(e, filename)

        #Bauforth box
        self.beaufortbox = QHBoxLayout()
        self.beaufortL = QLabel(str(fetch_mean.beaufortLS))
        self.beaufortL.setAlignment(Qt.AlignHCenter)
        self.beaufortL.setMinimumHeight(40)
        self.beaufortL.setFont(QFont('Arial', 20))
        self.beaufortbox.addWidget(self.beaufortL)
        self.windContainer.addLayout(self.beaufortbox)

        #GRAPH
        self.graphContainer = QVBoxLayout()
        self.graph = graph_plot(fetch_graph.wind_graph_X,fetch_graph.wind_graph_Y,fetch_graph.atp_graph_X,fetch_graph.atp_graph_Y)
        self.graphContainer.addWidget(self.graph)
        self.windContainer.addLayout(self.graphContainer)
        self.windContainer.addStretch()
        self.mainContainer.addLayout(self.windContainer)

        #sens container
        self.sensFrame = QFrame(self)
        self.sensBox = QVBoxLayout(self.sensFrame)

        # self.sensheaderFrame =  QFrame(self)
        self.sensheaderBox = QHBoxLayout(self.sensFrame)
        self.sensHL = QLabel("SENSOR")
        self.sensHL.setFont(QFont('Arial', 15))
        # self.sensHL.setMinimumHeight(50)
        self.sensheaderBox.addWidget(self.sensHL)
        self.sensBox.addLayout(self.sensheaderBox)

        self.sensgrid = QGridLayout()
        self.sensBox.addLayout(self.sensgrid)


        self.tempimg = QPixmap(path + '/img/ico-generic.png')
        self.tempico = QLabel()
        self.tempico.setPixmap(self.tempimg)
        self.tempvalue = QLabel(fetch_sens.temp + " °C")
        self.tempvalue.setFont(QFont('Arial', 13))
        self.tempimgarrow = QPixmap(path + '/img/' + sens_arrow(1))
        self.temparrow = QLabel()
        self.temparrow.setPixmap(self.tempimgarrow)

        self.sensgrid.addWidget(self.tempico, 0, 0, Qt.AlignCenter)
        self.sensgrid.addWidget(self.tempvalue, 0, 1, Qt.AlignCenter)
        self.sensgrid.addWidget(self.temparrow, 0, 2, Qt.AlignCenter)

        self.humimg = QPixmap(path + '/img/ico-generic.png')
        self.humico = QLabel()
        self.humico.setPixmap(self.humimg)
        self.humvalue = QLabel(fetch_sens.hum + " %")
        self.humvalue.setFont(QFont('Arial', 13))
        self.humimgarrow = QPixmap(path + '/img/' + sens_arrow(2))
        self.humarrow = QLabel()
        self.humarrow.setPixmap(self.humimgarrow)

        self.sensgrid.addWidget(self.humico, 1, 0, Qt.AlignCenter)
        self.sensgrid.addWidget(self.humvalue, 1, 1, Qt.AlignCenter)
        self.sensgrid.addWidget(self.humarrow, 1, 2, Qt.AlignCenter)

        self.atpimg = QPixmap(path + '/img/ico-generic.png')
        self.atpico = QLabel()
        self.atpico.setPixmap(self.atpimg)
        self.atpvalue = QLabel(fetch_sens.atp + " hPa")
        self.atpvalue.setFont(QFont('Arial', 13))
        self.atpimgarrow = QPixmap(path + '/img/' + sens_arrow(3))
        self.atparrow = QLabel()
        self.atparrow.setPixmap(self.atpimgarrow)

        self.sensgrid.addWidget(self.atpico, 2, 0, Qt.AlignCenter)
        self.sensgrid.addWidget(self.atpvalue, 2, 1, Qt.AlignCenter)
        self.sensgrid.addWidget(self.atparrow, 2, 2, Qt.AlignCenter)

        self.sensBox.addStretch()
        self.sensBox.addLayout(self.sensgrid)


        #Forecast container
        self.forecast = QVBoxLayout(self.sensFrame)
        self.Fheader = QLabel("FORECAST")
        self.Fheader.setFont(QFont('Arial', 15))
        forecast_val = forecast()
        self.Fforecast1 = QLabel("Expect: " + forecast_val[0] + " conditions")
        self.Fforecast2 = QLabel("Changes: " + forecast_val[1])
        self.Fforecast3 = QLabel("Expected Winds: " + forecast_val[2] + " BFT")

        self.forecast.addWidget(self.Fheader)
        self.forecast.addWidget(self.Fforecast1)
        self.forecast.addWidget(self.Fforecast2)
        self.forecast.addWidget(self.Fforecast3)
        self.forecast.addStretch()
        self.sensBox.addLayout(self.forecast)

        #GPS container
        self.gpsBox = QVBoxLayout(self.sensFrame)
        self.latitude = QLabel("Latitude: " + fetch_gps.lat)
        self.longitude = QLabel("Longitude: " + fetch_gps.long)
        self.altitude = QLabel("Altitude: " + fetch_gps.alt)

        self.gpsBox.addWidget(self.latitude)
        self.gpsBox.addWidget(self.longitude)
        self.gpsBox.addWidget(self.altitude)
        self.sensBox.addLayout(self.gpsBox)
        self.gpsBox.addStretch()

        # self.sensBox.addStretch()

        # self.gbp = 2
        button_style = "background-color: #444444; color: black; font-weight:600"
        self.button_wind = QPushButton()
        self.button_wind.setText("WIND")
        self.button_wind.setStyleSheet(button_style)
        self.button_wind.setCheckable(True)
        
        self.button_temp = QPushButton()
        self.button_temp.setText("TEMP")
        self.button_temp.setStyleSheet(button_style)
        self.button_temp.setCheckable(True)
        
        self.button_hum = QPushButton()
        self.button_hum.setText("HUM")
        self.button_hum.setStyleSheet(button_style)
        self.button_hum.setCheckable(True)
        
        self.button_atp = QPushButton()
        self.button_atp.setText("ATP")
        self.button_atp.setStyleSheet(button_style)
        self.button_atp.setCheckable(True)
        
        
        self.button_wind.clicked.connect(self.button_wind_clicked)
        self.sensBox.addWidget(self.button_wind)
        self.sensBox.addWidget(self.button_temp)
        self.sensBox.addWidget(self.button_hum)
        self.sensBox.addWidget(self.button_atp)

        self.sensBox.addStretch()

        # # footer box
        # self.footerbox = QVBoxLayout()
        # self.credit = QLabel("Creator: Stefan Bahrawy")
        # self.winddate = QLabel("W: " + str(fetch_wind.timestamp))
        # self.sensdate = QLabel("S: " + str(fetch_sens.sens_timestamp))
        # self.gpsdate = QLabel("G: " + str(fetch_gps.gps_timestamp))
        #
        # self.credit.setFont(QFont('Arial', 8))
        # self.winddate.setFont(QFont('Arial', 8))
        # self.sensdate.setFont(QFont('Arial', 8))
        # self.gpsdate.setFont(QFont('Arial', 8))
        #
        # self.footerbox.addWidget(self.credit)
        # self.footerbox.addWidget(self.winddate)
        # self.footerbox.addWidget(self.sensdate)
        # self.footerbox.addWidget(self.gpsdate)
        # self.sensBox.addLayout(self.footerbox)
        #
        # self.footerbox.addStretch()
        self.mainContainer.addWidget(self.sensFrame)

        self.O1.addLayout(self.mainContainer)


    def button_wind_clicked(self):
        global gbp
        if gbp < 3:
            gbp += 1
        else:
            gbp = 0
        fetch_graph()
        try:
            blabel = ["WIND", "ATP", "HUM", "TEMP"]
            self.button_wind.setText(blabel[gbp])
            graph_update(self, fetch_graph.wind_graph_X, fetch_graph.wind_graph_Y)
            self.graph

        except Exception as e:
            filename = Path(__file__).name
            error_handle(e, filename)

        QApplication.processEvents()

    def update_wind(self):
        try:
            self.windL.setText(fetch_wind.wind)
            self.meanL.setText(str(fetch_mean.meanwind))
            # self.winddate.setText("W: " + str(fetch_wind.timestamp))
            self.beaufortL.setText(fetch_mean.beaufortLS)
        except Exception as e:
            filename = Path(__file__).name
            error_handle(e, filename)

        QApplication.processEvents()

    def update_sens(self):
        try:
            path = str(Path(__file__).parent.absolute())
            fetch_graph()
            fetch_sens()
            fetch_gps()
            forecast()
            forecast_val = forecast()

            self.tempvalue.setText(fetch_sens.temp + " °C")
            self.tempimgarrow = QPixmap(path + '/img/' + sens_arrow(1))
            self.temparrow.setPixmap(self.tempimgarrow)
            self.humvalue.setText(fetch_sens.hum + "%")
            self.humimgarrow = QPixmap(path + '/img/' + sens_arrow(2))
            self.humarrow.setPixmap(self.humimgarrow)
            self.atpvalue.setText(fetch_sens.atp + " hPa")
            self.atpimgarrow = QPixmap(path + '/img/' + sens_arrow(3))
            self.atparrow.setPixmap(self.atpimgarrow)

            self.Fforecast1.setText("Expect: " + forecast_val[0] + " conditions")
            self.Fforecast2.setText("Changes: " + forecast_val[1])
            self.Fforecast3.setText("Expected Winds: " + forecast_val[2] + " BFT")

            self.latitude.setText("Latitude: " + fetch_gps.lat)
            self.longitude.setText("Longitude: " + fetch_gps.long)
            self.altitude.setText("Altitude: " + fetch_gps.alt)

            graph_update(self, fetch_graph.wind_graph_X, fetch_graph.wind_graph_Y)
            self.graph

            # self.sensdate.setText("S: " + str(fetch_sens.sens_timestamp))
            # self.gpsdate.setText("G: " + str(fetch_gps.gps_timestamp))

        except Exception as e:
            filename = Path(__file__).name
            error_handle(e, filename)

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
    timer2.start(5000)

    sys.exit(app.exec_())

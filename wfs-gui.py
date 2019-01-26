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
            self.hum = str(round(db_sens[2]))
            self.atp = str(db_sens[3])
            self.sens_timestamp = str(db_sens[4])

            get_gps = "SELECT * FROM gps WHERE id=(SELECT MAX(id) FROM gps)"
            cursor.execute(get_gps)
            db_gps = cursor.fetchone()
            self.lat = str(db_gps[1])
            self.long = str(db_gps[2])
            self.alt = str(db_gps[3])
            self.gps_timestamp = str(db_gps[4])

            # WIND
            get_max_wind_12 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
            get_max_wind_24 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
            get_max_wind = "SELECT MAX(wind) FROM wind"

            get_min_wind_12 = "SELECT MIN(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
            get_min_wind_24 = "SELECT MIN(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"

            get_mean_wind = "SELECT AVG(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 10 MINUTE)"

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

            cursor.execute(get_mean_wind)
            db_mean_wind = cursor.fetchone()
            try:
                self.meanwind = str(round(db_mean_wind[0], 1))
            except:
                self.meanwind = "0"

            #   MAX
            cursor.execute(get_max_temp)
            db_max_temp = cursor.fetchone()
            try:
                self.maxtemp = str(round(db_max_temp[0], 1))
            except:
                self.maxtemp = "0"

            cursor.execute(get_max_hum)
            db_max_hum = cursor.fetchone()
            try:
                self.maxhum = str(round(db_max_hum[0]))
            except:
                self.maxhum = "0"

            cursor.execute(get_max_atp)
            db_max_atp = cursor.fetchone()
            try:
                self.maxatp = str(round(db_max_atp[0]))
            except:
                self.maxatp = "0"
            
            #   MIN
            cursor.execute(get_min_temp)
            db_min_temp = cursor.fetchone()
            try:
                self.mintemp = str(round(db_min_temp[0], 1))
            except:
                self.mintemp = "0"

            cursor.execute(get_min_hum)
            db_min_hum = cursor.fetchone()
            try:
                self.minhum = str(round(db_min_hum[0]))
            except:
                self.minhum = "0"

            cursor.execute(get_min_atp)
            db_min_atp = cursor.fetchone()
            try:
                self.minatp = str(round(db_min_atp[0]))
            except:
                self.minatp = "0"
            
            
            #   MAX12
            cursor.execute(get_max_temp_12)
            db_max_temp_12 = cursor.fetchone()
            try:
                self.max12temp = str(round(db_max_temp_12[0], 1))
            except:
                self.max12temp = "0"

            cursor.execute(get_max_hum_12)
            db_max_hum_12 = cursor.fetchone()
            try:
                self.max12hum = str(round(db_max_hum_12[0]))
            except:
                self.max12hum = "0"

            cursor.execute(get_max_atp_12)
            db_max_atp_12 = cursor.fetchone()
            try:
                self.max12atp = str(round(db_max_atp_12[0]))
            except:
                self.max12atp = "0"

            #   MIN12
            cursor.execute(get_min_temp_12)
            db_min_temp_12 = cursor.fetchone()
            try:
                self.min12temp = str(round(db_min_temp_12[0], 1))
            except:
                self.min12temp = "0"

            cursor.execute(get_min_hum_12)
            db_min_hum_12 = cursor.fetchone()
            try:
                self.min12hum = str(round(db_min_hum_12[0]))
            except:
                self.min12hum = "0"

            cursor.execute(get_min_atp_12)
            db_min_atp_12 = cursor.fetchone()
            try:
                self.min12atp = str(round(db_min_atp_12[0]))
            except:
                self.min12atp = "0"

            #   MAX24
            cursor.execute(get_max_temp_24)
            db_max_temp_24 = cursor.fetchone()
            try:
                self.max24temp = str(round(db_max_temp_24[0], 1))
            except:
                self.max24temp = "0"

            cursor.execute(get_max_hum_24)
            db_max_hum_24 = cursor.fetchone()
            try:
                self.max24hum = str(round(db_max_hum_24[0]))
            except:
                self.max24hum = "0"

            cursor.execute(get_max_atp_24)
            db_max_atp_24 = cursor.fetchone()
            try:
                self.max24atp = str(round(db_max_atp_24[0]))
            except:
                self.max24atp = "0"

            #   MIN24
            cursor.execute(get_min_temp_24)
            db_min_temp_24 = cursor.fetchone()
            try:
                self.min24temp = str(round(db_min_temp_24[0], 1))
            except:
                self.min24temp = "0"

            cursor.execute(get_min_hum_24)
            db_min_hum_24 = cursor.fetchone()
            try:
                self.min24hum = str(round(db_min_hum_24[0]))
            except:
                self.min24hum = "0"

            cursor.execute(get_min_atp_24)
            db_min_atp_24 = cursor.fetchone()
            try:
                self.min24atp = str(round(db_min_atp_24[0]))
            except:
                self.min24atp = "0"


            # print("Thread Running")

            time.sleep(self.interval)


data = GetData()


class App(QWidget):

    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)
        self.title = "WFS - Weather Forecast Station"
        self.setWindowIcon(QIcon("drawing.svg.png"))
        self.left = 475
        self.top = 650
        self.width = 480
        self.height = 720
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("color: white; background-color: #152025;")
        self.initUI()

    def initUI(self):

        self.mainContainer = QVBoxLayout(self)
        self.windContainer = QHBoxLayout()

        self.windFrame = QFrame(self)
        self.wind_VL = QVBoxLayout(self.windFrame)
        self.windL = QLabel(data.wind, self.windFrame)
        self.windL.setStyleSheet("background-image: url('wind-circle.png'); background-repeat: no-repeat;")
        self.windL.setAlignment(Qt.AlignCenter)
        self.windL.setMinimumHeight(200)
        self.windL.setFont(QFont('Arial', 50))
        self.wind_VL.addWidget(self.windL)
        self.windContainer.addWidget(self.windFrame)

        self.meanFrame = QFrame(self)
        self.mean_VL = QVBoxLayout(self.meanFrame)
        self.meanL = QLabel(data.meanwind, self.meanFrame)
        self.meanL.setStyleSheet("background-image: url('wind-circle.png'); background-repeat: no-repeat;")
        self.meanL.setAlignment(Qt.AlignCenter)
        self.meanL.setMinimumHeight(200)
        self.meanL.setFont(QFont('Arial', 50))
        self.mean_VL.addWidget(self.meanL)
        self.windContainer.addWidget(self.meanFrame)
        
        self.mainContainer.addLayout(self.windContainer)

        self.sensContainer = QVBoxLayout()
        self.sensContainer.setSpacing(0)

        self.sensFrame = QFrame(self)
        self.sensgrid = QGridLayout(self.sensFrame)

        self.sensgrid.addWidget(QLabel("Temp (°C)"),    0, 1)
        self.sensgrid.addWidget(QLabel("Humid (%)"),    0, 2)
        self.sensgrid.addWidget(QLabel("ATP (mBar)"),   0, 3)

        self.sensgrid.addWidget(QLabel("Current"),      1, 0)
        self.sensgrid.addWidget(QLabel("Max 12hrs"),    2, 0)
        self.sensgrid.addWidget(QLabel("Min 12hrs"),    3, 0)
        self.sensgrid.addWidget(QLabel("Max 24hrs"),    4, 0)
        self.sensgrid.addWidget(QLabel("Min 24hrs"),    5, 0)
        self.sensgrid.addWidget(QLabel("Max all time"), 6, 0)
        self.sensgrid.addWidget(QLabel("Min all time"), 7, 0)

        self.sensgrid.addWidget(QLabel(data.temp),      1, 1)
        self.sensgrid.addWidget(QLabel(data.hum),       1, 2)
        self.sensgrid.addWidget(QLabel(data.atp),       1, 3)

        self.sensgrid.addWidget(QLabel(data.max12temp), 2, 1)
        self.sensgrid.addWidget(QLabel(data.max12hum),  2, 2)
        self.sensgrid.addWidget(QLabel(data.max12atp),  2, 3)

        self.sensgrid.addWidget(QLabel(data.min12temp), 3, 1)
        self.sensgrid.addWidget(QLabel(data.min12hum),  3, 2)
        self.sensgrid.addWidget(QLabel(data.min12atp),  3, 3)

        self.sensgrid.addWidget(QLabel(data.max24temp), 4, 1)
        self.sensgrid.addWidget(QLabel(data.max24hum),  4, 2)
        self.sensgrid.addWidget(QLabel(data.max24atp),  4, 3)

        self.sensgrid.addWidget(QLabel(data.min24temp), 5, 1)
        self.sensgrid.addWidget(QLabel(data.min24hum),  5, 2)
        self.sensgrid.addWidget(QLabel(data.min24atp),  5, 3)

        self.sensgrid.addWidget(QLabel(data.maxtemp),   6, 1)
        self.sensgrid.addWidget(QLabel(data.maxhum),    6, 2)
        self.sensgrid.addWidget(QLabel(data.maxatp),    6, 3)

        self.sensgrid.addWidget(QLabel(data.mintemp),   7, 1)
        self.sensgrid.addWidget(QLabel(data.minhum),    7, 2)
        self.sensgrid.addWidget(QLabel(data.minatp),    7, 3)

        self.sensContainer.addWidget(self.sensFrame)
        self.mainContainer.addLayout(self.sensContainer)
        self.mainContainer.addStretch()


    def update_label(self):
        self.windL.setText(data.wind)
        self.meanL.setText(data.meanwind)
        # self.sensgrid.addWidget.setT
        # self.temp_label.setText(data.temp)
        # self.hum_label.setText(data.hum)
        # self.atp_label.setText(data.atp)
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()

    timer = QTimer()
    timer.timeout.connect(ex.update_label)
    timer.start(1000)

    sys.exit(app.exec_())

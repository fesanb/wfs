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

            get_max_wind01 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 1 MINUTE)"
            get_max_wind05 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 5 MINUTE)"
            get_max_wind010 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 10 MINUTE)"
            get_max_wind030 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 30 MINUTE)"
            get_max_wind1 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)"
            get_max_wind2 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 2 HOUR)"
            get_max_wind4 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 4 HOUR)"
            get_max_wind6 = "SELECT MAX(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 6 HOUR)"

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

            #   Wind History MAx list
            cursor.execute(get_max_wind01)
            db_max_temp01 = cursor.fetchone()
            try:
                self.maxwind01 = str(round(db_max_temp01[0], 1))
            except:
                self.maxwind01 = "0"

            cursor.execute(get_max_wind05)
            db_max_temp05 = cursor.fetchone()
            try:
                self.maxwind05 = str(round(db_max_temp05[0], 1))
            except:
                self.maxwind05 = "0"

            cursor.execute(get_max_wind010)
            db_max_temp010 = cursor.fetchone()
            try:
                self.maxwind010 = str(round(db_max_temp010[0], 1))
            except:
                self.maxwind010 = "0"

            cursor.execute(get_max_wind030)
            db_max_temp030 = cursor.fetchone()
            try:
                self.maxwind030 = str(round(db_max_temp030[0], 1))
            except:
                self.maxwind030 = "0"

            cursor.execute(get_max_wind1)
            db_max_temp1 = cursor.fetchone()
            try:
                self.maxwind1 = str(round(db_max_temp1[0], 1))
            except:
                self.maxwind1 = "0"

            cursor.execute(get_max_wind2)
            db_max_temp2 = cursor.fetchone()
            try:
                self.maxwind2 = str(round(db_max_temp2[0], 1))
            except:
                self.maxwind2 = "0"

            cursor.execute(get_max_wind4)
            db_max_temp4 = cursor.fetchone()
            try:
                self.maxwind4 = str(round(db_max_temp4[0], 1))
            except:
                self.maxwind4 = "0"

            cursor.execute(get_max_wind6)
            db_max_temp6 = cursor.fetchone()
            try:
                self.maxwind6 = str(round(db_max_temp6[0], 1))
            except:
                self.maxwind6 = "0"

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

            baufort = [
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
                "Beaufort 12 - Hurricane"
            ]
            baufortmean = self.meanwind

            if float(baufortmean) < 0.3:
                self.baufortLS = baufort[0]
            if float(baufortmean) > 1.6:
                self.baufortLS = baufort[1]
            if float(baufortmean) > 3.4:
                self.baufortLS = baufort[2]
            if float(baufortmean) > 5.5:
                self.baufortLS = baufort[3]
            if float(baufortmean) > 8.0:
                self.baufortLS = baufort[4]
            if float(baufortmean) > 10.8:
                self.baufortLS = baufort[5]
            if float(baufortmean) > 13.9:
                self.baufortLS = baufort[6]
            if float(baufortmean) > 17.2:
                self.baufortLS = baufort[7]
            if float(baufortmean) > 20.8:
                self.baufortLS = baufort[8]
            if float(baufortmean) > 24.5:
                self.baufortLS = baufort[9]
            if float(baufortmean) > 28.5:
                self.baufortLS = baufort[10]
            if float(baufortmean) > 32.7:
                self.baufortLS = baufort[11]


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

        self.windHeader = QHBoxLayout(self)
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

        self.baufortbox = QHBoxLayout()
        self.baufortL = QLabel(data.baufortLS)
        self.baufortL.setAlignment(Qt.AlignHCenter)
        self.baufortL.setMinimumHeight(50)
        self.baufortL.setFont(QFont('Arial', 20))
        self.baufortbox.addWidget(self.baufortL)
        self.mainContainer.addLayout(self.baufortbox)


        self.windHistoryContainer = QVBoxLayout()
        self.windHistoryHeader = QHBoxLayout()
        self.windHHLS = "Max Wind History:"
        self.windHHL = QLabel(self.windHHLS)
        self.windHHL.setFont(QFont('Arial', 15))
        self.windHistoryHeader.addWidget(self.windHHL)
        self.windHistoryContainer.addLayout(self.windHistoryHeader)

        self.windHG = QGridLayout()
        self.windHG.addWidget(QLabel("1min"),   0, 0)
        self.windHG.addWidget(QLabel("5min"),   0, 1)
        self.windHG.addWidget(QLabel("10min"),  0, 2)
        self.windHG.addWidget(QLabel("30min"),  0, 3)
        self.windHG.addWidget(QLabel("1hr"),    0, 4)
        self.windHG.addWidget(QLabel("2hr"),    0, 5)
        self.windHG.addWidget(QLabel("4hr"),    0, 6)
        self.windHG.addWidget(QLabel("6hr"),    0, 7)

        self.windmax01 = QLabel(data.maxwind01)
        self.windmax01.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax01,   1, 0)

        self.windmax05 = QLabel(data.maxwind05)
        self.windmax05.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax05,   1, 1)

        self.windmax010 = QLabel(data.maxwind010)
        self.windmax010.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax010,  1, 2)

        self.windmax030 = QLabel(data.maxwind030)
        self.windmax030.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax030,  1, 3)

        self.windmax1 = QLabel(data.maxwind1)
        self.windmax1.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax1,    1, 4)

        self.windmax2 = QLabel(data.maxwind2)
        self.windmax2.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax2,    1, 5)

        self.windmax4 = QLabel(data.maxwind4)
        self.windmax4.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax4,    1, 6)

        self.windmax6 = QLabel(data.maxwind6)
        self.windmax6.setAlignment(Qt.AlignHCenter)
        self.windHG.addWidget(self.windmax6,    1, 7)



        self.windHistoryContainer.addLayout(self.windHG)
        self.mainContainer.addLayout(self.windHistoryContainer)

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

        self.tempL = QLabel(data.temp)
        self.sensgrid.addWidget(self.tempL,      1, 1)
        self.humL = QLabel(data.hum)
        self.sensgrid.addWidget(self.humL,       1, 2)
        self.atpL = QLabel(data.atp)
        self.sensgrid.addWidget(self.atpL,       1, 3)

        self.max12tempL = QLabel(data.max12temp)
        self.sensgrid.addWidget(self.max12tempL, 2, 1)
        self.max12humL = QLabel(data.max12hum)
        self.sensgrid.addWidget(self.max12humL,  2, 2)
        self.max12atpL = QLabel(data.max12atp)
        self.sensgrid.addWidget(self.max12atpL,  2, 3)

        self.min12tempL = QLabel(data.min12temp)
        self.sensgrid.addWidget(self.min12tempL, 3, 1)
        self.min12humL = QLabel(data.min12hum)
        self.sensgrid.addWidget(self.min12humL,  3, 2)
        self.min12atpL = QLabel(data.min12atp)
        self.sensgrid.addWidget(self.min12atpL,  3, 3)

        self.max24tempL = QLabel(data.max24temp)
        self.sensgrid.addWidget(self.max24tempL, 4, 1)
        self.max24humL = QLabel(data.max24hum)
        self.sensgrid.addWidget(self.max24humL,  4, 2)
        self.max24atpL = QLabel(data.max24atp)
        self.sensgrid.addWidget(self.max24atpL,  4, 3)

        self.min24tempL = QLabel(data.min24temp)
        self.sensgrid.addWidget(self.min24tempL, 5, 1)
        self.min24humL = QLabel(data.min24hum)
        self.sensgrid.addWidget(self.min24humL,  5, 2)
        self.min24atpL = QLabel(data.min24atp)
        self.sensgrid.addWidget(self.min24atpL,  5, 3)

        self.maxtempL = QLabel(data.maxtemp)
        self.sensgrid.addWidget(self.maxtempL,   6, 1)
        self.maxhumL = QLabel(data.maxhum)
        self.sensgrid.addWidget(self.maxhumL,    6, 2)
        self.maxatpL = QLabel(data.maxatp)
        self.sensgrid.addWidget(self.maxatpL,    6, 3)

        self.mintempL = QLabel(data.mintemp)
        self.sensgrid.addWidget(self.mintempL,   7, 1)
        self.minhumL = QLabel(data.minhum)
        self.sensgrid.addWidget(self.minhumL,    7, 2)
        self.minatpL = QLabel(data.minatp)
        self.sensgrid.addWidget(self.minatpL,    7, 3)

        self.sensContainer.addWidget(self.sensFrame)
        self.mainContainer.addLayout(self.sensContainer)
        self.mainContainer.addStretch()


    def update_label(self):
        self.windL.setText(data.wind)
        self.meanL.setText(data.meanwind)

        self.baufortL.setText(data.baufortLS)

        self.tempL.setText(data.temp)
        self.humL.setText(data.hum)
        self.atpL.setText(data.atp)

        self.max12tempL.setText(data.max12temp)
        self.max12humL.setText(data.max12hum)
        self.max12atpL.setText(data.max12atp)

        self.min12tempL.setText(data.min12temp)
        self.min12humL.setText(data.min12hum)
        self.min12atpL.setText(data.min12atp)

        self.max24tempL.setText(data.max24temp)
        self.max24humL.setText(data.max24hum)
        self.max24atpL.setText(data.max24atp)

        self.min24tempL.setText(data.min24temp)
        self.min24humL.setText(data.min24hum)
        self.min24atpL.setText(data.min24atp)

        self.maxtempL.setText(data.maxtemp)
        self.maxhumL.setText(data.maxhum)
        self.maxatpL.setText(data.maxatp)

        self.mintempL.setText(data.mintemp)
        self.minhumL.setText(data.minhum)
        self.minatpL.setText(data.minatp)

        self.windmax01.setText(data.maxwind01)
        self.windmax05.setText(data.maxwind05)
        self.windmax010.setText(data.maxwind010)
        self.windmax030.setText(data.maxwind030)
        self.windmax1.setText(data.maxwind1)
        self.windmax2.setText(data.maxwind2)
        self.windmax4.setText(data.maxwind4)
        self.windmax6.setText(data.maxwind6)

        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()

    timer = QTimer()
    timer.timeout.connect(ex.update_label)
    timer.start(1000)

    sys.exit(app.exec_())

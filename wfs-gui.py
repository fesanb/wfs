import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QIcon
import mysql.connector

wind = 0.0
hum = 48
atp = 1001
lat = 10.58
long = 56.84
alt = 26
sat = 13


def get_data():

    cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
    cursor = cnx.cursor()

    get_wind = "SELECT wind FROM wind WHERE id=(SELECT MAX(id) FROM wind)"
    cursor.execute(get_wind)
    get_data.wind = cursor.fetchone()




get_data()
print(get_data.wind)


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "WFS - Weather Forecast Station"
        self.left = 50
        self.top = 100
        self.width = 450
        self.height = 350
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        wind_label = QLabel("wind: " + str(wind), self)
        wind_label.move(50, 50)

        hum_label = QLabel("Humidity: " + str(hum), self)
        hum_label.move(50, 75)

        atp_label = QLabel("Atm. Pressure: " + str(atp), self)
        atp_label.move(50, 100)

        lat_label = QLabel("Latitude: " + str(lat), self)
        lat_label.move(50, 125)

        long_label = QLabel("Longitude: " + str(long), self)
        long_label.move(50, 150)

        alt_label = QLabel("Altitude: " + str(alt), self)
        alt_label.move(50, 175)

        sat_label = QLabel("Sattelites: " + str(sat), self)
        sat_label.move(50, 200)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


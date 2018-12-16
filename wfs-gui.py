#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QIcon
import mysql.connector


def get_data():

    cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
    cursor = cnx.cursor()

    get_wind = "SELECT * FROM wind WHERE id=(SELECT MAX(id) FROM wind)"
    cursor.execute(get_wind)
    get_data.wind = cursor.fetchone()
    global wind
    wind = get_data.wind[1]
    global wind_timestamp
    wind_timestamp = get_data.wind[2]

    get_sens = "SELECT * FROM sens WHERE id=(SELECT MAX(id) FROM sens)"
    cursor.execute(get_sens)
    get_data.sens = cursor.fetchone()
    global temp
    temp = get_data.sens[1]
    global hum
    hum = get_data.sens[2]
    global atp
    atp = get_data.sens[3]
    global sens_timestamp
    sens_timestamp = get_data.sens[4]

    get_gps = "SELECT * FROM gps WHERE id=(SELECT MAX(id) FROM gps)"
    cursor.execute(get_gps)
    get_data.gps = cursor.fetchone()
    global lat
    lat = get_data.gps[1]
    global long
    long = get_data.gps[2]
    global alt
    alt = get_data.gps[3]
    global gps_timestamp
    gps_timestamp = get_data.gps[4]


get_data()


print("Wind: ", wind, "Timestamp: ", wind_timestamp)
print("Temp: ", temp, "Hum: ", hum, "ATP: ", atp, "Timestamp: ", sens_timestamp)
print("Lat: ", lat, "Long: ", long, "Alt: ", alt, "Timestamp: ", gps_timestamp)


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "WFS - Weather Forecast Station"
        self.setWindowIcon(QIcon("drawing.svg.png"))
        self.left = 2000
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

        test_label = QLabel(self)
        test_label.setText("test å skirve en skikkelig lang text for å se om det feiler")
        test_label.move(50, 200)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


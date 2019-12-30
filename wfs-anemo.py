# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import sys
import RPi.GPIO as g
from time import sleep, perf_counter
import mysql.connector
from pathlib import Path
from wfs_error_handling import error_handle

g.setmode(g.BCM)
g.setup(16, g.IN, pull_up_down=g.PUD_DOWN)

global anemo
anemo = 0


def increv(channel):
    global anemo
    anemo += 1


def db_insert(wind):
    cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
    cursor = cnx.cursor()
    cursor.execute(u'''INSERT INTO wind(wind) VALUES ({0})'''.format(wind))
    cnx.commit()
    # print("SQL insert done")


g.add_event_detect(16, g.RISING, callback=increv)

last_wind = 0

while True:
    try:
        sleep(1)
        wind = anemo * 0.1
        if wind == last_wind:
            # print("Wind: {0}m/s".format(wind), end="\r")
            pass
        else:
            db_insert(wind)
            # print("SQL insert - Wind: {0}m/s".format(wind), end="\r")
            last_wind = wind
            anemo = 0

    except Exception as e:
        filename = Path(__file__).name
        error_handle(e, filename)

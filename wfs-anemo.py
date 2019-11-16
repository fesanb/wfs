# WFS - Weather Forecast Station
# Written by Stefan Bahrawy


import sys
import RPi.GPIO as g
from time import sleep, perf_counter
import mysql.connector

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
    cursor.execute(u'''INSERT INTO wind(wind) VALUES (%s)''' % wind)
    emp_no = cursor.lastrowid
    cnx.commit()


g.add_event_detect(16, g.RISING, callback=increv)

while True:
    try:
        sleep(1)
        wind = anemo * 0.1
        print("Frequency: {0}Hz".format(anemo))
        print("Wind: {0}m/s".format(wind))
        db_insert(wind)
        anemo = 0

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(repr(e))

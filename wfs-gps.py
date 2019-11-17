# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import sys
import pynmea2
import serial
import mysql.connector
from time import sleep

sleep_time = 30
sleep_time2 = 0


def db_insert(lat, lon, alt):
    cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
    cursor = cnx.cursor()
    try:
        cursor.execute(u'''INSERT INTO gps(lat,lon,alt) VALUES ({0}, {1}, {2})'''.format(lat, lon, alt))
        cnx.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(repr(e))
    print("SQL insert done")


def parseGPS(str):
    if str.find('GGA') > 0:
        try:
            msg = pynmea2.parse(str)
            if msg.lat is None:
                # print("pass")
                pass
            else:
                lat = msg.latitude
                lon = msg.longitude
                alt = msg.altitude
                sats = msg.num_sats
                db_insert(lat, lon, alt)
                global sleep_time
                global sleep_time2
                if int(sats) < 6:
                    sleep_time = 30
                elif sleep_time2 < 3600:
                    sleep_time2 += 300
                    sleep_time = sleep_time2
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            print(repr(e))
    else:
        sleep_time = 0.5


ser = serial.Serial("/dev/ttyS0", 9600, timeout=0.5)

while True:
    try:
        sleep(sleep_time)
        str = ser.readline().decode()
        parseGPS(str)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(repr(e))

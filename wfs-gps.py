# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import sys
import pynmea2
import serial
import mysql.connector
from time import sleep

sleep_time = 60


def db_insert(lat, lon, alt):
    cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
    cursor = cnx.cursor()
    cursor.execute(u'''INSERT INTO gps(lat,lon,alt) VALUES (%s)''' % lat, lon, alt)
    # cnx.commit()
    print("SQL insert done")
    sleep_time = 3600


def parseGPS(str):
    if str.find('GGA') > 0:
        try:
            msg = pynmea2.parse(str)
            if msg.lat is None:
                print("pass")
                # pass
            else:
                print("GGA received")
                lat = msg.latitude
                lon = msg.longitude
                alt = msg.altitude
                sats = msg.num_sats
                print(lat, lon, alt, sats)
                db_insert(lat, lon, alt)
            # print("Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s" % (msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            print(repr(e))


ser = serial.Serial("/dev/ttyS0", 9600, timeout=0.5)

while True:
    try:
        sleep(2)
        str = ser.readline().decode()
        #print(str)
        parseGPS(str)
        print(sleep_time)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(repr(e))

# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import sys
import pynmea2
import serial


def parseGPS(gpsstr):
    if gpsstr.find('GGA') > 0:
        msg = pynmea2.parse(gpsstr)
        print("Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s" % (msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units))


serialPort = serial.Serial("/dev/ttyS0", 9600)

while True:
    try:
        gpsstr = serialPort.readline()
        parseGPS(gpsstr)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(repr(e))

# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import pynmea2
import serial
import mysql.connector
from time import sleep
from pathlib import Path
from wfs_error_handling import error_handle

global satellites


def db_insert(lat, lon, alt):
	cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
	cursor = cnx.cursor()
	try:
		cursor.execute(u'''INSERT INTO gps(lat, lon, alt) VALUES ("{0}", "{1}", "{2}")'''.format(lat, lon, alt))
		cnx.commit()
	except Exception as e:
		filename = Path(__file__).name
		error_handle(e, filename)

	cursor.close()
	cnx.close()


def parse_gps(gps_sig):
	if gps_sig.find('GGA') > 0:
		msg = pynmea2.parse(gps_sig)
		if len(msg.lat) == 0:
			pass
		else:
			lat = msg.latitude
			lon = msg.longitude
			alt = msg.altitude
			global satellites
			satellites = msg.num_sats
			db_insert(lat, lon, alt)


def interval():
	sleep_time = 0
	if int(satellites) < 6:
		sleep_time = 120
	elif int(satellites) > 6:
		sleep_time = 3600

	return sleep_time


# ser = serial.Serial("/dev/ttyS0", 9600, timeout=0.5)
ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

while True:
	try:
		sleep(interval())
		gps = ser.readline().decode()
		parse_gps(gps)
	# except:
	# 	pass
	except Exception as e:
		pass
		filename = Path(__file__).name
		error_handle(e, filename)

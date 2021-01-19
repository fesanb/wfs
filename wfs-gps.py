# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import pynmea2
import serial
import mysql.connector

from time import sleep
from pathlib import Path
from wfs_error_handling import error_handle


# NOT IN USE ser = serial.Serial("/dev/ttyS0", 9600, timeout=0.5)


# fake_sig = "$GPGGA,045252.000,3014.4273,N,09749.0628,W,1,09,1.3,206.9,M,-22.5,M,,0000*6F"
# fake_sig1 = "$GPGGA,045104.000,3014.1985,N,09749.2873,W,1,09,1.2,211.6,M,-22.5,M,,0000*62"
# fake_sig2 = "$GPGGP,045252.000,3014.4273,N,09749.0628,W,1,09,1.3,206.9,M,-22.5,M,,0000*6F"
# fake_sig3 = ""


def db_insert(lat, lon, alt, sat):
	cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
	cursor = cnx.cursor()
	try:
		cursor.execute(u'''INSERT INTO gps(lat, lon, alt) VALUES ("{0}", "{1}", "{2}")'''.format(lat, lon, alt))
		cnx.commit()
	except Exception as e:
		cursor.close()
		cnx.close()
		filename = Path(__file__).name
		error_handle(e, filename)

	cursor.close()
	cnx.close()


def parse_gps(gps_sig):
	if gps_sig.find('GGA') > 0:
		msg = pynmea2.parse(gps_sig)
		if len(msg.lat) == 0:
			parse_gps.sig = False
		else:
			parse_gps.sig = True
			parse_gps.lat = msg.latitude
			parse_gps.lon = msg.longitude
			parse_gps.alt = msg.altitude
			parse_gps.sat = msg.num_sats
	else:
		parse_gps.sig = False


ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=2)

try:
	gps_iter = 0
	gps_list = []

	while gps_iter < 40:
		gps = ser.readline().decode()
		parse_gps(gps)  # random.choice([fake_sig, fake_sig1, fake_sig2, fake_sig3])

		if parse_gps.sig is True:
			gps_list.append([parse_gps.lat, parse_gps.lon, parse_gps.alt, parse_gps.sat])
			print(parse_gps.lat, parse_gps.lon, parse_gps.alt, parse_gps.sat)

		gps_iter += 1
		sleep(0.3)

	c1 = 0
	c2 = 0
	equal = 0
	equal_list = []

	print(len(gps_list))

	while c1 < len(gps_list):
		for i in gps_list:
			if gps_list[c1] == gps_list[c2]:
				equal += 1
			c2 += 1
		equal_list.append(equal)
		equal = 0
		c2 = 0
		c1 += 1

	print(len(equal_list))

	if len(equal_list) == 0:
		pass
	else:
		m = max(equal_list)
		equals = equal_list.count(max(equal_list))
		index = [i for i, j in enumerate(equal_list) if j == m]

		if equals > 5:
			insert = gps_list[index[0]]
			db_insert(insert[0], insert[1], insert[2], insert[3])

except Exception as e:
	filename = Path(__file__).name
	error_handle(e, filename)

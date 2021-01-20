# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import bme680
import time
import mysql.connector
from pathlib import Path
from wfs_error_handling import error_handle

s = bme680.BME680()
s.set_humidity_oversample(bme680.OS_16X)
s.set_pressure_oversample(bme680.OS_16X)
s.set_temperature_oversample(bme680.OS_16X)
s.set_filter(bme680.FILTER_SIZE_15)


def db_fetch():
	try:
		cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
		cursor = cnx.cursor(buffered=True)

		fetch_last_sens = "SELECT * FROM sens ORDER BY id DESC LIMIT 1, 1"
		cursor.execute(fetch_last_sens)
		if cursor.rowcount > 0:
			db_last_sens = cursor.fetchone()
			# db_fetch.temp = str(db_last_sens[1])
			# db_fetch.hum = str(round(db_last_sens[2]))
			# db_fetch.atp = str(db_last_sens[3])
			db_fetch.last_sens = [db_last_sens[1], db_last_sens[2], db_last_sens[3]]
		else:
			db_fetch.last_sens = []
	except Exception as e:
		filename = Path(__file__).name
		error_handle(e, filename)


def db_insert(temp, hum, atp):
	cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
	cursor = cnx.cursor()
	try:
		cursor.execute(u'''INSERT INTO sens(temp, hum, atp) VALUES ({0}, {1}, {2})'''.format(temp, hum, atp))
		cnx.commit()
	except Exception as e:
		filename = Path(__file__).name
		error_handle(e, filename)

	cursor.close()
	cnx.close()


new_sens = [round(s.data.temperature), round(s.data.humidity), round(s.data.pressure)]
db_fetch()
print(db_fetch.last_sens)
print(new_sens)
if new_sens == db_fetch.last_sens:
	print("they are the same")

if s.get_sensor_data() is None:
	pass
else:
	if new_sens == db_fetch.last_sens:
		pass
	else:
		db_insert(new_sens[0], new_sens[1], new_sens[2])



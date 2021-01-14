# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import bme680
import time
import mysql.connector
from pathlib import Path
from wfs_error_handling import error_handle

sensor = bme680.BME680()
# all bme680 setting are set in different file on boot of unit


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


last_sens = []


new_sens = [round(sensor.data.temperature, 1), round(sensor.data.humidity), round(sensor.data.pressure)]
if sensor.get_sensor_data() is None:
	pass
else:
	db_insert(new_sens[0], new_sens[1], new_sens[2])
	last_sens = new_sens
	del last_sens[-1]


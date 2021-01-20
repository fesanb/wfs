# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import mysql.connector
from datetime import timedelta, datetime


def make_mean():
	try:
		cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
		cursor = cnx.cursor(buffered=True)

		cursor.execute("SELECT AVG(wind) FROM wind  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 10 MINUTE)")
		db_mean = cursor.fetchone()
		if db_mean[0] is None:
			pass
		else:
			add_mean = (u'''INSERT INTO mean(mean) VALUES (%s)''' % (round(db_mean[0], 2)))
			cursor.execute(add_mean)
			emp_no = cursor.lastrowid
			cnx.commit()
	except Exception as e:
		filename = Path(__file__).name
		error_handle(e, filename)

	cursor.close()
	cnx.close()

make_mean()

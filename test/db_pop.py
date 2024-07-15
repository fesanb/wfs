import mysql.connector
import time
# import datetime
from datetime import timedelta, datetime
from random import random, randrange, uniform


def wind_insert(wind):
	cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
	cursor = cnx.cursor()
	cursor.execute(u'''INSERT INTO wind(wind) VALUES ({0})'''.format(wind))
	cnx.commit()


def sens_insert(temp, hum, atp):
	cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
	cursor = cnx.cursor()
	cursor.execute(u'''INSERT INTO sens(temp, hum, atp) VALUES ({0}, {1}, {2})'''.format(temp, hum, atp))
	cnx.commit()


def clean_db():
	try:
		cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
		cursor = cnx.cursor(buffered=True)

		tw = "TRUNCATE wind"
		tm = "TRUNCATE mean"
		tc = "TRUNCATE sens"

		cursor.execute(tw)
		cursor.execute(tm)
		cursor.execute(tc)

		cursor.close()
		cnx.close()
		print("DB is Clean")

	except Exception as e:
		print(e)


def build_db():
	try:
		cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
		cursor = cnx.cursor(buffered=True)

		tm = datetime.now() - timedelta(hours=24)

		while tm < datetime.now():
			tm = tm + timedelta(minutes=10)
			wind = round(uniform(3, 8), 1)
			temp = round(uniform(18, 19), 1)
			hum = round(uniform(40, 45), 0)
			atp = round(uniform(980, 1020), 0)

			cursor.execute(u'''INSERT INTO mean(mean, tmestmp) VALUES ({0}, "{1}")'''.format(wind, str(tm)))
			cnx.commit()

			cursor.execute(u'''INSERT INTO sens(temp, hum, atp, tmestmp) VALUES ({0}, {1}, {2}, "{3}")'''.format(temp, hum, atp, tm))
			cnx.commit()

		print("DB build complete")
		print("")

	except Exception as e:
		print(e)


clean_db()
build_db()

while True:
	# seed(1)
	wind = round(uniform(3, 8), 1)
	temp = round(uniform(18, 19), 1)
	hum = round(uniform(40, 45), 0)
	atp = round(uniform(980, 1020), 0)

	wind_insert(wind)
	sens_insert(temp, hum, atp)
	print("Single DB insert done")

	time.sleep(30)

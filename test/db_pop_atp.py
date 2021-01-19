import mysql.connector
import time
# import datetime
from datetime import timedelta, datetime
from random import random, randrange, uniform


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

		tm = datetime.now() - timedelta(hours=2.5)
		atp = [881, 881, 881, 881, 880]
		i = 0
		while len(atp) > i:
			print(i)
			tm = tm + timedelta(minutes=25)

			wind = round(uniform(3, 8), 1)
			temp = round(uniform(18, 19), 1)
			hum = round(uniform(40, 45), 0)

			cursor.execute(u'''INSERT INTO mean(mean, tmestmp) VALUES ({0}, "{1}")'''.format(wind, str(tm)))
			cnx.commit()

			cursor.execute(u'''INSERT INTO sens(temp, hum, atp, tmestmp) VALUES ({0}, {1}, {2}, "{3}")'''.format(temp, hum, atp[i], tm))
			cnx.commit()

			i += 1

		print("DB build complete")
		print("")

	except Exception as e:
		print(e)


clean_db()
build_db()
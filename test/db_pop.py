import mysql.connector
import time
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


while True:
	# seed(1)
	wind = round(uniform(3, 8), 1)
	temp = round(uniform(18, 19), 1)
	hum = round(uniform(40, 45), 0)
	atp = round(uniform(1003, 1009), 0)

	wind_insert(wind)
	sens_insert(temp, hum, atp)
	print("insert done")

	time.sleep(10)

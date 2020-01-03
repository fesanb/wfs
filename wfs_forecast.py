# WFS - Weather Forecast Station
# Written by Stefan Bahrawy
# - File: ww - Weather Warning

import mysql.connector
from datetime import datetime, timedelta
import time

cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
cursor = cnx.cursor(buffered=True)


def forecast():
	fetch_atp = "SELECT atp, tmestmp FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 3 HOUR)"
	# fetch_atp = "SELECT atp, tmestmp FROM sens ORDER BY id DESC LIMIT 10"

	cursor.execute(fetch_atp)
	if cursor.rowcount > 0:
		db_atp = cursor.fetchall()
		split_atp = [i[0] for i in db_atp]
		split_timestamp = [i[1] for i in db_atp]

		if split_atp[0] < split_atp[len(split_atp)-1]:
			# print("Expect wetter conditions")
			expect = "Expect wetter conditions"

		if split_atp[0] > split_atp[len(split_atp)-1]:
			# print("Expect dryer conditions")
			expect = "Expect wetter conditions"

		i = 0
		print(len(split_timestamp))
		while split_timestamp[0] - split_timestamp[i] < timedelta(hours=1):
			i += 1
			if i > len(split_atp)-1:
				break
		change = abs(split_atp[0]-split_atp[i])

		if change > 1:
			# print("Small weather change")
			# print("Beaufort 3-5")
			change1 = "Small weather change"
			change2 = "Beaufort 3-5"
		elif change > 2:
			# print("Moderate weather change")
			# print("Beaufort 5-7")
			change1 = "Moderate weather change"
			change2 = "Beaufort 5-7"
		elif change > 3:
			# print("Great weather change")
			# print("Beaufort 8-10")
			change1 = "Great weather change"
			change2 = "Beaufort 8-10"

		return expect, change1, change2


forecast()

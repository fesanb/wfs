# WFS - Weather Forecast Station
# Written by Stefan Bahrawy
# - File: ww - Weather Warning

import mysql.connector
from datetime import datetime, timedelta
import time


def forecast():
	cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
	cursor = cnx.cursor(buffered=True)

	fetch_atp_3hr = "SELECT atp, tmestmp FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 3 HOUR)"
	fetch_atp_1hr = "SELECT atp, tmestmp FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)"
	# fetch_atp = "SELECT atp, tmestmp FROM sens ORDER BY id DESC LIMIT 10"

	expect = "-"
	change1 = "-"
	change2 = "-"

	cursor.execute(fetch_atp_1hr)
	if cursor.rowcount > 0:
		db_atp = cursor.fetchall()
		split_atp = [i[0] for i in db_atp]
		split_timestamp = [i[1] for i in db_atp]

		if split_atp[0] < split_atp[len(split_atp)-1]:
			# print("Expect wetter conditions")
			expect = "dryer"

		if split_atp[0] > split_atp[len(split_atp)-1]:
			# print("Expect dryer conditions")
			expect = "wetter"

		i = 0

		while split_timestamp[0] - split_timestamp[i] < timedelta(hours=1):
			i += 1
			if i > len(split_atp)-1:
				i -= 1
				break
		change = abs(split_atp[0]-split_atp[i])

		if change > 3:
			# print("Great weather change")
			# print("Beaufort 8-10")
			change1 = "Greater"
			change2 = "8-10"
		elif change > 2:
			# print("Moderate weather change")
			# print("Beaufort 5-7")
			change1 = "Moderate"
			change2 = "5-7"
		elif change > 1:
			# print("Small weather change")
			# print("Beaufort 3-5")
			change1 = "Smaller"
			change2 = "3-5"
		elif change < 1:
			# print("Small weather change")
			# print("Beaufort 3-5")
			change1 = "None"
			change2 = "As is"

	return expect, change1, change2


forecast()

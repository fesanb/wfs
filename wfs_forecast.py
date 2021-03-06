# WFS - Weather Forecast Station
# Written by Stefan Bahrawy
# - File: ww - Weather Warning

import mysql.connector


def fc():
	eval_wind_1hr = "--"
	conditions = "--"

	fetch_atp_12hr = "SELECT atp, tmestmp FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
	fetch_atp_3hr = "SELECT atp, tmestmp FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 3 HOUR)"
	fetch_atp_1hr = "SELECT atp, tmestmp FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)"
	# fetch_atp = "SELECT atp, tmestmp FROM sens ORDER BY id DESC LIMIT 10"

	cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
	cursor = cnx.cursor(buffered=True)

	cursor.execute(fetch_atp_1hr)
	if cursor.rowcount > 0:
		one_hour = cursor.fetchall()
		atp_1hr = [i[0] for i in one_hour]
		# atp_1hr_timestamp = [i[1] for i in one_hour]
		change_1hr = atp_1hr[len(atp_1hr) - 1] - atp_1hr[0]

	else:
		one_hour = []
		change_1hr = 0

	cursor.execute(fetch_atp_3hr)
	if cursor.rowcount > 0:
		three_hour = cursor.fetchall()
		atp_3hr = [i[0] for i in three_hour]
		# atp_3hr_timestamp = [i[1] for i in three_hour]
		change_3hr = atp_3hr[len(atp_3hr) - 1] - atp_3hr[0]

		if atp_3hr[0] < atp_3hr[len(atp_3hr) - 1]:
			# print("Expect wetter conditions")
			conditions = "Dryer conditions"

		if atp_3hr[0] > atp_3hr[len(atp_3hr) - 1]:
			# print("Expect dryer conditions")
			conditions = "Wetter conditions"
	else:
		three_hour = []
		change_3hr = 0

	# cursor.execute(fetch_atp_12hr)
	# if cursor.rowcount > 0:
	# 	twelve_hour = cursor.fetchall()
	# 	atp_12hr = [i[0] for i in twelve_hour]
	# 	atp_12hr_timestamp = [i[1] for i in twelve_hour]
	# 	change_12hr = atp_12hr[0] - atp_12hr[len(atp_12hr) - 1]
	# else:
	# 	twelve_hour = []

	# print("1hr", change_1hr)
	# print("3hr", change_3hr)
	# print("")

	cnx.close()

	# print(conditions)

	if change_1hr == 0:
		eval_wind_1hr = "No Change"
	elif change_1hr > 3:
		eval_wind_1hr = "Winds: > 24m/s"
	elif change_1hr > 2:
		eval_wind_1hr = "Winds: 17 - 24m/s"
	elif change_1hr > 1:
		eval_wind_1hr = "Winds: 10 - 17m/s"
	elif change_1hr < -2:
		eval_wind_1hr = "Winds: > 24m/s"
	elif change_1hr < -1:
		eval_wind_1hr = "Winds: 17 - 24m/s"
	elif change_1hr > -2 or change_1hr < 1:
		eval_wind_1hr = "Winds: 0 - 10m/s"

	# print(eval_wind_1hr)

	if change_3hr == 0:
		eval_wind_3hr = "No Change"
	elif change_3hr > 10:
		eval_wind_3hr = "Winds: > 24m/s"
	elif change_3hr > 9:
		eval_wind_3hr = "Winds: 17 - 24m/s"
	elif change_3hr > 4:
		eval_wind_3hr = "Winds: 10 - 17m/s"
	elif change_3hr < -6:
		eval_wind_3hr = "Winds: > 24m/s"
	elif change_3hr < -6:
		eval_wind_3hr = "Winds: 17 - 24m/s"
	elif change_3hr > -4 or change_3hr < 4:
		eval_wind_3hr = "Winds: 0 - 10m/s"

	# print(eval_wind_3hr)

	eval_wind = "No data"

	if change_1hr >= change_3hr:
		eval_wind = eval_wind_1hr

	if change_3hr > change_1hr:
		eval_wind = eval_wind_3hr

	return eval_wind, conditions

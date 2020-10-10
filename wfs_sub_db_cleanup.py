# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import mysql.connector
from datetime import timedelta, datetime

cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
cursor = cnx.cursor(buffered=True)


#def store_values_before_clean():
	# Check and insert max / min values to db.


def reduce_mean_table():
	while True:
		# reduce records to only one pr 10min.
		find_min_row = "SELECT MIN(tmestmp) FROM mean WHERE red IS NULL"
		cursor.execute(find_min_row)

		db_mean = cursor.fetchone()
		if db_mean[0] is None:
			break
		min_row = db_mean[0]
		min_row += timedelta(minutes=10)

		find_rows = "SELECT id, mean, tmestmp FROM mean WHERE red IS NULL AND tmestmp <= '{0}'".format(min_row)
		cursor.execute(find_rows)
		db_list = cursor.fetchall()

		r = []
		id = []

		for i in db_list:
			r.append(i[1])
			id.append(i[0])

		red = sum(r) / len(r)

		insert_red_val = "UPDATE mean SET mean = '{0}', red = 1 WHERE id = '{1}' ".format(red, max(id))
		cursor.execute(insert_red_val)
		cnx.commit()
		del id[-1]
		for g in id:
			delete_rows = "DELETE FROM mean where id = '{0}'".format(g)
			cursor.execute(delete_rows)
			cnx.commit()


def delete_sens():
	delete = "DELETE FROM sens WHERE issame = 1 AND tmestmp <= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
	cursor.execute(delete)
	cnx.commit()


def cleanup_old_wind():
	delete = "DELETE FROM wind WHERE tmestmp <= DATE_SUB(NOW(), INTERVAL 10 DAY)"
	cursor.execute(delete)
	cnx.commit()


# alter table mean add red int(1)

reduce_mean_table()
cleanup_old_wind()
delete_sens()

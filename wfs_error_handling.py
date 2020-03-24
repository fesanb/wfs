import sys
import mysql.connector
from pathlib import Path


def error_handle(e, file):
	try:
		cnx
	except NameError:
		pass
	else:
		cnx.close()
		print("Mysql Connection Closed due to error")

	# filename = Path(__file__).name
	exc_type, exc_obj, exc_tb = sys.exc_info()

	cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
	cursor = cnx.cursor(buffered=True)

	add_error = (u'''INSERT INTO 
    error(file, type, obj, line) 
    VALUES ("{0}", "{1}", "{2}", {3}) '''
				 .format(file, exc_type, exc_obj, exc_tb.tb_lineno))

	cursor.execute(add_error)
	cnx.commit()

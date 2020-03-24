# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import mysql.connector

cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
cursor = cnx.cursor(buffered=True)


def delete_sens(self):
	delete = "DELETE FROM sens WHERE issame = 1 AND tmestmp <= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
	self.cursor.execute(delete)
	self.cnx.commit()

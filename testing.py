import sys
import mysql.connector
import threading
import time


get_wind = "SELECT * FROM wind WHERE id=(SELECT MAX(id) FROM wind)"


class GetData(object):
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.mysql_fetch, args=())
        thread.daemon = True
        thread.start()

        self.query = query

    def mysql_fetch(self, query):
        cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        time.sleep(self.interval)
        return result


print(GetData.mysql_fetch(get_wind))

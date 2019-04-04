import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import pyqtgraph as pg
import mysql.connector
import threading
import time
from datetime import datetime

get_graph_wind_timestamp = "SELECT CAST(tmestmp AS CHAR) FROM wind WHERE id=(SELECT MAX(id) FROM wind)"


cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
cursor = cnx.cursor(buffered=True)

cursor.execute(get_graph_wind_timestamp)
db_graph_timestamp = cursor.fetchone()
print(db_graph_timestamp[0])
t = datetime.strptime(str(db_graph_timestamp[0]),"%Y-%m-%d %H:%M:%S")
print(t)
#fetch_graph.graphwind_X = t

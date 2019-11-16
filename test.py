import sys, os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import pyqtgraph as pg
import mysql.connector
import threading
import time
from datetime import datetime
from datetime import timedelta

cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
cursor = cnx.cursor(buffered=True)

cursor.execute("SELECT * FROM wind WHERE id=(SELECT MAX(id) FROM wind)")
if cursor.rowcount > 0:
    db_graph_wind = cursor.fetchone()

    print(db_graph_wind[2])

    print(time.mktime(db_graph_wind[2].timetuple()))

    # graphwind_X = []
    # graphwind_Y = []
    #
    # for i in db_graph_wind:
    #     graphwind_X.append(time.mktime(i[0].timetouple))
    #     graphwind_Y.append(i[1])

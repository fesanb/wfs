# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

# imports
import gc
import numpy as np
import mysql.connector
import pyqtgraph as pg
import sys, os
import threading
import time


# import psutil
try:
	import psutil
	ps = True
except:
	ps = False

# froms
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime, timedelta
from pathlib import Path

# custom imports
from wfs_sub_graph import graph_plot, graph_update
from wfs_error_handling import error_handle
from wfs_forecast import fc


# Wind
get_wind = "SELECT * FROM wind WHERE id=(SELECT MAX(id) FROM wind)"


# GRAPH
interval = 12
get_graph_wind = "SELECT mean, UNIX_TIMESTAMP(tmestmp) FROM mean WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL {} HOUR)".format(interval)
get_graph_atp = "SELECT atp, UNIX_TIMESTAMP(tmestmp) FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL {} HOUR)".format(interval)
get_graph_hum = "SELECT hum, UNIX_TIMESTAMP(tmestmp) FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL {} HOUR)".format(interval)
get_graph_temp = "SELECT temp, UNIX_TIMESTAMP(tmestmp) FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL {} HOUR)".format(interval)

# SENS
get_sens = "SELECT * FROM sens WHERE id=(SELECT MAX(id) FROM sens)"
get_gps = "SELECT * FROM gps WHERE id=(SELECT MAX(id) FROM gps) AND tmestmp >= DATE_SUB(NOW(), INTERVAL 65 MINUTE)"


def fetch_wind():
	try:
		cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
		cursor = cnx.cursor(buffered=True)

		cursor.execute(get_wind)
		if cursor.rowcount > 0:
			db_wind = cursor.fetchone()
			fetch_wind.wind = str(db_wind[1])
			fetch_wind.timestamp = db_wind[2]

			if fetch_wind.timestamp < datetime.now() - timedelta(minutes=0.25):
				fetch_wind.wind = "-.-"

		else:
			fetch_wind.wind = "-.-"

		cursor.close()
		cnx.close()

	except Exception as e:
		filename = Path(__file__).name
		error_handle(e, filename)
		# print(e)

def fetch_mean():

	try:
		# get_mean_wind = "SELECT AVG(mean) FROM mean  WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 10 MINUTE)"
		get_mean_wind = "SELECT mean FROM mean WHERE id=(SELECT MAX(id) FROM mean) AND tmestmp >= DATE_SUB(NOW(), INTERVAL 11 MINUTE)"

		cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
		cursor = cnx.cursor(buffered=True)

		cursor.execute(get_mean_wind)
		db_mean_wind = cursor.fetchone()
		if cursor.rowcount is 0: #db_mean_wind[0] is None:  # cursor.rowcount is 0 and
			fetch_mean.meanwind = "-.-"
			fetch_mean.beaufortLS = "no data last 10 min..."
		else:
			fetch_mean.meanwind = round(float(db_mean_wind[0]), 1)

			if float(fetch_mean.meanwind) < 0.3:
				fetch_mean.beaufortLS = "Beaufort 0 - Calm"
			elif float(fetch_mean.meanwind) > 32.7:
				fetch_mean.beaufortLS = "Beaufort 12 - Hurricane"
			elif float(fetch_mean.meanwind) > 28.5:
				fetch_mean.beaufortLS = "Beaufort 11 - Violent Storm"
			elif float(fetch_mean.meanwind) > 24.5:
				fetch_mean.beaufortLS = "Beaufort 10 - Storm"
			elif float(fetch_mean.meanwind) > 20.8:
				fetch_mean.beaufortLS = "Beaufort 9 - Strong Gale"
			elif float(fetch_mean.meanwind) > 17.2:
				fetch_mean.beaufortLS = "Beaufort 8 - Fresh Gale"
			elif float(fetch_mean.meanwind) > 13.9:
				fetch_mean.beaufortLS = "Beaufort 7 - Moderate gale"
			elif float(fetch_mean.meanwind) > 10.8:
				fetch_mean.beaufortLS = "Beaufort 6 - Strong breeze"
			elif float(fetch_mean.meanwind) > 8.0:
				fetch_mean.beaufortLS = "Beaufort 5 - Fresh breeze"
			elif float(fetch_mean.meanwind) > 5.5:
				fetch_mean.beaufortLS = "Beaufort 4 - Moderate breeze"
			elif float(fetch_mean.meanwind) > 3.4:
				fetch_mean.beaufortLS = "Beaufort 3 - Gentle breeze"
			elif float(fetch_mean.meanwind) > 1.6:
				fetch_mean.beaufortLS = "Beaufort 2 - Light breeze"
			elif float(fetch_mean.meanwind) > 0.3:
				fetch_mean.beaufortLS = "Beaufort 1 - Light Air"

	except Exception as e:
		filename = Path(__file__).name
		error_handle(e, filename)

	cursor.close()
	cnx.close()
	end = time.time()

def fetch_statistics():

	# Max
	get_max_wind24 = "SELECT MAX(wind) FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
	get_max_wind12 = "SELECT MAX(wind) FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 12 HOUR)"
	get_max_wind6 = "SELECT MAX(wind) FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 6 HOUR)"
	get_max_wind3 = "SELECT MAX(wind) FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 3 HOUR)"
	get_max_wind1 = "SELECT MAX(wind) FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)"
	peak_wind = "SELECT MAX(wind) FROM wind WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 10 MINUTE)"

	try:
		cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
		cursor = cnx.cursor(buffered=True)

		cursor.execute(peak_wind)
		db_wind = cursor.fetchone()
		if db_wind[0] is None:
			fetch_statistics.peak_wind = "0.0"
		else:
			fetch_statistics.peak_wind = str(round(db_wind[0], 1))

		cursor.execute(get_max_wind1)
		db_wind = cursor.fetchone()
		if db_wind[0] is None:
			fetch_statistics.max1 = "0.0"
		else:
			fetch_statistics.max1 = str(round(db_wind[0], 1))

		cursor.execute(get_max_wind3)
		db_wind = cursor.fetchone()
		if db_wind[0] is None:
			fetch_statistics.max3 = "0.0"
		else:
			fetch_statistics.max3 = str(round(db_wind[0], 1))

		cursor.execute(get_max_wind6)
		db_wind = cursor.fetchone()
		if db_wind[0] is None:
			fetch_statistics.max6 = "0.0"
		else:
			fetch_statistics.max6 = str(round(db_wind[0], 1))

		cursor.execute(get_max_wind12)
		db_wind = cursor.fetchone()
		if db_wind[0] is None:
			fetch_statistics.max12 = "0.0"
		else:
			fetch_statistics.max12 = str(round(db_wind[0], 1))

		cursor.execute(get_max_wind24)
		db_wind = cursor.fetchone()
		if db_wind[0] is None:
			fetch_statistics.max24 = "0.0"
		else:
			fetch_statistics.max24 = str(round(db_wind[0], 1))

		cursor.close()
		cnx.close()

	except Exception as e:
		filename = Path(__file__).name
		error_handle(e, filename)
		# print(e)

def fetch_sens():
	fetch_sens.current_sens = None
	try:
		cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
		cursor = cnx.cursor(buffered=True)

		cursor.execute(get_sens)
		if cursor.rowcount > 0:
			db_sens = cursor.fetchone()
			fetch_sens.temp = str(db_sens[1])
			fetch_sens.hum = str(db_sens[2])
			fetch_sens.atp = str(db_sens[3])
			fetch_sens.sens_timestamp = str(db_sens[5])
			fetch_sens.current_sens = []
			for i in db_sens:
				fetch_sens.current_sens.append(i)


		else:
			fetch_sens.temp = "0"
			fetch_sens.hum = "0"
			fetch_sens.atp = "0"
			fetch_sens.sens_timestamp = "0"
			fetch_sens.current_sens = []

	except Exception as e:
		filename = Path(__file__).name
		error_handle(e, filename)

	cursor.close()
	cnx.close()

def fetch_gps():
	try:
		cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
		cursor = cnx.cursor(buffered=True)

		cursor.execute(get_gps)
		if cursor.rowcount > 0:
			db_gps = cursor.fetchone()
			fetch_gps.lat = str(db_gps[1])
			fetch_gps.long = str(db_gps[2])
			fetch_gps.alt = str(db_gps[3])
			fetch_gps.gps_timestamp = str(db_gps[4])
		else:
			fetch_gps.lat = "No gps signal"
			fetch_gps.long = "No gps signal"
			fetch_gps.alt = "No gps signal"
			fetch_gps.gps_timestamp = "-"

	except Exception as e:
		filename = Path(__file__).name
		error_handle(e, filename)

	cursor.close()
	cnx.close()

def fg():
	# print("fetch graph")
	fg.gw_x = None
	fg.gw_y = None
	fg.ga_x = None
	fg.ga_y = None
	fg.gt_x = None
	fg.gt_y = None
	fg.gh_x = None
	fg.gh_y = None
	try:
		cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
		cursor = cnx.cursor(buffered=True)

		cursor.execute(get_graph_wind)
		if cursor.rowcount > 0:
			db_graph_wind = cursor.fetchall()
			fg.gw_x = []
			fg.gw_y = []

			for i in db_graph_wind:
				fg.gw_x.append(i[1])
				fg.gw_y.append(i[0])

		else:
			fg.gw_x = []
			fg.gw_y = []
			fg.gw_x.append(time.time())
			fg.gw_y.append(0)

		# atp
		cursor.execute(get_graph_atp)
		if cursor.rowcount > 0:
			db_graph_atp = cursor.fetchall()
			fg.ga_x = []
			fg.ga_y = []

			for i in db_graph_atp:
				fg.ga_x.append(i[1])
				fg.ga_y.append(i[0])

		else:
			fg.ga_x = []
			fg.ga_y = []
			fg.ga_x.append(time.time())
			fg.ga_y.append(0)

		# hum
		cursor.execute(get_graph_hum)
		if cursor.rowcount > 0:
			db_graph_hum = cursor.fetchall()
			fg.gh_x = []
			fg.gh_y = []

			for i in db_graph_hum:
				fg.gh_x.append(i[1])
				fg.gh_y.append(i[0])

		else:
			fg.gh_x = []
			fg.gh_y = []
			fg.gh_x.append(time.time())
			fg.gh_y.append(0)
		# temp
		cursor.execute(get_graph_temp)
		if cursor.rowcount > 0:
			db_graph_temp = cursor.fetchall()
			fg.gt_x = []
			fg.gt_y = []

			for i in db_graph_temp:
				fg.gt_x.append(i[1])
				fg.gt_y.append(i[0])

		else:
			fg.gt_x = []
			fg.gt_y = []
			fg.gt_x.append(time.time())
			fg.gt_y.append(0)

	except Exception as e:
		filename = Path(__file__).name
		error_handle(e, filename)

	cursor.close()
	cnx.close()

def sens_arrow(sens_type):
	fetch_last_sens = "SELECT * FROM sens ORDER BY id DESC LIMIT 3"

	try:
		cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
		cursor = cnx.cursor(buffered=True)

		cursor.execute(fetch_last_sens)
		if cursor.rowcount > 0:
			db_last_sens = cursor.fetchall()
			temp = [a[1] for a in db_last_sens]
			hum = [a[2] for a in db_last_sens]
			atp = [a[3] for a in db_last_sens]

		sens_col = [temp[::-1], hum[::-1], atp[::-1]]

	except Exception as e:
		filename = Path(__file__).name
		error_handle(e, filename)


	t = (sum(sens_col[sens_type]) / len(sens_col[sens_type])) - sens_col[sens_type][2]

	if t > 0:
		img = "arrow_down.png"
		return img

	if t < 0:
		img = "arrow_up.png"
		return img

	if t == 0:
		img = "arrow_flat.png"
		return img

	cursor.close()
	cnx.close()

def error_light():
	fetch_error = "SELECT * FROM error WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL 10 MINUTE)"

	try:
		cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
		cursor = cnx.cursor(buffered=True)

		cursor.execute(fetch_error)
		if cursor.rowcount > 0:
			light = "error-red.png"
		else:
			light = "error-green.png"

		return light

	except Exception as e:
		filename = Path(__file__).name
		error_handle(e, filename)

	cursor.close()
	cnx.close()

thread_fetch_wind = threading.Thread(target=fetch_wind, args=())
thread_fetch_wind.daemon = True
thread_fetch_wind.start()

thread_mean = threading.Thread(target=fetch_mean, args=())
thread_mean.daemon = True
thread_mean.start()

thread_statistics = threading.Thread(target=fetch_statistics, args=())
thread_statistics.daemon = True
thread_statistics.start()

thread_fetch_sens = threading.Thread(target=fetch_sens, args=())
thread_fetch_sens.daemon = True
thread_fetch_sens.start()

thread_fetch_gps = threading.Thread(target=fetch_gps, args=())
thread_fetch_gps.daemon = True
thread_fetch_gps.start()

thread_fetch_graph = threading.Thread(target=fg, args=())
thread_fetch_graph.daemon = True
thread_fetch_graph.start()

thread_error_light = threading.Thread(target=error_light, args=())
thread_error_light.daemon = True
thread_error_light.start()

time.sleep(2)

class App(QWidget):

	def __init__(self, parent=None):
		super(App, self).__init__(parent=parent)
		self.title = "WFS - Weather Forecast Station"
		self.setWindowIcon(QIcon("img/drawing.svg.png"))
		self.setWindowTitle(self.title)
		self.setStyleSheet("color: white; background-color: black;")

		if ps is True:
			self.showFullScreen()
		else:
			self.left = 0
			self.top = 0
			self.width = 720
			self.height = 480
			self.setGeometry(self.left, self.top, self.width, self.height)

		self.initUI()

	def initUI(self):

		path = str(Path(__file__).parent.absolute())

		self.O1 = QVBoxLayout(self)
		self.mainContainer = QHBoxLayout(self)
		self.windContainer = QVBoxLayout(self)

		try:  # Wind box

			self.windBox = QHBoxLayout()
			self.windFrame = QFrame(self)
			self.wind_VL = QVBoxLayout(self.windFrame)
			self.windL = QLabel(fetch_wind.wind, self.windFrame)
			img = path + "/img/wc_wind.png"
			self.windL.setStyleSheet("background-image: url({}); "
									 "background-repeat: no-repeat; "
									 "background-position: center".format(img))
			self.windL.setAlignment(Qt.AlignCenter)
			self.windL.setMinimumHeight(200)
			self.windL.setFont(QFont('Arial', 50))
			self.wind_VL.addWidget(self.windL)
			self.windBox.addWidget(self.windFrame)

			self.meanFrame = QFrame(self)
			self.mean_VL = QVBoxLayout(self.meanFrame)
			self.meanL = QLabel(str(fetch_mean.meanwind), self.meanFrame)
			img = path + "/img/wc_mean.png"
			self.meanL.setStyleSheet("background-image: url({}); "
									 "background-repeat: no-repeat; "
									 "background-position: center".format(img))
			self.meanL.setAlignment(Qt.AlignCenter)
			self.meanL.setMinimumHeight(200)
			self.meanL.setFont(QFont('Arial', 50))
			self.mean_VL.addWidget(self.meanL)
			self.windBox.addWidget(self.meanFrame)

			self.windContainer.addLayout(self.windBox)

		except Exception as e:
			filename = Path(__file__).name
			error_handle(e, filename)

		# Bauforth box
		self.beaufortbox = QHBoxLayout()
		self.beaufortL = QLabel(str(fetch_mean.beaufortLS))
		self.beaufortL.setAlignment(Qt.AlignHCenter)
		self.beaufortL.setMinimumHeight(40)
		self.beaufortL.setFont(QFont('Arial', 20))
		self.beaufortbox.addWidget(self.beaufortL)
		self.windContainer.addLayout(self.beaufortbox)

		#GRAPH
		self.graphContainer = QVBoxLayout()
		self.graph = graph_plot(fg.gw_x, fg.gw_y, fg.ga_y)
		self.graphContainer.addWidget(self.graph)
		self.windContainer.addLayout(self.graphContainer)
		self.windContainer.addStretch()
		self.mainContainer.addLayout(self.windContainer)

		# sens container
		self.sensFrame = QFrame(self)
		self.sensBox = QVBoxLayout(self.sensFrame)

		self.sensheaderBox = QHBoxLayout(self.sensFrame)
		self.sensHL = QLabel("SENSOR")
		self.sensHL.setFont(QFont('Arial', 15))
		self.sensheaderBox.addWidget(self.sensHL)
		self.sensBox.addLayout(self.sensheaderBox)

		self.sensgrid = QGridLayout()
		self.sensBox.addLayout(self.sensgrid)

		self.tempimg = QPixmap(path + '/img/ico-generic.png')
		self.tempico = QLabel()
		self.tempico.setPixmap(self.tempimg)
		self.tempvalue = QLabel(fetch_sens.temp + " °C")
		self.tempvalue.setFont(QFont('Arial', 13))
		self.tempimgarrow = QPixmap(path + '/img/' + sens_arrow(0))
		self.temparrow = QLabel()
		self.temparrow.setPixmap(self.tempimgarrow)

		self.sensgrid.addWidget(self.tempico, 0, 0, Qt.AlignCenter)
		self.sensgrid.addWidget(self.tempvalue, 0, 1, Qt.AlignCenter)
		self.sensgrid.addWidget(self.temparrow, 0, 2, Qt.AlignCenter)

		self.humimg = QPixmap(path + '/img/ico-generic.png')
		self.humico = QLabel()
		self.humico.setPixmap(self.humimg)
		self.humvalue = QLabel(fetch_sens.hum + " %")
		self.humvalue.setFont(QFont('Arial', 13))
		self.humimgarrow = QPixmap(path + '/img/' + sens_arrow(1))
		self.humarrow = QLabel()
		self.humarrow.setPixmap(self.humimgarrow)

		self.sensgrid.addWidget(self.humico, 1, 0, Qt.AlignCenter)
		self.sensgrid.addWidget(self.humvalue, 1, 1, Qt.AlignCenter)
		self.sensgrid.addWidget(self.humarrow, 1, 2, Qt.AlignCenter)

		self.atpimg = QPixmap(path + '/img/ico-generic.png')
		self.atpico = QLabel()
		self.atpico.setPixmap(self.atpimg)
		self.atpvalue = QLabel(fetch_sens.atp + " hPa")
		self.atpvalue.setFont(QFont('Arial', 13))
		self.atpimgarrow = QPixmap(path + '/img/' + sens_arrow(2))
		self.atparrow = QLabel()
		self.atparrow.setPixmap(self.atpimgarrow)

		self.sensgrid.addWidget(self.atpico, 2, 0, Qt.AlignCenter)
		self.sensgrid.addWidget(self.atpvalue, 2, 1, Qt.AlignCenter)
		self.sensgrid.addWidget(self.atparrow, 2, 2, Qt.AlignCenter)

		self.sensgrid.setRowStretch(3,50)
		self.sensBox.addLayout(self.sensgrid)

		#wind info container
		try:

			self.peak = QLabel("Peak:      NA m/s")
			self.max1 = QLabel("Max 1hr:   NA m/s")
			self.max3 = QLabel("Max 3hr:   NA m/s")
			self.max6 = QLabel("Max 6hr:   NA m/s")
			self.max12 = QLabel("Max 12hr: NA m/s")
			self.max24 = QLabel("Max 24hr: NA m/s")

			self.statistic = QVBoxLayout(self.sensFrame)

			self.peak = QLabel("Peak:      " + fetch_statistics.peak_wind + " m/s")
			self.max1 = QLabel("Max 1hr:   " + fetch_statistics.max1 + " m/s")
			self.max3 = QLabel("Max 3hr:   " + fetch_statistics.max3 + " m/s")
			self.max6 = QLabel("Max 6hr:   " + fetch_statistics.max6 + " m/s")
			self.max12 = QLabel("Max 12hr: " + fetch_statistics.max12 + " m/s")
			self.max24 = QLabel("Max 24hr: " + fetch_statistics.max24 + " m/s")

			self.statistic.addWidget(self.peak)
			self.statistic.addWidget(self.max1)
			self.statistic.addWidget(self.max3)
			self.statistic.addWidget(self.max6)
			self.statistic.addWidget(self.max12)
			self.statistic.addWidget(self.max24)

			self.statistic.addStretch(40)
			self.sensBox.addLayout(self.statistic)

		except Exception as e:
			filename = Path(__file__).name
			error_handle(e, filename)

		# Forecast container
		self.forecast = QVBoxLayout(self.sensFrame)
		self.Fheader = QLabel("FORECAST")
		self.Fheader.setFont(QFont('Arial', 15))
		f = fc()
		self.Fforecast1 = QLabel(f[0])
		self.Fforecast2 = QLabel(f[1])
		# self.Fforecast3 = QLabel("Expected Winds: ")# + forecast_val[2] + " BFT")

		self.forecast.addWidget(self.Fheader)
		self.forecast.addWidget(self.Fforecast1)
		self.forecast.addWidget(self.Fforecast2)
		# self.forecast.addWidget(self.Fforecast3)

		self.forecast.addStretch(10)
		self.sensBox.addLayout(self.forecast)

		#Graph Buttons
		button_style_wind = "QPushButton {background-color: grey; color: black; font-weight:600}" \
					   "QPushButton:checked {background-color: yellow; color: black; font-weight:600}"
		button_style_atp = "QPushButton {background-color: grey; color: black; font-weight:600}" \
					   "QPushButton:checked {background-color: blue; color: black; font-weight:600}"

		self.gwb = QPushButton()
		self.gwb.setText("WIND")
		self.gwb.setStyleSheet(button_style_wind)
		self.gwb.setCheckable(True)
		self.gwb.setChecked(True)
		self.gwb.clicked.connect(self.gwbf)
		self.gwb.clicked.connect(self.update_graph)

		self.gab = QPushButton()
		self.gab.setText("Pressure")
		self.gab.setStyleSheet(button_style_atp)
		self.gab.setCheckable(True)
		self.gab.clicked.connect(self.gabf)
		self.gab.clicked.connect(self.update_graph)

		self.sensBox.addWidget(self.gwb)
		self.sensBox.addWidget(self.gab)

		self.mainContainer.addWidget(self.sensFrame)

		self.O1.addLayout(self.mainContainer)

		# FOOTER
		self.footerBox = QHBoxLayout()

		self.latitude = QLabel("Latitude: " + fetch_gps.lat)
		self.longitude = QLabel("Longitude: " + fetch_gps.long)
		self.altitude = QLabel("Altitude: " + fetch_gps.alt)

		self.footerBox.addWidget(self.latitude)
		self.footerBox.addWidget(self.longitude)
		self.footerBox.addWidget(self.altitude)

		self.errimg = QPixmap(path + '/img/' + error_light())
		self.errico = QLabel()
		self.errico.setPixmap(self.errimg)
		self.footerBox.addWidget(self.errico)
		if ps is True:
			mem = psutil.virtual_memory()
			used_mem = round(mem.used/mem.total * 100)
			self.res = QLabel("P:{}% - M:{}%".format(psutil.cpu_percent(), used_mem))
			self.footerBox.addWidget(self.res)


		self.O1.addLayout(self.footerBox)

		# FOOTER END
		self.gw = True
		self.ga = False

	def gwbf(self):
		if self.gwb.isChecked():
			self.gw = True
		else:
			self.gw = False

	def gabf(self):
		if self.gab.isChecked():
			self.ga = True
		else:
			self.ga = False

	def update_wind(self):
		fetch_wind()
		fetch_mean()
		try:
			self.windL.setText(fetch_wind.wind)
			self.meanL.setText(str(fetch_mean.meanwind))
			self.beaufortL.setText(fetch_mean.beaufortLS)
		except Exception as e:
			filename = Path(__file__).name
			error_handle(e, filename)

		QApplication.processEvents()

	def update_statistics(self):
		fetch_statistics()
		try:
			self.peak.setText("Peak:        " + fetch_statistics.peak_wind + " m/s")
			self.max1.setText("Max 1hr:   " + fetch_statistics.max1 + " m/s")
			self.max3.setText("Max 3hr:   " + fetch_statistics.max3 + " m/s")
			self.max6.setText("Max 6hr:   " + fetch_statistics.max6 + " m/s")
			self.max12.setText("Max 12hr: " + fetch_statistics.max12 + " m/s")
			self.max24.setText("Max 24hr: " + fetch_statistics.max24 + " m/s")
		except Exception as e:
			filename = Path(__file__).name
			error_handle(e, filename)

		QApplication.processEvents()

	def update_sens(self):
		try:
			path = str(Path(__file__).parent.absolute())
			fetch_sens()
			fetch_gps()

			self.tempvalue.setText(fetch_sens.temp + " °C")
			self.tempimgarrow = QPixmap(path + '/img/' + sens_arrow(0))
			self.temparrow.setPixmap(self.tempimgarrow)
			self.humvalue.setText(fetch_sens.hum + "%")
			self.humimgarrow = QPixmap(path + '/img/' + sens_arrow(1))
			self.humarrow.setPixmap(self.humimgarrow)
			self.atpvalue.setText(fetch_sens.atp + " hPa")
			self.atpimgarrow = QPixmap(path + '/img/' + sens_arrow(2))
			self.atparrow.setPixmap(self.atpimgarrow)
			f = fc()
			self.Fforecast1.setText(f[0])
			self.Fforecast2.setText(f[1])
			# self.Fforecast3.setText("Expected Winds: " + forecast_val[2] + " BFT")

			self.latitude.setText("Latitude: " + fetch_gps.lat)
			self.longitude.setText("Longitude: " + fetch_gps.long)
			self.altitude.setText("Altitude: " + fetch_gps.alt)

			self.errimg = QPixmap(path + '/img/' + error_light())
			self.errico.setPixmap(self.errimg)
			if ps is True:
				mem = psutil.virtual_memory()
				used_mem = round(mem.used/mem.total * 100)
				self.res.setText("P:{}% - M:{}%".format(psutil.cpu_percent(), used_mem))


		except Exception as e:
			filename = Path(__file__).name
			error_handle(e, filename)

		QApplication.processEvents()

	def update_graph(self):
			try:
				fg()
				graph_update(self, fg.gw_x, fg.gw_y, fg.ga_x, fg.ga_y)

			except Exception as e:
				filename = Path(__file__).name
				# error_handle(e, filename)
				# print(e, filename)
			QApplication.processEvents()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.show()

	thread_update_graph = threading.Thread(target=ex.update_graph, args=())
	thread_update_graph.daemon = True
	thread_update_graph.start()

	thread_update_sens = threading.Thread(target=ex.update_sens, args=())
	thread_update_sens.daemon = True
	thread_update_sens.start()

	thread_update_wind = threading.Thread(target=ex.update_wind, args=())
	thread_update_wind.daemon = True
	thread_update_wind.start()


	wind_timer = QTimer()
	wind_timer.timeout.connect(ex.update_wind)
	wind_timer.start(1000)

	sens_timer = QTimer()
	sens_timer.timeout.connect(ex.update_sens)
	sens_timer.start(5000)

	graph_timer = QTimer()
	graph_timer.timeout.connect(ex.update_graph)
	graph_timer.start(60000)

	statistics_timer = QTimer()
	statistics_timer.timeout.connect(ex.update_statistics)
	statistics_timer.start(60000)

	sys.exit(app.exec_())

import sys
import time
import curses
from curses import wrapper
import mysql.connector
import itertools


def spinning_cursor():
	while True:
		for cursor in '|/-\\':
			yield cursor


def get_db_fresh_data():
	cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
	cursor = cnx.cursor()

	get_wind = "SELECT * FROM wind WHERE id=(SELECT MAX(id) FROM wind)"
	cursor.execute(get_wind)
	global wind
	wind = cursor.fetchone()

	get_gps = "SELECT * FROM gps WHERE id=(SELECT MAX(id) FROM gps)"
	cursor.execute(get_gps)
	global gps
	gps = cursor.fetchone()

	get_sens = "SELECT * FROM sens WHERE id=(SELECT MAX(id) FROM sens)"
	cursor.execute(get_sens)
	global sens
	sens = cursor.fetchone()

	get_db_size = """SELECT table_schema 'wfs', 
        ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) 'DB Size in MB' 
        FROM information_schema.tables 
        WHERE table_schema='wfs'
        GROUP BY table_schema;"""

	cursor.execute(get_db_size)
	global db_size
	db_size = cursor.fetchone()

	global last_record
	last_record = max(wind[2], gps[4], sens[4])


def gui_constants(stdscr):
	stdscr.erase()

	stdscr.addstr(0, 1, """This is a wind forecast station prototype under development""")

	stdscr.addstr(2, 5, 'Wind: ')

	stdscr.addstr(5, 5, 'GPS')
	stdscr.addstr(6, 5, 'Latitude: ')
	stdscr.addstr(6, 20, 'Longitude: ')
	stdscr.addstr(6, 35, 'Altitude: ')

	stdscr.addstr(9, 5, 'Sensors: ')
	stdscr.addstr(10, 5, 'Temperature: ')
	stdscr.addstr(10, 20, 'Humidity: ')
	stdscr.addstr(10, 35, 'Atmospheric Pressure: ')

	stdscr.addstr(2, 30, 'Last record: ')
	stdscr.addstr(2, 60, 'db Size: ')

	stdscr.refresh()


# stdscr.getkey()


def main(stdscr):
	# stdscr.erase()

	get_db_fresh_data()

	stdscr.addstr(2, 11, str(wind[1]))

	stdscr.addstr(7, 5, str(gps[1]))
	stdscr.addstr(7, 20, str(gps[2]))
	stdscr.addstr(7, 35, str(gps[3]))

	stdscr.addstr(11, 5, str(sens[1]))
	stdscr.addstr(11, 20, str(sens[2]))
	stdscr.addstr(11, 35, str(sens[3]))

	stdscr.addstr(3, 30, str(last_record))

	stdscr.addstr(3, 60, str(db_size[1]) + 'MB')

	stdscr.addstr(3, 60, str(db_size[1]) + 'MB')

	stdscr.refresh()


# stdscr.getkey()


while True:
	wrapper(gui_constants)

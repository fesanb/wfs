#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import curses
from curses import wrapper
import mysql.connector

a = 0


def main(stdscr):
    stdscr.clear()

    cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
    cursor = cnx.cursor()

    get_wind = "SELECT * FROM wind WHERE id=(SELECT MAX(id) FROM wind)"
    cursor.execute(get_wind)
    wind = cursor.fetchone()

    stdscr.addstr(str(wind[0]) + str(wind[1]) + str(wind[2]))

    stdscr.refresh()
    stdscr.getkey()

while True:
    wrapper(main)

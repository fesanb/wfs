#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import curses
from curses import wrapper
import mysql.connector


def main(stdscr):
    stdscr.clear()

    a = 0
    r = 0

    cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
    cursor = cnx.cursor()

    get_wind = "SELECT * FROM wind WHERE id=(SELECT MAX(id) FROM wind)"
    cursor.execute(get_wind)
    wind = cursor.fetchone()

    #stdscr.addstr(str(wind[0]) + str(wind[1]) + str(wind[2]))
    while a < 10:
        a += 1
        stdscr.addstr(2, 10, str(a))
        if r == 1:
            stdscr.addstr(2, 8, "/")
            r = 0
        else:
            stdscr.addstr(2, 8, "\\")
            r = 1

        time.sleep(0.5)
        stdscr.refresh()

    stdscr.refresh()
    stdscr.getkey()

while True:
    wrapper(main)

#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Serial Formatting
# Wind: <w,wind>
# GPS: <GPS,gpslat,gpslong,gpsalt,gpssat>
# Sensor: <SENS,temp,hum,atp>

import sys
import time
import serial
import serial.tools.list_ports as port_list
import mysql.connector

print("")
print("")
print("")
print("WWWWWWWW                           WWWWWWWWFFFFFFFFFFFFFFFFFFFFFF   SSSSSSSSSSSSSSS")
print("W::::::W                           W::::::WF::::::::::::::::::::F SS:::::::::::::::S")
print("W::::::W                           W::::::WF::::::::::::::::::::FS:::::SSSSSS::::::S")
print("W::::::W                           W::::::WFF::::::FFFFFFFFF::::FS:::::S     SSSSSSS")
print(" W:::::W           WWWWW           W:::::W   F:::::F       FFFFFFS:::::S")
print("  W:::::W         W:::::W         W:::::W    F:::::F             S:::::S")
print("   W:::::W       W:::::::W       W:::::W     F::::::FFFFFFFFFF    S::::SSSS")
print("    W:::::W     W:::::::::W     W:::::W      F:::::::::::::::F     SS::::::SSSSS")
print("     W:::::W   W:::::W:::::W   W:::::W       F:::::::::::::::F       SSS::::::::SS")
print("      W:::::W W:::::W W:::::W W:::::W        F::::::FFFFFFFFFF          SSSSSS::::S")
print("       W:::::W:::::W   W:::::W:::::W         F:::::F                         S:::::S")
print("        W:::::::::W     W:::::::::W          F:::::F                         S:::::S")
print("         W:::::::W       W:::::::W         FF:::::::FF           SSSSSSS     S:::::S")
print("          W:::::W         W:::::W          F::::::::FF           S::::::SSSSSS:::::S")
print("           W:::W           W:::W           F::::::::FF           S:::::::::::::::SS")
print("            WWW             WWW            FFFFFFFFFFF            SSSSSSSSSSSSSSS ")
print("")
print("")
print("")
print("")
print("                          Weather Forecast Station - v0.3")
print("                            - Written by Stefan Bahrawy")
print("                            - Terminal console and debugging below")
print(" ")
print(" ")
print(" ")
time.sleep(0)

cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
cursor = cnx.cursor()

# HANDSHAKE
i = 0
handshake = 0
ports = list(port_list.comports())
serial_port = ""
beauti_sleep = 1


while handshake == 0:
    for y in ports:
        x = [ports[i]]
        probe = x[0]
        i += 1
        print("    Probing: " + "\x1b[1;33m" + probe[0] + "\x1b[0m")
        ser = serial.Serial(probe[0], 19200, timeout=4)
        cc = str(ser.readline())
        probe_answer = cc[2:][:-5]
        time.sleep(beauti_sleep)

        if probe_answer == "S":
            print("")
            print("\x1b[1;32m" + "    ok" + "\x1b[0m" + " - Handshake 'S' received. Trying to send signal back...")
            time.sleep(beauti_sleep)
            serial_port = probe[0]
            print("\x1b[1;32m" + "    ok" + "\x1b[0m" + " - Serial port set to: " + "\x1b[1;33m" + serial_port + "\x1b[0m")
            time.sleep(beauti_sleep)
            ss = cc.encode()
            ser.write(ss)

            print("\x1b[1;32m" + "    ok" + "\x1b[0m" + " - Handshake signal sent with success.")
            time.sleep(beauti_sleep)
            handshake = 1
            print("")
            print("\x1b[1;32m" + "      <-- Handshake successful --> " + "\x1b[0m")
            print("")
            print(".. Starting script")
            print("")
            print("")
            time.sleep(beauti_sleep)
            ser.close()

            break
        print("    Silence: " + "\x1b[1;31m" + probe[0] + "\x1b[0m")
        print("")
# HANDSHAKE

try:
    ser = serial.Serial(serial_port, 19200)
except:
    print("Error connecting to the serial port. Either busy or no connection")
    print("Code needs changing, you are helpless.")
    sys.exit(1)

lastdatawind = ""
lastdatahum = ""
lastdatatemp = ""
lastdataatp = ""

timepassed = time.perf_counter()
countertime = 0
interval = 0.3



while True:
    try:
        cc = ser.readline()
        pcs = cc.decode().split(",")

        if timepassed - countertime > interval:
            if pcs[0] == "w":
                if pcs[1] != lastdatawind:
                    lastdatawind = pcs[1]
                    add_wind = (u'''INSERT INTO wind(wind) VALUES (%s)''' % (pcs[1]))
                    cursor.execute(add_wind)
                    emp_no = cursor.lastrowid
                    cnx.commit()

                    countertime = time.perf_counter()
        timepassed = time.perf_counter()

        if pcs[0] == "GPS":
            if pcs[1] != "0.00":
                print("Lat: ", pcs[1], " Long: ", pcs[2], " Alt: ", pcs[3], " SAT: ", pcs[4])

                add_gps = (u'''INSERT INTO gps(lat, lon, alt) VALUES (%s, %s, %s)''' % (pcs[1], pcs[2], pcs[3]))
                cursor.execute(add_gps)
                emp_no = cursor.lastrowid
                cnx.commit()

        if pcs[0] == "SENS":
            print("Temp: ", pcs[1], " Hum: ", pcs[2], " ATP: ", pcs[3], end="\r \r", flush=True)
            if pcs[1] != lastdatatemp and pcs[2] != lastdatahum and pcs[3] != lastdataatp:
                lastdatatemp = pcs[1]
                lastdatahum = pcs[2]
                lastdataatp = pcs[3]
                add_sens = (u'''INSERT INTO sens(temp, hum, atp) VALUES (%s, %s, %s)''' % (pcs[1], pcs[2], pcs[3]))
                cursor.execute(add_sens)
                emp_no = cursor.lastrowid
                cnx.commit()

    except:
        print("Error in serial read")

# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import bme680
import time
import mysql.connector
import sys
from wfs_error_handling import error_handle

sensor = bme680.BME680()

# sensor.set_humidity_oversample(bme680.OS_2X)
# sensor.set_pressure_oversample(bme680.OS_4X)
# sensor.set_temperature_oversample(bme680.OS_8X)
# sensor.set_filter(bme680.FILTER_SIZE_3)
#
# sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
# sensor.set_gas_heater_temperature(320)
# sensor.set_gas_heater_duration(150)
# sensor.select_gas_heater_profile(0)


def db_insert(temp, hum, atp, isset):
    cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
    cursor = cnx.cursor()
    try:
        cursor.execute(u'''INSERT INTO sens(temp, hum, atp, isset) VALUES ({0}, {1}, {2}, {3})'''.format(temp, hum, atp, isset))
        cnx.commit()
    except Exception as e:
        error_handle(e)


last_sens = []

while True:
    new_sens = [round(sensor.data.temperature, 1), round(sensor.data.humidity, 0), sensor.data.pressure]

    if last_sens == new_sens:
        issame = 1
    else:
        issame = 0

    new_sens.append(issame)

    if sensor.get_sensor_data() is None:
        pass
    else:
        db_insert(new_sens[0], new_sens[1], new_sens[2], new_sens[3])
        last_sens = new_sens

        time.sleep(120)

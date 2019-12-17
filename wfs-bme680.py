# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import bme680
import time
import mysql.connector
import sys

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


def db_insert(temp, hum, atp):
    cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
    cursor = cnx.cursor()
    try:
        cursor.execute(u'''INSERT INTO sens(temp, hum, atp) VALUES ({0}, {1}, {2})'''.format(temp, hum, atp))
        cnx.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_tb.tb_lineno)
        print(repr(e))
    # print("SQL insert done")


while True:
    if sensor.get_sensor_data() is None:
        pass
    else:
        temp = sensor.data.temperature
        hum = sensor.data.humidity
        atp = sensor.data.pressure
        db_insert(temp, hum, atp)
        time.sleep(600)

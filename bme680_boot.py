# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import bme680

sensor = bme680.BME680()

sensor.set_humidity_oversample(bme680.OS_16X)
sensor.set_pressure_oversample(bme680.OS_16X)
sensor.set_temperature_oversample(bme680.OS_16X)
sensor.set_filter(bme680.FILTER_SIZE_15)

# sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
# sensor.set_gas_heater_temperature(320)
# sensor.set_gas_heater_duration(150)
# sensor.select_gas_heater_profile(0)

# Thanks to https://github.com/triplepoint/micropython_bme280_i2c

import machine
from BME280 import bme280_i2c
import relay_controller as heater
import time
from micropython import const

# In Celsius
_heater_off_temperature = const(18)
_heater_on_temperature = const(6)

# Create a Micropython I2C object with the appropriate device pins
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

# Create a sensor object to represent the BME280
# Note that this will throw error if the device can't be reached over I2C.
sensor = bme280_i2c.BME280_I2C(address=bme280_i2c.BME280_I2C_ADDR_PRIM, i2c=i2c)

# Configure the sensor for the application in question.
sensor.set_measurement_settings({
    'filter': bme280_i2c.BME280_FILTER_COEFF_16,
    'standby_time': bme280_i2c.BME280_STANDBY_TIME_500_US,
    'osr_h': bme280_i2c.BME280_OVERSAMPLING_1X,
    'osr_p': bme280_i2c.BME280_OVERSAMPLING_16X,
    'osr_t': bme280_i2c.BME280_OVERSAMPLING_2X})

# Start the sensor automatically sensing
sensor.set_power_mode(bme280_i2c.BME280_NORMAL_MODE)

# Wait for the measurement settle time, print the measurement, and repeat
while 1:
    measurement = sensor.get_measurement()

    temperature = measurement["temperature"]
    print(f'Temperature: {temperature}')
    if temperature <= _heater_on_temperature:
        heater.turn_on()
    elif temperature >= _heater_off_temperature:
        heater.turn_off()

    humidity = measurement["humidity"]
    print(f'Humidity: {humidity}')

    pressure = measurement["pressure"]
    print(f'Pressure: {pressure}')
    print('========================')
    time.sleep_ms(1000)

# The above code repeatedly prints a line like:
# {'pressure': 101412.0, 'humidity': 39.5, 'temperature': 27.86}

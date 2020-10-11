import machine

from BME280 import bme280_i2c

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

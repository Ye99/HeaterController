import time

from micropython import const

import BME280_controller
import relay_controller as heater

# In Celsius
_heater_off_temperature = const(18)
_heater_on_temperature = const(6)

# In ms.
_measure_interval = const(1000)
assert _measure_interval > 100, "Must wait for measurement settle time before taking the next measurement."

while True:
    time.sleep_ms(_measure_interval)
    measurement = BME280_controller.sensor.get_measurement()

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

# The above code repeatedly prints a line like:
# {'pressure': 101412.0, 'humidity': 39.5, 'temperature': 27.86}

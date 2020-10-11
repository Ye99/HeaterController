import time

import ujson
from micropython import const

import BME280_controller
import mqtt_client
import relay_controller as heater
from MicroPythonLibriaries.connectWifi import do_connect

# In Celsius
_heater_off_temperature = const(18)
_heater_on_temperature = const(6)

# In ms.
_measure_interval = const(1000)
assert _measure_interval > 100, "Must wait for measurement settle time before taking the next measurement."

with open('credentials.json') as f:
    credentials = ujson.load(f)

wifi = credentials['Wifi']
ssid = wifi['ssid']
wifi_pwd = wifi['pwd']
do_connect(ssid, wifi_pwd)

mqtt = credentials['MQTT']
mqtt_user = mqtt['user']
mqtt_pwd = mqtt['pwd']
mqtt_client_id = mqtt['client_id']
mqtt_server = mqtt['server']

while True:
    time.sleep_ms(_measure_interval)
    measurement = BME280_controller.sensor.get_measurement()
    # Example readings
    # {'pressure': 101412.0, 'humidity': 39.5, 'temperature': 27.86}

    temperature = measurement["temperature"]
    temperature_message = f'Temperature: {temperature}'
    mqtt_client.publish_message(temperature_message, mqtt_client_id, mqtt_server, mqtt_user, mqtt_pwd)

    if temperature <= _heater_on_temperature:
        heater.turn_on()
    elif temperature >= _heater_off_temperature:
        heater.turn_off()

    humidity = measurement["humidity"]
    humidity_message = f'Humidity: {humidity}'
    mqtt_client.publish_message(humidity_message, mqtt_client_id, mqtt_server, mqtt_user, mqtt_pwd)

    pressure = measurement["pressure"]
    pressure_message = f'Pressure: {pressure}'
    mqtt_client.publish_message(pressure_message, mqtt_client_id, mqtt_server, mqtt_user, mqtt_pwd)
    print('========================')

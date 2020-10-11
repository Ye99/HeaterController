import time

import ujson
from micropython import const

import BME280_controller
import mqtt_client
import relay_controller as heater
from MicroPythonLibriaries.connectWifi import do_connect

# In Celsius
_heater_off_temperature = const(23)
_heater_on_temperature = 22.9

# In ms.
_measure_interval = const(5000)
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
mqtt_topic = mqtt['topic']

while True:
    time.sleep_ms(_measure_interval)
    measurement = BME280_controller.sensor.get_measurement()
    # Example readings
    # {'pressure': 101412.0, 'humidity': 39.5, 'temperature': 27.86}

    temperature = measurement["temperature"]
    temperature_message = 'Temperature: {}'.format(temperature)
    print(temperature_message)
    mqtt_client.publish_message(mqtt_topic, temperature_message, mqtt_client_id, mqtt_server, mqtt_user, mqtt_pwd)

    if temperature <= _heater_on_temperature:
        heater.turn_on()
        message = 'Heater turned on'
        print(message)
        mqtt_client.publish_message(mqtt_topic, message, mqtt_client_id, mqtt_server, mqtt_user, mqtt_pwd)
    elif temperature >= _heater_off_temperature:
        heater.turn_off()
        message = 'Heater turned off'
        print(message)
        mqtt_client.publish_message(mqtt_topic, message, mqtt_client_id, mqtt_server, mqtt_user, mqtt_pwd)

    humidity = measurement["humidity"]
    humidity_message = 'Humidity: {}'.format(humidity)
    print(humidity_message)
    mqtt_client.publish_message(mqtt_topic, humidity_message, mqtt_client_id, mqtt_server, mqtt_user, mqtt_pwd)

    pressure = measurement["pressure"]
    pressure_message = 'Pressure: {}'.format(pressure)
    print(pressure_message)
    mqtt_client.publish_message(mqtt_topic, pressure_message, mqtt_client_id, mqtt_server, mqtt_user, mqtt_pwd)
    print('========================')

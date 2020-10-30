import gc
import time

import machine
import ujson
from MicroPythonLibriaries.connectWifi import do_connect
from micropython import const

import BME280_controller
import error_counter
import mqtt_client

error_counter = error_counter.ErrorCounter()

# In ms.
_measure_interval = const(10000)
assert _measure_interval > 100, "Must wait for measurement settle time before taking the next measurement."

# each loop can generate 5 mqtt errors * number of loop in 4 minutes. Larger than rebooting router time, 2.5 minutes.
# 4 * 60 / (_measure_interval / 1000) * 5 = 120
_mqtt_consecutive_failure_threshold = const(120)
print("_mqtt_consecutive_failure_threshold is {}".format(_mqtt_consecutive_failure_threshold))

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

_control_strategy = credentials['Control_Strategy']

if "temperature" == _control_strategy:
    import temperature_strategy

    control_strategy = temperature_strategy.TemperatureControlStrategy()
elif "humidity" == _control_strategy:
    import humidity_strategy

    control_strategy = humidity_strategy.HumidityControlStrategy()

mqtt_message_sequence = 0
mqtt_failure_count = 0

while True:
    try:
        # periodically gc is good https://docs.micropython.org/en/latest/reference/speed_python.html
        gc.collect()

        print('\n======Measurements=======')
        measurement = BME280_controller.sensor.get_measurement()
        # Example readings
        # {'pressure': 101412.0, 'humidity': 39.5, 'temperature': 27.86}

        temperature = measurement["temperature"]
        temperature_message = '{}_temperature: {}'.format(mqtt_message_sequence, temperature)
        mqtt_failure_count = error_counter.invoke(mqtt_client.publish_message, mqtt_topic, temperature_message,
                                                  mqtt_client_id, mqtt_server, mqtt_user,
                                                  mqtt_pwd)

        humidity = measurement["humidity"]
        humidity_message = '{}_humidity: {}'.format(mqtt_message_sequence, humidity)
        mqtt_failure_count = error_counter.invoke(mqtt_client.publish_message, mqtt_topic, humidity_message,
                                                  mqtt_client_id,
                                                  mqtt_server, mqtt_user, mqtt_pwd)

        pressure = measurement["pressure"]
        pressure_message = '{}_pressure: {}'.format(mqtt_message_sequence, pressure)
        mqtt_failure_count = error_counter.invoke(mqtt_client.publish_message, mqtt_topic, pressure_message,
                                                  mqtt_client_id,
                                                  mqtt_server, mqtt_user, mqtt_pwd)
        print('=====Control section========')
        print('Control strategy is {}'.format(_control_strategy))

        if "temperature" == _control_strategy:
            input_value = temperature
        elif "humidity" == _control_strategy:
            input_value = humidity

        relay_status_tuple = control_strategy.apply_strategy(input_value)

        if relay_status_tuple.off_to_on:
            message = '{}_relay turned on'.format(mqtt_message_sequence)
            mqtt_failure_count = error_counter.invoke(mqtt_client.publish_message, mqtt_topic, message, mqtt_client_id,
                                                      mqtt_server, mqtt_user, mqtt_pwd)
        elif relay_status_tuple.on_to_off:
            message = '{}_relay turned off'.format(mqtt_message_sequence)
            mqtt_failure_count = error_counter.invoke(mqtt_client.publish_message, mqtt_topic, message, mqtt_client_id,
                                                      mqtt_server, mqtt_user, mqtt_pwd)

        message = '{}_relay status {}'.format(mqtt_message_sequence, relay_status_tuple.current_status)
        mqtt_failure_count = error_counter.invoke(mqtt_client.publish_message, mqtt_topic, message, mqtt_client_id,
                                                  mqtt_server, mqtt_user, mqtt_pwd)

        mqtt_message_sequence += 1

        time.sleep_ms(_measure_interval)  # wait before reconnect wifi, otherwise pending message will be dropped.

        print("Current mqtt failure count is {}".format(mqtt_failure_count))
        if mqtt_failure_count > _mqtt_consecutive_failure_threshold:
            machine.reset()

    except Exception as e:  # [Errno 110] ETIMEDOUT because of reading sensor, or network error.
        print('\tException {}'.format(e))
        time.sleep_ms(_measure_interval)  # This wait is necessary, otherwise endless loop.
        machine.reset()

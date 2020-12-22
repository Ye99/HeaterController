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

# each loop can generate 1 mqtt errors * number of loop in 4 minutes.
# Make sure longer than rebooting router time, 2.5 minutes.
# 4 * 60 / (_measure_interval / 1000) * 1 = 24. Put in below const.
_mqtt_consecutive_failure_threshold = const(24)
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
_location = credentials['Location']

control_strategy = None
relay_status_tuple = None

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

        measurement = BME280_controller.sensor.get_measurement()
        # Example readings
        # {'pressure': 101412.0, 'humidity': 39.5, 'temperature': 27.86}
        temperature = measurement["temperature"]
        humidity = measurement["humidity"]
        pressure = measurement["pressure"]

        if control_strategy is not None:
            print('Control strategy is {}'.format(_control_strategy))

            if "temperature" == _control_strategy:
                input_value = temperature
            elif "humidity" == _control_strategy:
                input_value = humidity

            relay_status_tuple = control_strategy.apply_strategy(input_value)

        # MQTT message using InfluxDB line protocol
        # weather,location=us-midwest,season=summer temperature=82
        # https://docs.influxdata.com/influxdb/v1.8/write_protocols/line_protocol_tutorial/
        message = 'status,location={},control_strategy={},sequence_id={} ' \
                  'temperature={},humidity={},pressure={}'.format(
            _location, _control_strategy, mqtt_message_sequence,
            temperature, humidity, pressure)

        if relay_status_tuple is not None:
            message += ',relay={},relay_off->on={},relay_on->off={}'.format(
                relay_status_tuple.current_status,
                relay_status_tuple.off_to_on,
                relay_status_tuple.on_to_off)

        mqtt_failure_count = error_counter.invoke(mqtt_client.publish_message, mqtt_topic, message, mqtt_client_id,
                                                  mqtt_server, mqtt_user, mqtt_pwd)

        mqtt_message_sequence += 1

        time.sleep_ms(_measure_interval)  # wait before reconnect wifi, otherwise pending message will be dropped.

        print("Current mqtt failure count is {}".format(mqtt_failure_count))
        if mqtt_failure_count > _mqtt_consecutive_failure_threshold:
            machine.reset()  # This recover from broken mqtt situation.

    except Exception as e:  # [Errno 110] ETIMEDOUT because of reading sensor, or network error.
        print('\tException {}'.format(e))
        time.sleep_ms(_measure_interval)  # This wait is necessary, otherwise endless loop.
        machine.reset()

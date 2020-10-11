from MicroPythonLibriaries.umqtt.simple import MQTTClient


def publish_message(message, client_id, server, user, password) -> None:
    """
    Publish message using MQTT.
    Only call this method when wifi is connected.
    :param message: The message to be published, in binary format.
    :param client_id: String client id of this client.
    :param server: Server ip address as string.
    :param user: User name to authenticate with MQTT server, e.g. b"mosquitto"
    :param password: Password e.g. b"mosquitto". If username/pwd wrong, this method will throw Exception
    :return:
    """
    print('Publish message {0}'.format(message))
    # don't catch "fail fast fail hard".
    c = MQTTClient(client_id,
                   server,
                   user,
                   password,
                   ssl=False)
    if 0 == c.connect():  # 0 is success.
        c.publish(b"network_watchdog_status_topic", message)
        c.disconnect()
    else:
        print('Connect to MQTT server failed. ')

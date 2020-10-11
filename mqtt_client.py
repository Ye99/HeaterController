from MicroPythonLibriaries.umqtt.simple import MQTTClient


def publish_message(topic, message, client_id, server, user, password) -> None:
    """
    Publish message using MQTT.
    Only call this method when wifi is connected.
    :param topic: The topic the message belongs to, in binary format. e.g. b"my_topic"
    :param message: The message to be published, in binary format. e.g. b"my_message"
    :param client_id: String client id of this client.
    :param server: Server ip address as string.
    :param user: User name to authenticate with MQTT server, e.g. b"mosquitto"
    :param password: Password e.g. b"mosquitto". If username/pwd wrong, this method will throw Exception
    :return:
    """
    print('Publish message {0}'.format(message))
    # don't catch "fail fast fail hard".
    c = MQTTClient(client_id=client_id,
                   # use parameter assignments, because skipped port and thus sequence won't match.
                   server=server,
                   user=user,
                   password=password,
                   ssl=False)
    if 0 == c.connect():  # 0 is success.
        c.publish(topic, message)
        c.disconnect()
    else:
        print('Connect to MQTT server failed. ')

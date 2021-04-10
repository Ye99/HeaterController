from MicroPythonLibriaries.umqtt.simple import MQTTClient


def publish_message(topic, message, client_id, server, port, user, password) -> bool:
    """
    Publish message using MQTT.
    Only call this method when wifi is connected.
    This function doesn't throw. Remember to check return value.
    :param topic: The topic the message belongs to, in binary format. e.g. b"my_topic"
    :param message: The message to be published, in binary format. e.g. b"my_message"
    :param client_id: String client id of this client.
    :param server: Server ip address as string.
    :param port: the port of MQTT service.
    :param user: User name to authenticate with MQTT server, e.g. b"mosquitto"
    :param password: Password e.g. b"mosquitto". If username/pwd wrong, this method will throw Exception
    :return True if publishing succeeded; False if failed.
    """
    try:
        print('Publish message: {0}'.format(message))
        # don't catch "fail fast fail hard".
        c = MQTTClient(client_id=client_id,
                       # use parameter assignments, because skipped port and thus sequence won't match.
                       server=server,
                       port=port,
                       user=user,
                       password=password,
                       ssl=False)
        if 0 == c.connect():  # 0 is success.
            c.publish(topic, message)
            c.disconnect()
            return True
        else:
            print('\tConnect to MQTT server failed. ')
            return False
    except Exception as e:  # (OSError, IndexError, MQTTException) all derive from Exception.
        # If network is down, proceed to next step and maintain control.
        # IndexError happens when socket read doesn't return enough data and throw at the assert line.
        #   resp = self.sock.read(4)
        #   assert resp[0] == 0x20 and resp[1] == 0x02
        # Exception handling see https://docs.python.org/3/tutorial/errors.html#handling-exceptions
        print('\tPublish message failed, error {}'.format(e))
        return False

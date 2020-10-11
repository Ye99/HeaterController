from machine import Pin

# Relay at D6 (GPIO12).
# D6 is high at boot.
# Connect the relay to high trigger.
# Do not set relay to low trigger, because some ESP8266 high output isn't high enough to turn off the relay.
# Set relay to high trigger mode is more reliable.
relay = Pin(12, Pin.OUT)


def turn_on() -> None:
    relay.value(1)


def turn_off() -> None:
    relay.value(0)

# Default off at device initialization.
turn_off()

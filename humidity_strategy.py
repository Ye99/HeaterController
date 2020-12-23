from micropython import const

import control_strategy
import relay_controller as relay

# In Celsius
_relay_off_humidity_threshold = const(40)
_relay_on_humidity_threshold = const(52)


class HumidityControlStrategy(control_strategy.ControlStrategyInterface):
    def apply_strategy(self, value: float) -> control_strategy.RelayStatusTuple:
        """
        Turn on/off relay based on input value.
        :param value:
        :return:
        """
        print("HumidityControlStrategy.apply_strategy input value ", value)
        off_to_on = False
        on_to_off = False
        if value >= _relay_on_humidity_threshold:
            off_to_on = True
            relay.turn_on()
        elif value <= _relay_off_humidity_threshold:
            on_to_off = True
            relay.turn_off()

        # Micropython doesn't support _replace
        # https://docs.python.org/3.3/library/collections.html?highlight=namedtuple#collections.namedtuple
        relay_status = control_strategy.RelayStatusTuple(off_to_on, on_to_off, relay.get_status())
        return relay_status

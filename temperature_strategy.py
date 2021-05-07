from micropython import const

import control_strategy
import relay_controller as relay

# In Celsius
_heater_off_temperature = const(11)
_heater_on_temperature = const(8)


class TemperatureControlStrategy(control_strategy.ControlStrategyInterface):
    def apply_strategy(self, value: float) -> control_strategy.RelayStatusTuple:
        """
        Turn on/off relay based on input value.
        :param value:
        :return:
        """
        print("TemperatureControlStrategy.apply_strategy input value ", value)
        off_to_on = False
        on_to_off = False
        if value <= _heater_on_temperature:
            off_to_on = True
            relay.turn_on()
        elif value >= _heater_off_temperature:
            on_to_off = True
            relay.turn_off()

        # Micropython doesn't support _replace
        # https://docs.python.org/3.3/library/collections.html?highlight=namedtuple#collections.namedtuple
        relay_status = control_strategy.RelayStatusTuple(off_to_on, on_to_off, relay.get_status())
        return relay_status

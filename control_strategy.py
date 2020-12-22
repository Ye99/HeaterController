# Micropython doesn't support abc as described here https://realpython.com/python-interface/
# My primitive ABC.
from ucollections import namedtuple
RelayStatusTuple = namedtuple("RelayStatus", ("off_to_on", "on_to_off", "current_status"))

class ControlStrategyInterface:
    def apply_strategy(self, value:float) -> RelayStatusTuple:
        """
        Turn on/off relay based on input value.
        :param value:
        :return:
        """
        pass


import math


class CalculationUtils:
    def __init__(self, take_profit, stop_loss):
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    @staticmethod
    def round_decimals_up(value: float, decimals: int = 2):
        if not isinstance(decimals, int):
            raise TypeError("decimal places must be an integer")
        elif decimals < 0:
            raise ValueError("decimal places has to be 0 or more")
        elif decimals == 0:
            return math.ceil(value)

        factor = 10 ** decimals
        print('Rounded amount to operate: ' + str(math.ceil(value * factor) / factor))
        return math.ceil(value * factor) / factor



from enum import Enum


class OrderType(Enum):
    SELL = 1
    BUY = 2


class OrderTypeUtils:
    @staticmethod
    def opposite(type: OrderType):
        if type == OrderType.SELL:
            return OrderType.BUY
        else:
            return OrderType.SELL

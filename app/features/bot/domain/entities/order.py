from enum import Enum

from app.features.bot.domain.entities.order_type import OrderType


class ProfitType(Enum):
    STOP_LOSS = 1
    TAKE_PROFIT = 2
    NEUTRAL = 3


class Order:
    def __init__(self, symbol, amount, price, type: OrderType, take_profit, stop_loss,
                 profit_type: ProfitType):
        self.symbol = symbol
        self.amount = float(amount)
        self.price = float(price)
        self.type = type
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.is_close_operation = take_profit is not None and stop_loss is not None
        self.profit_type = profit_type

from app.features.bot.domain.entities.order import Order
from app.features.bot.domain.entities.order_type import OrderType
from config import Config


class Band:
    def __init__(self, high: Order, low: Order):
        self.high = high
        self.low = low


class Breakpoints:
    def __init__(self, high: float, low: float):
        self.high = high
        self.low = low

class LossBreakpoints:
    def __init__(self, profit: float, loss: float):
        self.profit = profit
        self.loss = loss


class OrderCalculationUtils:
    def __init__(self):

        # import config settings
        cfg = Config()

        self.take_profit_percentage = cfg.take_profit
        self.stop_loss_percentage = cfg.stop_loss
        self.initial_band_percentage = cfg.initial_band_margin
        self.iteration_multiplier = cfg.amount_multiplier

    def calculate_take_profit(self, price, type: OrderType) -> float:
        if type == OrderType.BUY:
            multiplier = 1 + self.take_profit_percentage
        else:
            multiplier = 1 - self.take_profit_percentage
        return price * multiplier

    def calculate_stop_loss(self, price, type: OrderType) -> float:
        if type == OrderType.BUY:
            multiplier = 1 - self.stop_loss_percentage
        else:
            multiplier = 1 + self.stop_loss_percentage
        return price * multiplier

    def calculate_new_amount(self, amount):
        new_amount = amount * self.iteration_multiplier
        return new_amount

    def calculate_initial_breakpoints(self, price):
        # High
        high_price = price * (1 + self.initial_band_percentage)
        low_price = price * (1 - self.initial_band_percentage)
        return Breakpoints(high=high_price, low=low_price)

    def calculate_loss_breakpoints(self, price, next_order_type: OrderType) -> LossBreakpoints:
        if next_order_type == OrderType.BUY:
            profit = price * (1 + self.take_profit_percentage)
            loss = price * (1 - self.stop_loss_percentage)
        else:
            profit = price * (1 - self.take_profit_percentage)
            loss = price * (1 + self.stop_loss_percentage)
        return LossBreakpoints(profit=profit, loss=loss)

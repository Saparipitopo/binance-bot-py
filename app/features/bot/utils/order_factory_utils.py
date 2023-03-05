from app.features.bot.domain.entities.order import Order


class OrderFactoryUtils:
    def __init__(self, user_input_utils, order_calculation_utils):
        self.user_input_utils = user_input_utils
        self.order_calculation_utils = order_calculation_utils

    @staticmethod
    def create_order(symbol, amount, price, order_type, take_profit, stop_loss, profit_type):
        return Order(symbol=symbol, amount=amount, price=price, type=order_type, take_profit=take_profit,
                     stop_loss=stop_loss, profit_type=profit_type)

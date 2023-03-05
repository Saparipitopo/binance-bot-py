from app.features.bot.data.repositories.binance_remote_repository import BinanceRemoteRepository


class BinanceRequest:
    def __init__(self, repository: BinanceRemoteRepository):
        self.client_repository = repository.client

    @staticmethod
    def get_order_info(order):
        order = order[1]
        return order['orderId'], order['symbol']

    def request_order_data(self, order, data):

        order_id, order_symbol = self.get_order_info(order)

        order_json = self.client_repository.futures_get_order(symbol=order_symbol, orderId=order_id)
        return float(order_json[data])

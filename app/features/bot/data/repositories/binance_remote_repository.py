from binance.exceptions import BinanceAPIException

from app.features.bot.data.dto.account_info import AccountInfoMapper, AccountInfo
from app.features.bot.data.dto.ticker import SymbolPriceChangeTickerMapper, SymbolPriceChangeTicker, \
    SymbolTickerMapper
from app.features.bot.domain.entities.order import Order
from app.features.bot.domain.entities.order_type import OrderType, OrderTypeUtils
from app.features.bot.utils.decimal_calculations import CalculationUtils
from app.keys.keys import UserKeys
from binance import Client
from binance.enums import SIDE_SELL, FUTURE_ORDER_TYPE_MARKET, SIDE_BUY


class BinanceRemoteRepository:
    def __init__(self, keys: UserKeys, is_test: bool):
        self.client = Client(keys.api_key_public, keys.api_key_secret)
        self.decimal_precision = 0
        self.is_test = is_test
        self.leverage = None
        self.order = None

    def get_24hr_change_list(self):
        tickers = self.client.futures_ticker()
        ticker_list = []
        for json in tickers:
            ticker = SymbolPriceChangeTickerMapper.from_json(json)
            ticker_list.append(ticker)
        ticker_list.sort(key=self.__24hr_ticker_sort, reverse=True)
        return ticker_list

    @staticmethod
    def __24hr_ticker_sort(ticker: SymbolPriceChangeTicker):
        return abs(ticker.price_change_percent)

    def set_leverage(self, symbol, leverage):
        self.leverage = leverage
        try:
            data = self.client.futures_change_leverage(symbol=symbol, leverage=leverage)
            return data
        except Exception as e:
            print('Error while changing leverage: ', e)
            return None

    def get_symbol_info(self, symbol):
        try:
            data = self.client.get_symbol_info(symbol)
            return data
        except Exception as e:
            print('Error while getting info: ', e)
            return None

    def set_precision(self, precision):
        self.decimal_precision = precision

    def get_account_info(self, asset_symbol):
        accounts = self.client.futures_account_balance()
        for account_json in accounts:
            account = AccountInfoMapper.from_json(account_json)
            if account.asset == asset_symbol:
                return account
        return AccountInfo('no_alias', asset_symbol, 0, 0, 0)

    def get_price(self, symbol):
        try:
            symbol_json = self.client.futures_symbol_ticker(symbol=symbol)
            ticker = SymbolTickerMapper.from_json(symbol_json)
            print('\rPrice: ', ticker.price, end='')
            return ticker.price
        except Exception as e:
            print('Error while getting symbol price: ', e)
        return None

    def get_orders(self, symbol):
        result = self.client.futures_get_open_orders(symbol=symbol)
        return result

    def get_order_book(self, symbol) -> dict:
        orders = self.client.futures_order_book(symbol=symbol)
        return orders

    def get_precision(self, symbol):
        info = self.client.futures_exchange_info()
        for x in info['symbols']:
            if x['symbol'] == symbol:
                        if x['quantityPrecision'] is None:
                            x['quantityPrecision'] = 0
                            
                        self.set_precision(x['quantityPrecision'])
                        
                        return x['quantityPrecision']

    def can_market_operate(self, symbol, price, quantity, order_type: OrderType):
        orders = self.get_order_book(symbol)
        price_to_match = price * quantity
        print(orders)
        if order_type == OrderType.SELL:
            side_orders = list(orders['bids'])
        else:
            side_orders = orders['asks']

        qty = 0
        total_price = 0
        index = 0
        while qty <= quantity:
            order = side_orders[index]
            order_price = float(order[0])
            order_quantity = float(order[1])
            qty = qty + order_quantity
            total_price = total_price + (order_quantity * order_price)

        print('Total price: ', total_price, '. Price to match: ', price_to_match)
        return total_price >= price_to_match

    @staticmethod
    def __get_side_from_order_type(order_type: OrderType):
        if order_type == OrderType.SELL:
            side = SIDE_SELL
        else:
            side = SIDE_BUY
        return side

    def __round_decimals(self, value):
        return CalculationUtils.round_decimals_up(value, self.decimal_precision)

    def open_order(self, order: Order):
        try:
            side = self.__get_side_from_order_type(order.type)
            amount = self.__round_decimals(order.amount)
            if order.type == OrderType.SELL:
                type_str = 'SELL'
            else:
                type_str = 'BUY'
            print('\nPlacing order - type: ', type_str, '. Price: ', order.price, '. Amount: ', amount)
            print('Side: ', side)
            if not self.is_test:
                result = self.client.futures_create_order(symbol=order.symbol, side=side, type=FUTURE_ORDER_TYPE_MARKET,
                                                          quantity=amount)
                print(result)
                self.order = result

            order_result = order
            return order_result, self.order

        except BinanceAPIException as e:
            print('Error placing order: ', e)
            return None

    def close_order(self, order: Order):
        try:
            order_type = OrderTypeUtils.opposite(order.type)
            side = self.__get_side_from_order_type(order_type)
            amount = self.__round_decimals(order.amount)
            if not self.is_test:
                result = self.client.futures_create_order(symbol=order.symbol, side=side, reduceOnly=True,
                                                          type=FUTURE_ORDER_TYPE_MARKET, quantity=amount)
                print(result)
                self.order = result

            order_result = order
            return order_result, self.order

        except BinanceAPIException as e:
            print('Error closing order: ', e)
            return None

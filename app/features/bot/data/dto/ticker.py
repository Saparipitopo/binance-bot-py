class SymbolTicker:
    def __init__(self, price: float, symbol):
        self.price = float(price)
        self.symbol = symbol


class SymbolPriceChangeTicker:
    def __init__(self, price_change_percent: float, symbol, price: float):
        self.price_change_percent = price_change_percent
        self.symbol = symbol
        self.price = price


class SymbolTickerMapper:
    @staticmethod
    def from_json(json):
        price = float(json['price'])
        return SymbolTicker(price, json['symbol'])


class SymbolPriceChangeTickerMapper:
    @staticmethod
    def from_json(json):
        price = float(json['lastPrice'])
        price_change_percent = float(json['priceChangePercent'])
        symbol = json['symbol']
        return SymbolPriceChangeTicker(price_change_percent, symbol, price)

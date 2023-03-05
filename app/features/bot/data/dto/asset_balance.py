class AssetBalance:
    def __init__(self, symbol, free, locked):
        self.symbol = symbol
        self.free = free
        self.locked = locked


class AssetBalanceMapper:
    @staticmethod
    def from_json(json):
        return AssetBalance(json['asset'], json['free'], json['locked'])

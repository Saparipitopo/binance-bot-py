from app.features.bot.data.repositories.binance_remote_repository import BinanceRemoteRepository


class PriceWatcherUtils:
    def __init__(self, binance_repository: BinanceRemoteRepository):
        self.binance_repository = binance_repository

    async def watch_price_until_condition(self, symbol, less_than_this_value, greater_than_this_value):
        coin_price = await self.get_price(symbol)
        if coin_price is None:
            return
        is_greater = coin_price >= greater_than_this_value
        is_less = coin_price <= less_than_this_value
        while not is_greater and not is_less:
            coin_price = await self.get_price(symbol)
            if coin_price is None:
                return
            is_greater = coin_price >= greater_than_this_value
            is_less = coin_price <= less_than_this_value
        if is_greater:
            return greater_than_this_value
        else:
            return less_than_this_value

    async def get_price(self, symbol) -> int:
        market_price = self.binance_repository.get_price(symbol)
        while market_price is None:
            market_price = self.binance_repository.get_price(symbol)
        return market_price

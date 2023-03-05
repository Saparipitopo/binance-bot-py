import asyncio
from app.keys.keys import UserKeys
from app.features.bot.bot import Bot
from app.features.bot.data.repositories.binance_remote_repository import BinanceRemoteRepository

from app.features.bot.utils.counter_utils import CounterUtils
from app.features.bot.utils.order_calculation_utils import OrderCalculationUtils
from app.features.bot.utils.order_factory_utils import OrderFactoryUtils
from app.features.bot.utils.price_watcher_utils import PriceWatcherUtils
from app.features.bot.utils.user_input_utils import UserInputUtils

async def main():
        UserInputUtils().get_coin_setup()

        setup_values = UserInputUtils().get_setup_json()
        
        is_test = setup_values.get('is_test')
        symbol = setup_values.get('symbol')
        amount_in_usdt = setup_values.get('amount_in_usdt')
        leverage = setup_values.get('leverage')
        
        # Repository
        repo = BinanceRemoteRepository(keys=UserKeys(), is_test=is_test)
        repo.set_leverage(symbol, leverage)
        
        # Order calculations
        order_calculation_utils = OrderCalculationUtils()

        # Counter
        counter_utils = CounterUtils()

        # User inputs
        user_input_utils = UserInputUtils()

        # Order factory
        order_factory_utils = OrderFactoryUtils(user_input_utils, order_calculation_utils)

        # Price watcher
        price_watcher_utils = PriceWatcherUtils(binance_repository=repo)

        # Creating bot
        bot = Bot(repository= repo,
                  order_utils= order_calculation_utils,
                  counter_utils= counter_utils,
                  order_factory_utils= order_factory_utils,
                  price_watcher_utils= price_watcher_utils,
                  symbol= symbol)
        
        try:
            await bot.initialize(amount_in_usdt=amount_in_usdt, symbol=symbol)
        except Exception as e:
            print(e)
            
            
            
asyncio.run(main())
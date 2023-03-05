# BinanceRemoteRepository - interact with binance
from app.features.bot.data.repositories.binance_remote_repository import BinanceRemoteRepository
# OrderType - get OrderType object
from app.features.bot.domain.entities.order_type import OrderType

# BinanceRequest - request about open orders with binance
from app.features.bot.utils.binance_request_utils import BinanceRequest
# CounterUtils - takes care of the counters of the bot (eg. amount of SL)
from app.features.bot.utils.counter_utils import CounterUtils
# OrderCalculationUtils - calculation of breakpoints and new amount if SL was triggered
from app.features.bot.utils.order_calculation_utils import OrderCalculationUtils, Breakpoints
# OrderFactoryUtils - crates the Order object
from app.features.bot.utils.order_factory_utils import OrderFactoryUtils
# PriceWatcherUtils - gets the price of given symbol and waits till the price is X
from app.features.bot.utils.price_watcher_utils import PriceWatcherUtils
# PrintUtils - methods for printing data on terminal
from app.features.bot.utils.print_utils import PrintUtils
# UserInputUtils - used to get the initial config the user chose
from app.features.bot.utils.user_input_utils import UserInputUtils


class Bot:
    def __init__(self, repository: BinanceRemoteRepository,
                 order_utils: OrderCalculationUtils,
                 counter_utils: CounterUtils,
                 order_factory_utils: OrderFactoryUtils,
                 price_watcher_utils: PriceWatcherUtils,
                 symbol):

        self.repository = repository
        self.binance_request = BinanceRequest(repository=self.repository)
        self.order_utils = order_utils
        self.counter = counter_utils
        self.order_factory_utils = order_factory_utils
        self.price_watcher = price_watcher_utils
        self.print_utils = PrintUtils(counter=self.counter)
        self.coin_precision = repository.get_precision(symbol=symbol)

        setup_values = UserInputUtils().get_setup_json()

        self.initial_amount_in_usdt = setup_values.get('amount_in_usdt')
        self.is_test = setup_values.get('is_test')

    async def initialize(self, symbol, amount_in_usdt, action: OrderType = None):
        # Check if the bot must sleep for TP
        if self.counter.should_sleep_win():
            print('*********')
            print('TAKE PROFIT SLEEP')
            print('*********\n\n')
            return

        # Check if the bot must sleep for SL
        if self.counter.should_sleep_loss():
            print('*********')
            print('STOP LOSS SLEEP')
            print('*********\n\n')
            return

        # get coin price
        coin_price = await self.price_watcher.get_price(symbol)

        # calculating token amount from usdt
        amount_to_operate = self.calculate_amount_from_usdt(amount_in_usdt, coin_price)

        # printing initial data
        self.print_utils.print_initialize(amount_in_usdt, amount_to_operate, coin_price)

        # calculating the initial range breakpoints
        breakpoints = self.order_utils.calculate_initial_breakpoints(coin_price)

        if action == OrderType.BUY:
            match = breakpoints.high

        elif action == OrderType.SELL:
            match = breakpoints.low

        else:
            # printing on terminal the breakpoints
            self.print_utils.print_breakpoints(price=coin_price,
                                               breakpoints=Breakpoints)
            # comparing price with the two values of the breakpoints and returning the value that matched
            self.print_utils.print_waiting_for_high_low(breakpoints.high, breakpoints.low, coin_price)
            match = await self.price_watcher.watch_price_until_condition(symbol=symbol,
                                                                         less_than_this_value=breakpoints.low,
                                                                         greater_than_this_value=breakpoints.high)

        if match == breakpoints.high:
            if not action:
                # informing user
                print('\n*********')
                print('Long band match')
                print('*********')

            # creating the order
            order = self.order_factory_utils.create_order(symbol,
                                                          amount_to_operate,
                                                          breakpoints.high,
                                                          OrderType.BUY,
                                                          None,
                                                          None,
                                                          None)

            # opening the order
            open_order = self.repository.open_order(order=order)

            # if is_test is ture, then there's not an real order on binance to check the value, so it uses the token price when it was supposed to open the order
            if self.is_test:
                order_price = coin_price
            else:
                # getting from binance the avg price at wich the order was open
                order_price = self.binance_request.request_order_data(order=open_order,
                                                                      data='avgPrice')

            # calculating the TP & SL using the avg price
            tp = self.order_utils.calculate_take_profit(price=order_price,
                                                        type=OrderType.BUY)
            sl = self.order_utils.calculate_stop_loss(price=order_price,
                                                      type=OrderType.BUY)

            less_value = sl
            greater_value = tp

            sl_next_order_type = OrderType.SELL
            tp_next_order_type = OrderType.BUY

        elif match == breakpoints.low:
            if not action:
                # informing user
                print('\n*********')
                print('Short band match')
                print('*********')

            # creating the order
            order = self.order_factory_utils.create_order(symbol,
                                                          amount_to_operate,
                                                          breakpoints.low,
                                                          OrderType.SELL,
                                                          None,
                                                          None,
                                                          None)

            # opening the order
            open_order = self.repository.open_order(order=order)

            # if is_test is ture, then there's not an real order on binance to check the value, so it uses the token price when it was supposed to open the order
            if self.is_test:
                order_price = coin_price
            else:
                # getting from binance the avg price at wich the order was open
                order_price = self.binance_request.request_order_data(order=open_order,
                                                                      data='avgPrice')

            # calculating the TP & SL using the avg price
            tp = self.order_utils.calculate_take_profit(price=order_price,
                                                        type=OrderType.SELL)
            sl = self.order_utils.calculate_stop_loss(price=order_price,
                                                      type=OrderType.SELL)

            less_value = tp
            greater_value = sl

            sl_next_order_type = OrderType.BUY
            tp_next_order_type = OrderType.SELL


        else:
            print('*****************************************************')
            print('Something went wrong waiting for a initial band match')
            print('*****************************************************')
            return

        # print waiting
        self.print_utils.print_waiting_tp_sl(tp=tp,
                                             sl=sl,
                                             price=order_price)

        # comparing price with the TP & SL and returning the value that matched
        match = await self.price_watcher.watch_price_until_condition(symbol=symbol,
                                                                     less_than_this_value=less_value,
                                                                     greater_than_this_value=greater_value)

        if match == tp:
            # add counter to TP & print info
            self.print_utils.on_take_profit()
            # print all counters
            self.counter.print_counters()

            # closing open order
            self.repository.close_order(order=order)

            # starting the bot again with initial conditions
            await self.initialize(symbol=symbol,
                                  amount_in_usdt=self.initial_amount_in_usdt,
                                  action=tp_next_order_type)

        elif match == sl:
            # add counter to SL & print info
            self.print_utils.print_on_stop_loss()

            # print all counters
            self.counter.print_counters()

            # closing open order
            self.repository.close_order(order=order)

            # calculate the new amount of USDT to operate
            new_amount_usdt = self.order_utils.calculate_new_amount(amount=amount_in_usdt)

            # starting the bot again with more money
            if self.counter.should_enter_inversion_mode():
                await self.initialize(symbol=symbol,
                                      amount_in_usdt=new_amount_usdt,
                                      action=tp_next_order_type)
            else:
                await self.initialize(symbol=symbol,
                                      amount_in_usdt=new_amount_usdt,
                                      action=sl_next_order_type)

        else:
            print('**********************************************')
            print('Something went wrong waiting for a price match')
            print('**********************************************')
            return

    def calculate_amount_from_usdt(self, amount_in_usdt, coin_price):
        return round(amount_in_usdt / coin_price, self.repository.decimal_precision)

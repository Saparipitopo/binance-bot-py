import datetime
from app.features.bot.utils.counter_utils import CounterUtils


class PrintUtils:
    def __init__(self, counter: CounterUtils):
        self.counter = counter

    def print_loss_breakpoints(self, order_breakpoints):
        to_print = ['*****************',
                    'Loss breakpoints',
                    'TP: ' + str(order_breakpoints.profit) + '. SL: ' + str(order_breakpoints.loss),
                    '*****************']

        print(*to_print, sep='\n')

    def print_sl_action_info(self, next_action):
        to_print = ['*****************',
                    'Initializing stop loss iteration',
                    'Next action: ' + str(next_action),
                    '*****************']

        print(*to_print, sep='\n')

    def print_waiting_tp_sl(self, tp, sl, price):
        to_print = ['*****************',
                    'Waiting for TP (' + str(tp) + ' percentage: ' + str(
                        round(abs(100 - (tp * 100) / price), 3)) + '), or SL (' + str(sl) + 'percentage: ' + str(
                        round(abs(100 - (sl * 100) / price), 3)) + ')',
                    '*****************']

        print(*to_print, sep='\n')

    def print_waiting_for_high_low(self, high, low, price):
        to_print = ['*****************',
                    'Waiting for high (' + str(high) + ' percentage: ' + str(
                        round(abs(100 - (high * 100) / price), 3)) + '), or low (' + str(low) + ' percentage: ' + str(
                        round(abs(100 - (low * 100) / price), 3)) + ')',
                    '*****************']

        print(*to_print, sep='\n')

    def print_breakpoints(self, price, breakpoints):
        to_print = ['*****************',
                    'Initial breakpoints',
                    'Long band: ' + str(breakpoints.high) + ' percentage: ' + str(
                        round(abs(100 - (breakpoints.high * 100) / price), 3)),
                    'Short band: ' + str(breakpoints.low) + ' percentage: ' + str(
                        round(abs(100 - (breakpoints.low * 100) / price), 3)),
                    '*****************']

        print(*to_print, sep='\n')

    def print_initialize(self, amount_in_usdt, amount_to_operate, coin_price):
        self.print_time()

        to_print = ['*****************',
                    'Amount USDT to spend: ' + str(amount_in_usdt),
                    'Initial price: ' + str(coin_price),
                    'Token amount to operate: ' + str(amount_to_operate),
                    '*****************']

        print(*to_print, sep='\n')

    def print_time(self):
        to_print = ["\n @ " + str(datetime.datetime.now())]

        print(*to_print, sep='\n')

    def on_take_profit(self):
        self.print_time()

        to_print = ['******************',
                    '***   Profit   ***',
                    '******************']

        self.counter.add_take_profit_streak()
        self.counter.reset_stop_loss_streak()

        print(*to_print, sep='\n')

    def print_on_stop_loss(self):
        self.print_time()

        to_print = ['******************',
                    '***    Loss    ***',
                    '******************']

        print(*to_print, sep='\n')

        self.counter.add_stop_loss_count()
        self.counter.add_stop_loss_streak()

from config import Config


class CounterUtils:
    def __init__(self):
        self.take_profit_count = 0
        self.stop_loss_count = 0
        self.stop_loss_streak = 0

        # Config file variables
        cfg = Config()

        self.sleep_count = cfg.stop_loss_sleep_count
        self.sleep_take_profit_count = cfg.take_profit_sleep_count
        self.inversion_mode_count = cfg.stop_loss_to_inversion_count

    def add_stop_loss_count(self):
        self.stop_loss_count = self.stop_loss_count + 1

    def add_recovery_stop_loss_count(self):
        self.recovery_stop_loss_count = self.recovery_stop_loss_count + 1

    def add_take_profit_streak(self):
        self.take_profit_count = self.take_profit_count + 1

    def reset_stop_loss_streak(self):
        self.stop_loss_streak = 0

    def add_stop_loss_streak(self):
        self.stop_loss_streak = self.stop_loss_streak + 1

    def add_recovery_count(self):
        self.recovered_count = self.recovered_count + 1

    def print_counters(self):
        print('Take profit count: ', self.take_profit_count)
        print('Stop loss overall count: ', self.stop_loss_count)
        print('Stop loss streak: ', self.stop_loss_streak)
        print('Bot will sleep at ', self.sleep_count, ' consecutive stop losses')
        print('Bot will sleep at ', self.sleep_take_profit_count, ' take profits')

    def should_sleep_loss(self) -> bool:
        is_stop_loss_multiplier = self.is_multiplier(self.sleep_count, self.stop_loss_streak)

        return is_stop_loss_multiplier

    def should_sleep_win(self) -> bool:
        is_take_profit_multiplier = self.is_multiplier(self.sleep_take_profit_count, self.take_profit_count)

        return is_take_profit_multiplier

    def should_enter_inversion_mode(self) -> bool:
        is_inversion_multiplier = self.is_multiplier_unique(self.inversion_mode_count, self.recovery_stop_loss_count)
        if is_inversion_multiplier:
            self.recovery_stop_loss_count = 0

        return is_inversion_multiplier
    
    @staticmethod
    def is_multiplier(match, count) -> bool:
        if count == 0:
            return False
        elif match == 0:
            return False
        elif match <= count:
            return True

    @staticmethod
    def is_multiplier_unique(match, count) -> bool:
        if count == 0:
            return False
        elif match == 0:
            return False
        elif match == count:
            return True

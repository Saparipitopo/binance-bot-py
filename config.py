class Config():
    def __init__(self):
        # This is the multiplier to use after an SL to recover and take profit
        self.amount_multiplier = 2 / 3 # Default value is 4/3

        # The percentage of coin price variation needed to take profit
        self.take_profit = 0.03 # Default value is 0.03

        # The percentage of coin price variation needed to stop loss
        self.stop_loss = 0.01 # Default value is 0.01

        # The differences between the initial price and the sell or buy limits - (direction)
        self.initial_band_margin = 0.005 # Default value is 0.005

        # How many stop losses until the bot stops !!!!!!!!!!!!!!!
        self.stop_loss_sleep_count = 10 # Default 10

        # How many take profits until the bot stops !!!!!!!!!!!!!!!
        self.take_profit_sleep_count = 10 # Default 10

        # How many stop losses until the bot enters inversion mode on recovery - Reintento en la misma dirección.
        self.stop_loss_to_inversion_count = 2 # Default 2

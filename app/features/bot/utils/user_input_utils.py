import json
import pathlib

class UserInputUtils:
    def __init__(self):
        # initial setup
        self.is_test = None

        # coin setup
        self.symbol = None
        self.amount_in_usdt = None
        self.leverage = None

        # path to main folder for the print of the config_json file
        self.main_path = str(pathlib.Path(__file__).parent.parent.resolve())

    def get_coin_setup(self):
        self.is_test = self.get_yes_no_to_bool('Run in test mode? (y/n): ')

        self.symbol = input('Enter symbol to operate: ')
        self.amount_in_usdt = float(input('Enter amount in USDT to operate: '))
        self.leverage = input('Enter leverage to operate: ')

        self.print_config_json()

    def print_config_json(self):
        config = {'is_test': self.is_test,
                  'symbol': self.symbol,
                  'amount_in_usdt': self.amount_in_usdt,
                  'leverage': self.leverage}

        # Serializing json
        json_object = json.dumps(config, indent=4)

        # Writing to config_json.json
        with open(self.main_path + '\\bot_configs\\setup_json', "w") as config_json:
            config_json.write(json_object)

    def print_token_json(self, symbol):
        token = {'symbol': symbol}

        # Serializing json
        json_object = json.dumps(token, indent=1)

        # Writing to config_json.json
        with open(self.main_path + '\\bot_configs\\token_json', "w") as config_json:
            config_json.write(json_object)

    def get_setup_json(self):
        # Opening JSON file
        with open(self.main_path + '\\bot_configs\\setup_json', 'r') as openfile:
            # Reading from json file
            config_json = json.load(openfile)

        return config_json

    def get_token_json(self):
        # Opening JSON file
        with open(self.main_path + '\\bot_configs\\token_json', 'r') as openfile:
            # Reading from json file
            token_json = json.load(openfile)

        return token_json

    @staticmethod
    def get_yes_no_to_bool(title) -> bool:
        user_input = input(title)
        if user_input == 'Y':
            return True
        elif user_input == 'y':
            return True
        else:
            return False

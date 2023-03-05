class AccountInfo:
    def __init__(self, alias, asset, balance, withdraw_available, update_time):
        self.alias = alias
        self.asset = asset
        self.balance = balance
        self.withdraw_available = withdraw_available
        self.update_time = update_time


class AccountInfoMapper:
    @staticmethod
    def from_json(json):
        return AccountInfo(json['accountAlias'], json['asset'], json['balance'], json['withdrawAvailable'],
                           json['updateTime'])

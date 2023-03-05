import pandas as pd
from datetime import datetime
from app.features.bot.domain.entities.order import Order, ProfitType
from app.features.bot.domain.entities.order_type import OrderType


class OperationLogs:
    def __init__(self) -> None:
        columns = ['date_time', 'open_order', 'symbol', 'amount', 'type', 'price', 'tp', 'sl']
        self.df = pd.DataFrame(columns=columns)

    def create_log(self, order: Order):
        if order.type == OrderType.BUY:
            order.type = 'long'
        else:
            order.type = 'short'
        new_row = {
            'date_time': datetime.now(),
            'open_order': order.is_close_operation,
            'symbol': order.symbol,
            'amount': order.amount,
            'type': order.type,
            'price': order.price,
            'tp': order.take_profit,
            'sl': order.stop_loss,
        }
        rew_row_df = pd.DataFrame(data=new_row, index=[0])
        self.df = pd.concat([self.df, rew_row_df], ignore_index=True)
        self.df.to_excel('output.xlsx')


new_order = Order(symbol='ETHUSDT', amount='10', price='11', type=OrderType.BUY, take_profit='12', stop_loss='10',
                  profit_type=ProfitType.NEUTRAL)
logs = OperationLogs()
logs.create_log(order=new_order)

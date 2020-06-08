# Import the backtrader platform
import backtrader as bt

from bin.Util.util import line_of_best_fit

# Create a Stratey
class ScalpStrategy(bt.Strategy):
    params = (
        ('logging', True),
        ('long_rolling_gradient', 5)
    )

    def log(self, txt, dt=None, force_print=False):
        if force_print or self.params.logging:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.datalow = self.datas[0].low
        self.datahigh = self.datas[0].high
        self.datatime = self.datas[0].datetime

        # To keep track of pending orders and buy price/commission
        self.order = None

        # Indicators

        # Plot things
        self.buysell_ob = bt.observers.BuySell()
        self.value_ob = bt.observers.Cash()
        self.trades_ob = bt.observers.Trades()


    def notify_order(self, order):
        # Buy/Sell order submitted/accepted to/by broker - Nothing to do
        if order.status in [order.Submitted, order.Accepted]:
            return

        # Check if an order has been completed
        elif order.status in [order.Completed]:

            # Bought
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
            
            # Sold
            else:
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

        # Something went wrong with trade
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Clear order
        self.order = None


    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))


    def next(self):
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        elif not self.position:
            # Do check for if you want to buy then buy
            self.long_stratergy()

        else:
            # Do check to see if you want to sell use .close() it is easier
            self.close_stratergy()
            

    def long_stratergy(self):

        coords = []

        for i in range(-self.params.long_rolling_gradient, 1):
            coords.append((self.datatime[i], self.dataclose[i]))

        print(coords)
        input()
        print(line_of_best_fit(*coords))

    def close_stratergy(self):
        pass

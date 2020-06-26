# Import the backtrader platform
import backtrader as bt
from bin.Util.util import line_of_best_fit


# Create a Stratey
class EmaGradientInFollowOutStrategy(bt.Strategy):
    params = (
        ('logging', True),
        ('ema_small', 8),
        ('ema_meduim', 13),
        ('gradient_buyin', 0.5),
        ('gradient_nodes_num_buy', 5),
        ('gradient_sellout', -0.2),
        ('gradient_nodes_num_sell', 6),
        ('percentage_sell_bar', 0.01),
    )
    def __init__(self):
        # Keep a reference's to the line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.datalow = self.datas[0].low
        self.datahigh = self.datas[0].high
        self.datatime = self.datas[0].datetime

        # To keep track of pending orders and buy price/commission
        self.order = None

        # Indicators
        self.ema_s = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_small)
        self.ema_m = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_meduim)

        # Flags
        self.sell_bar = 0

        # Plot things
        self.buysell_ob = bt.observers.BuySell()
        self.value_ob = bt.observers.Cash()
        self.trades_ob = bt.observers.Trades()


    # Logging
    def log(self, txt, dt=None, force_print=False):
        if force_print or self.params.logging:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def stop(self):
        self.log('Ending Value %.2f' %
                 (self.broker.getvalue()), force_print=True)

    # Funcs
    def next(self):
        self.log(self.dataclose[0])
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        elif not self.position:
            # Do check for if you want to buy then buy
            if self.long_stratergy():
                self.order = self.buy(size=self.broker.get_cash()//self.dataclose[0])
                self.sell_bar = self.dataclose[0] * (1 - self.params.percentage_sell_bar)

        else:
            # Do check to see if you want to sell use .close() it is easier
            if self.close_stratergy():
                self.order = self.close()

        # Keep sell bar moving
        if self.dataclose[0] > self.dataclose[-1]:
            self.sell_bar = self.dataclose[0] * (1 - self.params.percentage_sell_bar)



    def long_stratergy(self):
        # Check for a cross over of the ema's where smaller ema is higher than medium ema
        if self.ema_s[0] > self.ema_m[0]:

            coords = []

            for i in range(-self.params.gradient_nodes_num_buy, 1):
                coords.append((self.datatime[i], self.dataclose[i]))

            # Now check that the gradient is good
            line = line_of_best_fit(*coords)

            if line[0][0] > self.params.gradient_buyin:
                return True

        return False


    def close_stratergy(self):
        
        if self.dataclose[0] < self.sell_bar:
            return True
        return False
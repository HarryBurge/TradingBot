# Import the backtrader platform
import backtrader as bt
import math

# Create a Stratey
class ScalpStrategy(bt.Strategy):
    params = (
        ('logging', True),
        ('commission', 0.01),
        ('order_percentage', 0.95),
        ('ema_small', 8),
        ('ema_meduim', 13),
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

        # To keep track of pending orders and buy price/commission
        self.order = None

        # Indicators
        self.ema_s = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_small)
        self.ema_m = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_meduim)

        # Flags
        self.s_above_m = False

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
            if self.ema_s > self.ema_m and self.s_above_m==False:

                amount_to_invest = self.params.order_percentage * self.broker.cash
                size = math.floor(amount_to_invest / self.dataclose)

                #Do a buy and change s_above_m to to true
                self.order = self.buy(size=size)
                self.s_above_m = True

        else:

            # Do check to see if you want to sell use .close() it is easier
            if self.ema_s < self.ema_m and self.s_above_m==True:
                # Do sell and change s_above_m to false
                self.close()
                self.s_above_m = False


    def stop(self):
        self.log('(EMA_s %2d) (EMA_m %2d) Ending Value %.2f' %
                 (self.params.ema_small, self.params.ema_meduim, self.broker.getvalue()), force_print=True)
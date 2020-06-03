# Import the backtrader platform
import backtrader as bt
import math

# Create a Stratey
class ScalpStrategy(bt.Strategy):
    params = (
        ('logging', True),
        ('ema_small', 8),
        ('ema_meduim', 13),
        ('ema_big', 21),
        ('plusminus', 0.03),
        ('amountattp1', 0.5),
        ('commission', 0.01),
        ('order_percentage', 0.95)
    )

    def log(self, txt, dt=None, force_print=False):
        if force_print or self.params.logging:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.passedtp1 = False

        # Indicators
        self.ema_s = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_small)
        self.ema_m = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_meduim)
        self.ema_b = bt.indicators.ExponentialMovingAverage(self.datas[0], period=self.params.ema_big)

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

            # Check for averages going up and that they are fanned out
            if self.ema_s > self.ema_m > self.ema_b:

                candlebot = min([self.dataclose, self.dataopen])

                # Trigger bar
                if candlebot < self.ema_s and candlebot > self.ema_b:
                    
                    maximum_value = max([self.dataclose[i] for i in range(-5, 1)] + [self.dataopen[i] for i in range(-5, 1)])
                    
                    self.buybeforepoint = maximum_value + self.params.plusminus

                    self.takelosspoint = min([self.dataclose, self.dataopen]) - self.params.plusminus

                    risk = abs(self.buybeforepoint - self.takelosspoint) + self.buybeforepoint*self.params.commission

                    self.takeprofitpoint1 = self.buybeforepoint + risk
                    self.takeprofitpoint2 = self.buybeforepoint + 2*risk

                    amount_to_invest = self.params.order_percentage * self.broker.cash
                    size = math.floor(amount_to_invest / self.dataclose)
                    self.order = self.buy(size=size, plimit=self.buybeforepoint, exectype=bt.Order.Limit)

        else:

            if self.dataclose <= self.takelosspoint:
                self.close()
                self.passedtp1 = False

            elif self.dataclose >= self.takeprofitpoint2:
                self.close()
                self.passedtp1 = False

            elif self.dataclose >= self.takeprofitpoint1 and self.passedtp1==False:
                self.order = self.sell(size=math.floor(self.broker.get_value() / self.dataclose)*0.5)
                self.passedtp1 = True

            elif self.dataclose <= self.takeprofitpoint1 and self.passedtp1==True:
                self.close()
                self.passedtp1 = False


    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (1, self.broker.getvalue()), force_print=True)
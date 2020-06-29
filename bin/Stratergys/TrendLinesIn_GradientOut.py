# Import the backtrader platform
import backtrader as bt


# Create a Stratey
class BlankStrategy(bt.Strategy):
    params = (
        ('logging', True),
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
                pass

        else:
            # Do check to see if you want to sell use .close() it is easier
            if self.close_stratergy():
                pass


    def long_stratergy(self):
        return True


    def close_stratergy(self):
        return True
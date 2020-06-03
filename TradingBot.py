import datetime
import os.path
import sys

# Import the backtrader platform
import backtrader as bt

from Stratergys.GoldenCrossStratergy import ScalpStrategy


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # strats = cerebro.optstrategy(
    #     ScalpStrategy,
    #     logging=False,
    #     ema_small=range(3,12),
    #     ema_meduim=range(12, 21))

    cerebro.addstrategy(ScalpStrategy)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, './BARCL.csv')

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2018, 1, 1),
        todate=datetime.datetime(2020, 5, 28),
        reverse=False)


    cerebro.adddata(data)
    cerebro.broker.setcash(1000.0)
    cerebro.broker.setcommission(commission=0.01)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run(maxcpus=1)

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()
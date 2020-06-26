__authour__ = 'Harry Burge'
__date_created__ = '04/06/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '04/06/2020'


# Imports
import backtrader as bt
import numpy

class Backtest:

    def __init__(self, stratergy, optimise=False, cash=1000.0, commission=0.00):
        self.cerebro = bt.Cerebro(stdstats=False)

        self.cerebro.broker.setcash(cash)
        self.cerebro.broker.setcommission(commission=commission)

        if not optimise:
            self.cerebro.addstrategy(stratergy)
        else:
            self.cerebro.optstrategy(
                    stratergy,
                    logging = False,
                    percentage_sell_bar = numpy.arange(0.001, 0.05, 0.001)
                    )

    
    def run_strat_on_data(self, data):
        self.cerebro.adddata(data)
        self.cerebro.run(maxcpus=1)


    def plot_results(self):
        self.cerebro.plot(style='candlestick')
# Imports
import backtrader as bt

from bin.alpha_vantage_class import StockDataAPI
from bin.backtesting_class import Backtest
from bin.Stratergys.GoldenCrossStratergy import ScalpStrategy


if __name__=='__main__':
    
    data_api = StockDataAPI('U94KFBUMZ4SY7DRA')
    # data = data_api.get_intraday_data('MSFT', '1min')[0]
    data = data_api.get_intraday_data('BA', '1min')[0]

    data.rename(columns={'date':'Date',
                         '2. high':'High',
                         '5. volume':'Volume',
                         '3. low':'Low',
                         '1. open':'Open',
                         '4. close':'Close'},
                inplace=True)

    print(data)

    data = bt.feeds.PandasData(dataname=data)

    broker = Backtest(ScalpStrategy, commission=0.01)

    broker.run_strat_on_data(data)
    broker.plot_results()
# Imports
import backtrader as bt

from bin.alpha_vantage_class import StockDataAPI
from bin.backtesting_class import Backtest

from bin.Stratergys.GoldenCrossStratergy import GoldenCrossStrategy
from bin.Stratergys.EmaGradientIn_FollowOutStratergy import EmaGradientInFollowOutStrategy
from bin.Stratergys.TrendLinesIn_GradientOut import BlankStrategy


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

    # Flip because data is inverted
    data = data.reindex(index=data.index[::-1])

    # Shorten data
    data = data.truncate('2020-06-24 09:35:00', '2020-06-24 10:35:00')
    print(data)

    data = bt.feeds.PandasData(dataname=data)

    broker = Backtest(BlankStrategy, commission=0.00, optimise=False) #0.005

    broker.run_strat_on_data(data)
    broker.plot_results()
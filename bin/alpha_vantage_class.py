__authour__ = 'Harry Burge'
__date_created__ = '04/06/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '04/06/2020'

# Imports
# import pandas
from alpha_vantage.timeseries import TimeSeries


# Stock Data API
class StockDataAPI:
    '''
    Is a connection to the alpha vantage API
    '''

    def __init__(self, api_key, output_format='pandas'):
        self.api = TimeSeries(key=api_key, output_format=output_format)

    
    def get_intraday_data(self, symbol, interval, outputsize='full'):
        data, meta_data = self.api.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
        return data, meta_data

    def get_day_data(self, symbol, outputsize='full'):
        data, meta_data = self.api.get_daily(symbol=symbol, outputsize=outputsize)
        return data, meta_data


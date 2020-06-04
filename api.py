from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas

ts = TimeSeries(key='U94KFBUMZ4SY7DRA', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
# print(data)
data['4. close'].plot()
# data['1. open'].plot()
data['2. high'].plot()
data['3. low'].plot()
plt.title('Intraday Times Series for the MSFT stock (1 min)')
plt.show()


# from alpha_vantage.techindicators import TechIndicators
# import matplotlib.pyplot as plt
# import pandas

# ti = TechIndicators(key='U94KFBUMZ4SY7DRA', output_format='pandas')
# data, meta_data = ti.get_bbands(symbol='MSFT', interval='60min', time_period=60)
# data.plot()
# plt.title('BBbands indicator for  MSFT stock (60 min)')
# plt.show()


# from alpha_vantage.sectorperformance import SectorPerformances
# import matplotlib.pyplot as plt

# sp = SectorPerformances(key='YOUR_API_KEY', output_format='pandas')
# data, meta_data = sp.get_sector()
# data['Rank A: Real-Time Performance'].plot(kind='bar')
# plt.title('Real Time Performance (%) per Sector')
# plt.tight_layout()
# plt.grid()
# plt.show()


# from alpha_vantage.cryptocurrencies import CryptoCurrencies
# import matplotlib.pyplot as plt

# cc = CryptoCurrencies(key='U94KFBUMZ4SY7DRA', output_format='pandas')
# data, meta_data = cc.get_digital_currency_daily(symbol='BTC', market='CNY')
# data['4b. close (USD)'].plot()
# plt.tight_layout()
# plt.title('Daily close value for bitcoin (BTC)')
# plt.grid()
# plt.show()
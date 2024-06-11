import pandas as pd
import mplfinance as mpf
import datetime

# Load data and convert 'DateTime' column to datetime objects
df = pd.read_csv("data/EURUSD_tickdata.csv").dropna().iloc[-1000:]
df['DateTime'] = df['DateTime'].apply(lambda x: datetime.datetime.strptime(x, '%d.%m.%Y %H:%M:%S.%f'))

# Group by minute and calculate OHLC
grouped_data = df.groupby(pd.Grouper(freq='1Min', key='DateTime'))
candles = grouped_data.agg({'Ask': ['first', 'max', 'min', 'last'], 'Bid': ['first', 'max', 'min', 'last']})

# Renaming columns for Ask and Bid to match Open, High, Low, Close
candles.columns = ['Ask_Open', 'Ask_High', 'Ask_Low', 'Ask_Close', 'Bid_Open', 'Bid_High', 'Bid_Low', 'Bid_Close']

# Create DataFrame with the required columns for mplfinance
ohlc_data = candles[['Ask_Open', 'Ask_High', 'Ask_Low', 'Ask_Close']]
ohlc_data.columns = ['Open', 'High', 'Low', 'Close']

# Plot OHLC candles
mpf.plot(ohlc_data, type='candle', style='yahoo', title='EURUSD OHLC Candles', ylabel='Price')
mpf.show()

import re
import json
import requests
import yfinance
import datetime as dt
import indicators
from utils import utils
import numpy as np
from pprint import pprint
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import matplotlib.dates as date
from argparse import ArgumentParser
from tradingview_ta import TA_Handler, Interval, Exchange, technicals


# Step 1 : Choose Stock and Dates
START_DATE = '1975-01-01'
TODAY = dt.datetime.now().strftime("%Y-%m-%d")

# Stock information
stock = {'symbol': "KO",
         'title': 'COCA-COLA',
         'screener': "america",
         'exchange': "NASDAQ",
         }

# Step 2 : Get Datas
class DataBase:
    def __init__(self, ticker, startdate, today):
        # Donnée du Stock
        self.stock = ticker
        self.stock_data = yfinance.download(self.stock['symbol'], startdate, today)
        self.df = pd.DataFrame(self.stock_data)
        pd.set_option('display.max_columns', None)

    def quote(self):
        return self.df


db = DataBase(stock, START_DATE, TODAY)
df = db.quote()
dfRes = utils.createZigZagPoints(df['Close']).dropna()
# pprint(df.keys())

higher_price = df['Close'].idxmax()
# dates = pd.to_datetime(df.index)

# Indicateurs
longSMA = df['Close'].rolling(window=200).mean()
longEMA = df['Close'].ewm(span=200).mean()
rsi = indicators.RSI(df['Close'])

# Step 3 : Visualisation un tableau avec Matplotlib
plt.rcParams.update({'font.size':10})
fig, ax1 = plt.subplots(figsize=(15, 8))

# Settings, Labels, Titles
ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.set_title(stock['title'])
ax1.grid()

# Import plot DATAs
ax1.plot(df['Close'], color='red')
ax1.plot(dfRes['Value'], color='green')
# ax1.plot(longSMA, color='red', label='MA200')
# ax1.plot(longEMA, color='green', label='EMA200')


######## Supports & Resistances ########

resistances = indicators.resistances(df, ranges=365)
timeD = dt.timedelta(days=300)
for price, dates in resistances.items():
    plt.plot_date([df.index[0], df.index[-1]],
                  [price, price],
                  linestyle="-", linewidth=8, color='red', alpha=0.2)

######## Tableau RSI ########

# plt.axes([0.04, 0.2, .9, 0.75])
# plt.axes([0.04, 0.05, .9, 0.1])
# plt.plot(df['Close'])
# plt.xlabel('Date')

# ax1.legend()
plt.show()



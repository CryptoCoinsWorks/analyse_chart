import datetime as dt

import matplotlib.pyplot as plt
import pandas as pd
import yfinance

import indicators
import numpy as np
from utils import utils
from pprint import pprint
from scipy import signal

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


db = DataBase(stock, START_DATE, TODAY) #"2020-01-01"
df = db.quote()

higher_price = df['Adj Close'].idxmax()
dates = pd.to_datetime(df.index)
df_close = df['Adj Close']

# Indicateurs
longSMA = df_close.rolling(window=200).mean()
longEMA = df_close.ewm(span=200).mean()
rsi = indicators.RSI(df_close)

# Step 3 : Visualisation un tableau avec Matplotlib
plt.rcParams.update({'font.size': 10})
fig, ax1 = plt.subplots(figsize=(15, 8))

# Settings, Labels, Titles
ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.set_title(stock['title'])
ax1.grid()

ax1.plot(df_close, color='blue')


# Import plot DATAs
ax1.plot(longSMA, color='red', label='MA200')
ax1.plot(longEMA, color='green', label='EMA200')


######## Zig Zag ########

zigzag = indicators.zig_zag(values=df_close)
ax1.plot(df_close[zigzag], color="green")
plt.scatter(dates[zigzag], df_close[zigzag], color="green")


######## Supports & Resistances ########

resistances = indicators.get_resistances(df_close.values, closest=0.8)
for resis in resistances:
    plt.axhline(y=resis, linestyle="-", linewidth=8, color='red', alpha=0.2)


# resistances = indicators.resistances(df)#, closest=0.8)
# timeD = dt.timedelta(days=300)
# for price, dates in resistances.items():
    # plt.plot_date([df.index[0], df.index[-1]],
    #               [price, price],
    #               linestyle="-", linewidth=8, color='red', alpha=0.2)

######## Tableau RSI ########

# plt.axes([0.04, 0.2, .9, 0.75])
# plt.axes([0.04, 0.05, .9, 0.1])
# plt.plot(df['Close'])
# plt.xlabel('Date')


ax1.legend()
plt.show()

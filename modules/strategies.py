from pprint import pprint
import numpy as np
from utils import indicators


def MACD_strategy(values):
    short_EMA = indicators.expo_moving_average(values['close'], w=12)
    long_EMA = indicators.expo_moving_average(values['close'], w=26)
    macd = short_EMA - long_EMA
    signal = indicators.expo_moving_average(macd, w=9)
    values['MACD'] = macd
    values['Signal'] = signal
    retournement = buy_sell_macd(values)
    # values['Buy'] = retournement
    values['Buy'] = retournement[0]
    values['Sell'] = retournement[1]
    return values

def buy_sell_macd(values, offset=0.01):
    offset_up = 1+offset
    offset_down = 1-offset
    buy = []
    sell = []
    # if 2 lines cross Flag change
    flag = -1
    ema200 = values['close'].ewm(com=200).mean()

    for i in range(0, len(values)):
        if values['MACD'][i] > values['Signal'][i]:# and values['close'][i] > ema200[i]:
            sell.append(np.nan)
            if flag != 1:
                buy.append(values['close'][i]*offset_up)
                flag = 1
            else:
                buy.append(np.nan)

        elif values['MACD'][i] < values['Signal'][i]:# and values['close'][i] < ema200[i]:
            buy.append(np.nan)
            if flag != 0:
                sell.append(values['close'][i]*offset_down)
                flag = 0
            else:
                sell.append(np.nan)
        else:
            buy.append(np.nan)
            sell.append(np.nan)
    return (buy, sell)



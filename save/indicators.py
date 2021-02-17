from pprint import pprint
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
from statistics import mean
from scipy import signal



def RSI(stock):
    rsi_period = 14
    change = stock.diff()
    gain = change.mask(change < 0, 0)
    loss = change.mask(change > 0, 0)
    average_gain = gain.ewm(com=rsi_period - 1, min_periods=rsi_period).mean()
    average_loss = loss.ewm(com=rsi_period - 1, min_periods=rsi_period).mean()
    rs = abs(average_gain / average_loss)
    rsi = 100 - (100 / (1 + rs))
    return rsi

#### RESISTANCES ####

def resistances(df, ranges=350):
    key = "Close"

    threshold = 0.1
    n_ltp = df.shape[0]

    max_values = [max(df[key][i:i+ranges]) for i in range(0, len(df[key]), ranges)]
    max_threshold = [x + threshold for x in max_values]
    min_threshold = [x - threshold for x in max_values]

    dic_all_res = {}
    for i in range(n_ltp):
        if df[key][i] in max_values:
            if df[key][i] in dic_all_res.keys():
                dic_all_res[df[key][i]].append(df.index[i])
            else:
                dic_all_res[df[key][i]] = []
                dic_all_res[df[key][i]].append(df.index[i])

    return dic_all_res


def get_max_min(stock, smoothing=120, ranges=350):
    smooth_prices = stock['Close'].rolling(window=smoothing).mean().dropna()
    local_max = [max(smooth_prices[i:i + ranges]) for i in range(0, len(smooth_prices), ranges)]
    # local_max = argrelextrema(smooth_prices.values, np.greater)[0]
    # local_min = argrelextrema(smooth_prices.values, np.less)[0]
    # pprint(smooth_prices)
    price_local_max_dt = {}
    for i in range(len(smooth_prices)):
        if smooth_prices[i] in local_max:
            price_local_max_dt[smooth_prices[i]] = smooth_prices.index[i]

    return price_local_max_dt, smooth_prices


def get_max_min_ori(prices, smoothing=120, window_range=10):
    smooth_prices = prices['Close'].rolling(window=smoothing).mean().dropna()
    local_max = argrelextrema(smooth_prices.values, np.greater)[0]
    local_min = argrelextrema(smooth_prices.values, np.less)[0]
    price_local_max_dt = []
    for i in local_max:
        if (i > window_range) and (i < len(prices) - window_range):
            price_local_max_dt.append(prices.iloc[i - window_range:i + window_range]['Close'].idxmax())
    price_local_min_dt = []
    for i in local_min:
        if (i > window_range) and (i < len(prices) - window_range):
            price_local_min_dt.append(prices.iloc[i - window_range:i + window_range]['Close'].idxmin())
    maxima = pd.DataFrame(prices.loc[price_local_max_dt])
    minima = pd.DataFrame(prices.loc[price_local_min_dt])
    max_min = pd.concat([maxima, minima]).sort_index()
    max_min.index.name = 'date'
    max_min = max_min.reset_index()
    max_min = max_min[~max_min.date.duplicated()]
    p = prices.reset_index()
    # max_min['day_num'] = p[p.index.isin(max_min.date)].index.values
    # max_min = max_min.set_index('day_num')['Close']

    return max_min

           ####

def _peaks_detection(values, rounded=3, direction="up"):
    """Peak detection for the given data.

    :param values: All values to analyse
    :type values: np.array
    :param rounded: round values of peaks with n digits, defaults to 3
    :type rounded: int, optional
    :param direction: The direction is use to find peaks.
    Two available choices: (up or down), defaults to "up"
    :type direction: str, optional
    :return: The list of peaks founded
    :rtype: list
    """
    data = np.copy(values)
    if direction == "down":
        data = -data
    peaks, _ = signal.find_peaks(data, height=min(data))
    if rounded:
        peaks = [abs(round(data[val], rounded)) for val in peaks]
    return peaks


def group_values_nearest(values):
    # values.sort()
    il = []
    ol = []
    for k, v in enumerate(values):
        if k <= 0:
            continue
        if abs(values[k] - values[k-1]) < 3:
            if values[k-1] not in il:
                il.append(values[k-1])
            if values[k] not in il:
                il.append(values[k])
        else:
            ol.append(list(il))
            il = []
    ol.append(list(il))
    return ol


def get_resistances(values, closest=2):
    """Get resistances in values

    :param values: Values to analyse
    :type values: np.array
    :param closest: The value for grouping. It represent the max difference
    between values in order to be considering inside the same
    bucket, more the value is small, more the result will be precises.
    defaults to 2
    :type closest: int, optional
    :return: list of values which represents resistances
    :rtype: list
    """
    return _get_support_resistances(
        values=values, direction="up", closest=closest
    )


def _get_support_resistances(values, direction, closest=2):
    """Private function which found all supports and resistances

    :param values: values to analyse
    :type values: np.array
    :param direction: The direction (up for resistances, down for supports)
    :type direction: str
    :param closest: closest is the maximun value difference between two values
    in order to be considering in the same bucket, default to 2
    :type closest: int, optional
    :return: The list of support or resistances
    :rtype: list
    """
    result = []
    # Find peaks
    peaks = _peaks_detection(values=values, direction=direction)
    # Group by nearest values
    peaks_grouped = group_values_nearest(values=peaks, closest=closest)
    # Mean all groups in order to have an only one value for each group
    for val in peaks_grouped:
        if not val:
            continue
        if len(val) < 3:  # need 3 values to confirm resistance
            continue
        result.append(mean(val))
    return result


def group_values_nearest(values, closest=2):
    """Group given values together under multiple buckets.

    :param values: values to group
    :type values: list
    :param closest: closest is the maximun value difference between two values
    in order to be considering in the same bucket, defaults to 2
    :type closest: int, optional
    :return: The list of the grouping (list of list)
    :rtype: list    s
    """
    values.sort()
    il = []
    ol = []
    for k, v in enumerate(values):
        if k <= 0:
            continue
        if abs(values[k] - values[k - 1]) < closest:
            if values[k - 1] not in il:
                il.append(values[k - 1])
            if values[k] not in il:
                il.append(values[k])
        else:
            ol.append(list(il))
            il = []
    ol.append(list(il))
    return ol


#### ZIG ZAG ####

def zig_zag(values, distance=2.1):
    peaks_up, _ = signal.find_peaks(values, prominence=1, distance=distance)
    peaks_down, _ = signal.find_peaks(-values, prominence=1, distance=distance)

    indexs = [i for i in peaks_up]
    indexs.extend([i for i in peaks_down])
    indexs.sort()

    return indexs
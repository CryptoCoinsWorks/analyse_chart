from pprint import pprint
from urllib3.connectionpool import xrange


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

def supports_resistances(stock):
    x = 50
    contact = 3
    pivots = []
    dates = []
    counter = 0
    lastPivot = 0

    ranges = [0] * x
    dateRange = [0] * x

    for i in stock.index:
        currentMax = max(ranges, default=0)
        value = stock['Value'][i]#round(stock['Value'][i], 50)
        ranges = ranges[1:x-1]
        ranges.append(value)
        dateRange = dateRange[1:x-1]
        dateRange.append(i)
        # print(len(ranges))
        if currentMax == max(ranges, default=0):
            counter += 1
        else:
            counter = 0

        if counter == 15:
            lastPivot = currentMax
            dateloc = ranges.index(lastPivot)
            lastDate = dateRange[dateloc]

            pivots.append(lastPivot)
            dates.append(lastDate)

    return pivots, dates


def isSupport(df,i):
  support = df['Low'][i] < df['Low'][i-1] and df['Low'][i] < df['Low'][i + 1] < df['Low'][i + 2] and df['Low'][i - 1] < df['Low'][i - 2]
  return support

def isResistance(df,i):
  resistance = df['High'][i] > df['High'][i-1] and df['High'][i] > df['High'][i + 1] > df['High'][i + 2] and df['High'][i - 1] > df['High'][i - 2]
  return resistance

def isFarFromLevel(l, levels, np, s):
  return np.sum([abs(l-x) < s for x in levels]) == 0


def supres(ltp, n, np):
    """
    This function takes a numpy array of last traded price
    and returns a list of support and resistance levels
    respectively. n is the number of entries to be scanned.
    """
    from scipy.signal import savgol_filter as smooth

    # converting n to a nearest even number
    if n % 2 != 0:
        n += 1

    n_ltp = ltp.shape[0]

    # smoothening the curve
    ltp_s = smooth(ltp, (n + 1), 3)

    # taking a simple derivative
    ltp_d = np.zeros(n_ltp)
    ltp_d[1:] = np.subtract(ltp_s[1:], ltp_s[:-1])

    resistance = []
    support = []

    for i in xrange(n_ltp - n):
        arr_sl = ltp_d[i:(i + n)]
        first = arr_sl[:(n / 2)]  # first half
        last = arr_sl[(n / 2):]  # second half

        r_1 = np.sum(first > 0)
        r_2 = np.sum(last < 0)

        s_1 = np.sum(first < 0)
        s_2 = np.sum(last > 0)

        # local maxima detection
        if (r_1 == (n / 2)) and (r_2 == (n / 2)):
            resistance.append(ltp[i + ((n / 2) - 1)])

        # local minima detection
        if (s_1 == (n / 2)) and (s_2 == (n / 2)):
            support.append(ltp[i + ((n / 2) - 1)])

    return support, resistance

def resistances(df):
    ranges = 350
    threshold = 2
    n_ltp = df.shape[0]
    max_values = [max(df['High'][i:i+ranges]) for i in range(0, len(df['High']), ranges)]
    dic_res = {}
    for i in range(n_ltp):
        if df['Close'][i] in max_values: # AJOUTER LE THRESHOLD
            if df['Close'][i] in dic_res.keys():
                dic_res[df['Close'][i]].append(df.index[i])
            else:
                dic_res[df['Close'][i]] = []
                dic_res[df['Close'][i]].append(df.index[i])

    pprint(dic_res)



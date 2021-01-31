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
        # if any(max_th > df[key][i] for max_th in max_threshold) and any(min_th < df[key][i] for min_th in min_threshold):
            if df[key][i] in dic_all_res.keys():
                dic_all_res[df[key][i]].append(df.index[i])
            else:
                dic_all_res[df[key][i]] = []
                dic_all_res[df[key][i]].append(df.index[i])

    # pprint(dic_all_res)

    # Recupere prix tres similaire ensemble
    # similar_price = {}
    # for ind, price in enumerate(dic_all_res.keys()):
    #     ls_values = [x*-1 if x < 0 else x for x in price - [x for x in dic_all_res.keys()]]
    #     # pprint(ls_values)
    #     similar_price[ind] = []
    #     for index, i in enumerate(ls_values):
    #         if i < 1.5:
    #             similar_price[ind].append(price)
    #             similar_price[ind].append(list(dic_all_res)[index])
    # pprint(similar_price)
    # # Enleve duplicate value
    # results = {}
    # for key, value in similar_price.items():
    #     results[key] = []
    #     for v in value:
    #         if v not in results[key]:
    #             results[key].append(v)

    # pprint(results)
    return dic_all_res



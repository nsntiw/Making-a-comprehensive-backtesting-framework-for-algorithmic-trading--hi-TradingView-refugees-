#https://medium.com/@FMZQuant/quantitative-trading-strategy-based-on-double-moving-average-crossover-d28b85577152
#not working as intended
from Strategy.Library import SMA
from ta.volume import OnBalanceVolumeIndicator
import pandas as pd

def calculate_obv(data_feed):
    obv_indicator = OnBalanceVolumeIndicator(close=data_feed['Close'], volume=data_feed['Volume'])
    return obv_indicator.on_balance_volume()

def calculate_vt(data_feed, period):
    close = data_feed['Close']
    volume = data_feed['Volume']
    vt_values = [close.diff().iloc[-i] / close.iloc[-i - 1] * volume.iloc[-1] for i in range(1, period)]
    vt = sum(vt_values)
    return vt

def MAQuantitative_long(data_feed):
    if len(data_feed) < 21:
        return 0, 0, 0
    #Strategy parametres
    ma_length = 20
    limit = 1
    TP_rate = 1.05
    SL_rate = 0.99
    #OBV
    obv = calculate_obv(data_feed)

    smoothing_line_ma = []
    smoothing_line_ma.append(SMA(obv, ma_length))
    smoothing_line_ma.append(SMA(obv.shift(1), ma_length))
    obv_diff = []
    obv_diff.append((obv.iloc[0] - smoothing_line_ma[0]) * 100 / obv.iloc[0])
    obv_diff.append((obv.iloc[1] - smoothing_line_ma[1]) * 100 / obv.iloc[1])

    #PVT
    vt = [calculate_vt(data_feed.tail(100).shift(i), len(data_feed.tail(100))-i) for i in range(21)]
    smoothing_line_map = []
    smoothing_line_map.append(SMA(pd.Series(vt), ma_length))
    smoothing_line_map.append(SMA(pd.Series(vt[1:]), ma_length))
    pvt_diff = []
    pvt_diff.append((vt[0] - smoothing_line_map[0]) * 100 / vt[0])
    pvt_diff.append((vt[1] - smoothing_line_map[1]) * 100 / vt[1])

    indicator = []
    indicator.append((pvt_diff[0] + obv_diff[0]) / 2)
    indicator.append((pvt_diff[1] + obv_diff[1]) / 2)

    long_cond = indicator[0] > limit and indicator[1] < limit

    #stopLoss = low * 0.99 // -2%
    #takeProfit = high * 1.05 // +5%
    if long_cond:
        return 1, data_feed['High'].iloc[-1] * TP_rate, data_feed['Low'].iloc[-1] * SL_rate
    return 0, 0, 0


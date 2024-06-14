#https://medium.com/@FMZQuant/ema-macd-supertrend-adx-atr-multi-indicator-trading-signal-strategy-9a6569b1f04d
import numpy as np
import pandas as pd
from Strategy.Library import MACD, EMA

def MACD_long(data_feed):
    #MACD parameters
    short_ma_length, long_ma_length, signal_length, EMA_length = 12, 26, 9, 200
    macd, signal = MACD(data_feed, short_ma_length, long_ma_length, signal_length)
    ema_filter = EMA(data_feed['Close'], EMA_length)
    #Generate strategy signal
    if(macd > signal and signal < 0 and data_feed['Close'].iloc[-1] > ema_filter):
        #works without np.isnan()
        return 1
    if(macd < signal):
        return -1
    return 0

def MACD_short(data_feed):
    #MACD parameters
    short_ma_length, long_ma_length, signal_length, EMA_length = 5, 12, 9, 200
    macd, signal = MACD(data_feed, short_ma_length, long_ma_length, signal_length)
    ema_filter = EMA(data_feed['Close'], EMA_length)
                     
    #Generate strategy signal
    if(macd < signal and signal > 0 and data_feed['Close'].iloc[-1] < ema_filter):
        return 1
    if(macd > signal):
        return -1
    return 0
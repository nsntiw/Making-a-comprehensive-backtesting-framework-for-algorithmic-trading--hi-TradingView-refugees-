#https://medium.com/@FMZQuant/ema-macd-supertrend-adx-atr-multi-indicator-trading-signal-strategy-9a6569b1f04d
import numpy as np
import pandas as pd

from Strategy.Library import MACD, SMA

def MACD_long(data_feed):
    #MACD parameters
    short_ma_length, long_ma_length = 5, 12

    #Calculate short and long simple moving averages
    short_ma = SMA(data_feed['Close'], short_ma_length)
    long_ma = SMA(data_feed['Close'], long_ma_length)

    #Return strategy signal
    return (1, 0, 0) if short_ma > long_ma else (-1, 0, 0)

def MACD_short(data_feed):
    #MACD parameters
    short_ma_length, long_ma_length = 5, 12

    #Calculate short and long simple moving averages
    short_ma = SMA(data_feed['Close'], short_ma_length)
    long_ma = SMA(data_feed['Close'], long_ma_length)

    #Return strategy signal
    return (1, 0, 0) if short_ma < long_ma else (-1, 0, 0)
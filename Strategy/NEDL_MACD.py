#https://www.youtube.com/watch?v=EAok0kAHnCU&list=PLE4a3phdCOauXaK3f1QMI_fEIqEYTsH9I
import numpy as np
import pandas as pd
from Strategy.Library import SMA

def MACD_long(data_feed):
    #MACD parameters
    short_ma_length, long_ma_length = 5, 12
    #calculate short and long simple moving averages
    short_ma = SMA(data_feed['Close'], short_ma_length)
    long_ma = SMA(data_feed['Close'], long_ma_length)
    SMA_filter = SMA(data_feed['High'], 100)

    #print(data_feed['Close'].iloc[-1])
    #print(SMA_filter)
    #and data_feed['Close'].iloc[-1] > SMA_filter
    return 1 if short_ma > long_ma else -1

def MACD_short(data_feed):
    #MACD parameters
    short_ma_length, long_ma_length = 5, 12
    #calculate short and long simple moving averages
    short_ma = SMA(data_feed['Close'], short_ma_length)
    long_ma = SMA(data_feed['Close'], long_ma_length)
    SMA_filter = SMA(data_feed['Low'], 100)

    #and data_feed['Close'].iloc[-1] < SMA_filter
    return 1 if short_ma < long_ma else -1
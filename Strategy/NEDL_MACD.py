#https://www.youtube.com/watch?v=EAok0kAHnCU&list=PLE4a3phdCOauXaK3f1QMI_fEIqEYTsH9I
import numpy as np
import pandas as pd
from Strategy.Library import SMA

def MACD_long(data_feed):
    #MACD parameters
    short_ma_length = 5
    long_ma_length = 12
    #calculate short and long simple moving averages
    short_ma = SMA(data_feed['Close'], short_ma_length)
    long_ma = SMA(data_feed['Close'], long_ma_length)
    
    if short_ma > long_ma:
        return 1
    else:
        return -1

def MACD_short(data_feed):
    #MACD parameters
    short_ma_length = 5
    long_ma_length = 12
    #calculate short and long simple moving averages
    short_ma = SMA(data_feed['Close'], short_ma_length)
    long_ma = SMA(data_feed['Close'], long_ma_length)

    if short_ma < long_ma:
        return 1
    else:
        return -1
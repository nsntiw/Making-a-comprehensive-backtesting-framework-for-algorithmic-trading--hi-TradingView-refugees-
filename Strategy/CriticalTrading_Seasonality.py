#https://youtu.be/6BjHuc_F8Lk?si=kycLmhur8IO-q3rt
import numpy as np
import pandas as pd
from Strategy.Library import SMA, high

def SPY_seasonality_long(data_feed):
    #Calculate SMA and last high
    SMA_length = 200
    SMA_filter = SMA(data_feed['Close'], SMA_length)
    last_high = data_feed['High'].shift(1).iloc[-1]

    #Return strategy signal
    if pd.offsets.MonthEnd().is_month_end(data_feed.index[-1]) and data_feed['Close'].iloc[-1] > SMA_filter:
        return 1, 0, 0
    if data_feed['Close'].iloc[-1] > last_high:
        return -1, 0, 0
    return 0, 0, 0

def SPY_seasonality_short(data_feed):
    return 0, 0, 0

def TLT_seasonality_long(data_feed):
    #Calculate SMA and last high
    SMA_length = 5
    SMA_filter = SMA(data_feed['Close'], SMA_length)
    last_high = data_feed['High'].shift(1).iloc[-1]

    #Return strategy signal
    if data_feed.index[-1].day_name() == 'Thursday' and data_feed['Close'].iloc[-1] < SMA_filter:
        return 1, 0, 0
    if data_feed['Close'].iloc[-1] > last_high:
        return -1, 0, 0
    return 0, 0, 0

def TLT_seasonality_short(data_feed):
    return 0, 0, 0
#https://youtu.be/dfT6rnkJCms?si=eHZWQoDF46QAwftp
import numpy as np
import pandas as pd
from Strategy.Library import RSI, SMA

def RSI_long(data_feed):
    #RSI parameters
    rsi_period = 2
    rsi_oversold = 10
    rsi_overbought = 90
    SMA_length = 200

    #Calculate RSI
    rsi = RSI(data_feed['Close'], rsi_period)
    rsi_prev = RSI(data_feed['Close'].shift(1), rsi_period)
    SMA_filter = SMA(data_feed['Close'], SMA_length)

    #Return strategy signal
    #if (rsi > rsi_oversold and rsi_prev < rsi_oversold) and data_feed['Close'].iloc[-1] > SMA_filter:
    if rsi < rsi_oversold and data_feed['Close'].iloc[-1] > SMA_filter:
        return 1, 0, 0
    if rsi > rsi_overbought:
        return -1, 0, 0
    else:
        return 0, 0, 0

#for some reason it doesn't generate short trades when crossunder is applied
def RSI_short(data_feed):
    #RSI parameters
    rsi_period = 2
    rsi_oversold = 10
    rsi_overbought = 90
    SMA_length = 200

    #Calculate RSI
    rsi = RSI(data_feed['Close'], rsi_period)
    rsi_prev = RSI(data_feed['Close'].shift(1), rsi_period)
    SMA_filter = SMA(data_feed['Close'], SMA_length)

    #Return strategy signal
    #if (rsi < rsi_overbought and rsi > rsi_overbought) and data_feed['Close'].iloc[-1] < SMA_filter:
    if  rsi > rsi_overbought and data_feed['Close'].iloc[-1] < SMA_filter:
        return 1, 0, 0
    if rsi < rsi_oversold:
        return -1, 0, 0
    else:
        return 0, 0, 0
    
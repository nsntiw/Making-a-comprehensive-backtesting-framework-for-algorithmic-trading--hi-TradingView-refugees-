#https://youtu.be/dfT6rnkJCms?si=eHZWQoDF46QAwftp
import numpy as np
import pandas as pd
from Strategy.Library import RSI, SMA

def RSI_long(data_feed):
    #RSI parameters
    rsi_period = 2
    rsi_oversold = 95
    rsi_overbought = 5
    SMA_length = 200

    #Calculate RSI
    rsi = RSI(data_feed, rsi_period)
    SMA_filter = SMA(data_feed['Close'], SMA_length)
    
    #Return strategy signal
    if rsi < rsi_oversold and data_feed['Close'].iloc[-1] > SMA_filter:
        return 1, 0, 0
    if rsi > rsi_overbought:
        return -1, 0, 0
    else:
        return 0, 0, 0
    
def RSI_short(data_feed):
    #RSI parameters
    rsi_period = 2
    rsi_oversold = 95
    rsi_overbought = 5
    SMA_length = 200

    #Calculate RSI
    rsi = RSI(data_feed, rsi_period)
    SMA_filter = SMA(data_feed['Close'], SMA_length)

    #Return strategy signal
    if rsi > rsi_overbought and data_feed['Close'].iloc[-1] < SMA_filter:
        return 1, 0, 0
    if rsi < rsi_oversold:
        return -1, 0, 0
    else:
        return 0, 0, 0
    
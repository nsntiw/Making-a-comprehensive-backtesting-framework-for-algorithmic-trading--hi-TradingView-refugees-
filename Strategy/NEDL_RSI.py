#https://youtu.be/dfT6rnkJCms?si=eHZWQoDF46QAwftp
import numpy as np
import pandas as pd

def RSI_long(data_feed):
    #RSI parameters
    rsi_period = 14
    rsi_oversold = 30
    rsi_overbought = 70
    #calculate RSI
    up = np.maximum(data_feed['Close'].diff(),0)
    down = np.maximum(-data_feed['Close'].diff(),0)
    rs = up[-rsi_period:].mean() / down[-rsi_period:].mean()
    rsi = 100 - 100/(1 + rs)
    #return signal
    if rsi < rsi_oversold:
        return 1
    if rsi > rsi_overbought:
        return -1
    else:
        return 0
    
def RSI_short(data_feed):
    #RSI parameters
    rsi_period = 14
    rsi_oversold = 30
    rsi_overbought = 70
    #calculate RSI
    up = np.maximum(data_feed['Close'].diff(),0)
    down = np.maximum(-data_feed['Close'].diff(),0)
    rs = up[-rsi_period:].mean() / down[-rsi_period:].mean()
    rsi = 100 - 100/(1 + rs)
    #return signal
    if rsi > rsi_overbought:
        return 1
    if rsi < rsi_oversold:
        return -1
    else:
        return 0
    
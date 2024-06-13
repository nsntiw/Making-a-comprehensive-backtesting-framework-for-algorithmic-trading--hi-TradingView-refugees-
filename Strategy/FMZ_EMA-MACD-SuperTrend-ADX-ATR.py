#https://medium.com/@FMZQuant/ema-macd-supertrend-adx-atr-multi-indicator-trading-signal-strategy-9a6569b1f04d
import numpy as np
import pandas as pd

def MACD_long(data):
    #MACD parameters
    short_ma_length = 5
    long_ma_length = 12
    #calculate short and long simple moving averages
    short_ma = data['Close'][-short_ma_length:].mean()
    long_ma = data['Close'][-long_ma_length:].mean()
    
    if short_ma > long_ma:
        return 1
    else:
        return -1

def MACD_short(data):
    #MACD parameters
    short_ma_length = 5
    long_ma_length = 12
    #calculate short and long simple moving averages
    short_ma = data['Close'][-short_ma_length:].mean()
    long_ma = data['Close'][-long_ma_length:].mean()

    if short_ma < long_ma:
        return 1
    else:
        return -1
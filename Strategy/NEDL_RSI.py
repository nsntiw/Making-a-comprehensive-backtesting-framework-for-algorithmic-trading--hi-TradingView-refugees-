#https://youtu.be/dfT6rnkJCms?si=eHZWQoDF46QAwftp
import numpy as np
import pandas as pd
from Strategy.Library import RSI

def RSI_long(data_feed):
    #RSI parameters
    rsi_period = 14
    rsi_oversold = 30
    rsi_overbought = 70

    #calculate RSI
    rsi = RSI(data_feed, rsi_period)

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
    rsi = RSI(data_feed, rsi_period)

    #return signal
    if rsi > rsi_overbought:
        return 1
    if rsi < rsi_oversold:
        return -1
    else:
        return 0
    
import numpy as np
import pandas as pd

def SMA(data_feed, length): #works
    if len(data_feed) < length:
        return np.nan
    SMA = data_feed.tail(length).mean()
    return SMA

def EMA(data_feed, length): #works
    EMA = data_feed.tail(length).ewm(span=length, adjust=False, min_periods = length).mean().iloc[-1]
    return EMA

def high(data_feed, length):
    high = max(data_feed.tail(length))
    return high

def low(data_feed, length):
    low = min(data_feed.tail(length))
    return low

def RSI(data_feed, rsi_period):
    #Get latest 15 values for RSI instead of the whole array
    close_prices = data_feed['Close'].tail(rsi_period + 1)
    up = np.maximum(close_prices.diff(), 0)
    down = np.maximum(-close_prices.diff(), 0)
    rs = up[-rsi_period:].mean() / down[-rsi_period:].mean()
    rsi = 100 - 100/(1 + rs)
    return rsi

def MACD(data_feed, short_ma_length, long_ma_length, signal_length): 
    close_prices = data_feed.tail(long_ma_length + signal_length)#works
    #Calculate short and long simple moving averages
    short_ema = close_prices.ewm(span=short_ma_length, adjust=False, min_periods = short_ma_length).mean()
    long_ema = close_prices.ewm(span=long_ma_length, adjust=False, min_periods = long_ma_length).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_length, adjust=False, min_periods = signal_length).mean()
    return(macd_line.iloc[-1], signal_line.iloc[-1]) 

def wwma(values, length):
    """
     J. Welles Wilder's EMA 
    """
    return values.ewm(alpha=1/length, min_periods=length, adjust=False).mean()

def ATR(data_feed, length):
    data = data_feed.copy()
    high = data_feed['High']
    low = data_feed['Low']
    close = data_feed['Close']
    data['tr0'] = abs(high - low)
    data['tr1'] = abs(high - close.shift())
    data['tr2'] = abs(low - close.shift())
    tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = wwma(tr, length)
    return atr

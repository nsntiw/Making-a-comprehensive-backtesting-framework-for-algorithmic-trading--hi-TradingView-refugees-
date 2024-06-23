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

def VWAP(data_feed, length):
    if len(data_feed) < length:
        return np.nan
    data = data_feed.tail(length)
    price = (data['High'] + data['Low'] + data['Close']) / 3
    volume = data['Volume']
    VWAP = sum(price * volume) / volume
    return VWAP.iloc[-1]

def high(data_feed, length):
    if len(data_feed) < length:
        return np.nan
    high = max(data_feed.tail(length))
    return high

def low(data_feed, length):
    if len(data_feed) < length:
        return np.nan
    low = min(data_feed.tail(length))
    return low

def RSI(data_feed, rsi_period):
    # Ensure we have at least rsi_period + 1 data points
    if len(data_feed) <= rsi_period:
        return np.nan
    # Select the last rsi_period + 1 close prices
    close_prices = data_feed.tail(rsi_period + 1).values
    # Calculate price changes
    price_diff = np.diff(close_prices)
    # Calculate gains (up) and losses (down)
    up = np.maximum(price_diff, 0)
    down = np.maximum(-price_diff, 0)
    # Calculate RS (Relative Strength)
    avg_gain = up.mean()
    avg_loss = down.mean()
    if avg_loss == 0:
        return 100  # Handle the case when avg_loss is zero to avoid division by zero
    rs = avg_gain / avg_loss
    # Calculate RSI
    rsi = 100 - 100 / (1 + rs)
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
    tr0 = abs(data_feed['High'] - data_feed['Low']).rolling(window=length).max()
    tr1 = abs(data_feed['High'] - data_feed['Close'].shift()).rolling(window=length).max()
    tr2 = abs(data_feed['Low'] - data_feed['Close'].shift()).rolling(window=length).max()
    
    # Calculate true range using trailing windows
    tr = pd.concat([tr0, tr1, tr2], axis=1).max(axis=1)
    
    # Calculate ATR
    atr = wwma(tr, length)
    
    return atr.iloc[-1]


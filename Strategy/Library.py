import numpy as np
import pandas as pd
import math

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
    if len(data_feed) < long_ma_length:
        return np.nan, np.nan
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

def ADX(data_feed, length):
    if len(data_feed) < length + 1:
        return np.nan

    # Convert columns to numpy arrays for efficiency
    high = data_feed['High'].values
    low = data_feed['Low'].values
    close = data_feed['Close'].values

    # Calculate True Range (TR)
    tr1 = high - low
    tr2 = np.abs(high - np.roll(close, 1))
    tr3 = np.abs(low - np.roll(close, 1))
    TR = np.maximum(tr1, np.maximum(tr2, tr3))
    TR[0] = np.nan  # The first TR value will be invalid due to np.roll

    # Calculate Directional Movement (DM)
    up_move = high - np.roll(high, 1)
    down_move = np.roll(low, 1) - low

    DM_plus = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    DM_minus = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
    DM_plus[0] = DM_minus[0] = np.nan  # The first DM values will be invalid due to np.roll

    # Calculate Smoothed True Range (ATR)
    ATR = pd.Series(TR).rolling(window=length).mean().values

    # Calculate Smoothed +DI and -DI
    DI_plus = 100 * (pd.Series(DM_plus).rolling(window=length).mean().values / ATR)
    DI_minus = 100 * (pd.Series(DM_minus).rolling(window=length).mean().values / ATR)

    # Calculate DX (Directional Movement Index)
    DX = 100 * (np.abs(DI_plus - DI_minus) / (DI_plus + DI_minus))

    # Calculate ADX (Average Directional Index)
    ADX = pd.Series(DX).rolling(window=length).mean().values

    # Return the latest ADX value
    current_adx = ADX[-1]
    return current_adx

def find_pivot_low(data_feed, left_lookback, right_lookback, num_pivots):
    pivot_indexes = []
    
    for i in range(-right_lookback - 2 , -len(data_feed) - 1, -1):
        if data_feed.iloc[i] == min(data_feed.iloc[i - left_lookback : i + right_lookback + 1]):
            pivot_indexes.append(i)
        if len(pivot_indexes) == num_pivots: #temp for this strategy, remove later
            return pivot_indexes
    return pivot_indexes

def find_pivot_high(data_feed, left_lookback, right_lookback, num_pivots):
    pivot_indexes = []
    
    for i in range(-right_lookback - 2, -len(data_feed) - 1, -1):
        if data_feed.iloc[i] == max(data_feed.iloc[i - left_lookback : i + right_lookback + 1]):
            pivot_indexes.append(i)
        if len(pivot_indexes) == num_pivots:
            return pivot_indexes
    return pivot_indexes

def inverse_fisher_transform(data_feed, length_WMA):
    def wma(series, length):
        weights = np.arange(1, length + 1)
        return series.rolling(window=length).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)

    v1 = 0.1 * (data_feed.tail(length_WMA) - 50)
    v2 = wma(v1, length_WMA)
    INV = (np.exp(2 * v2) - 1) / (np.exp(2 * v2) + 1) 
    return INV

def TTP_volatility_filter(data_feed):
    def calculate_hp(price, alpha1):
        """Calculate the High Pass filter."""
        hp = pd.Series(np.zeros(len(price)), index=price.index)
        for i in range(1, len(price)):
            hp.iloc[i] = 0.5 * (1 + alpha1) * (price.iloc[i] - price.iloc[i - 1]) + alpha1 * hp.iloc[i - 1]
        return hp

    def ss_filter(price, lower_band):
        """Apply the Super Smoother Filter."""
        angle2 = np.sqrt(2) * 3.141 / lower_band
        a1 = np.exp(-angle2)
        b1 = 2 * a1 * np.cos(angle2)
        c2 = b1
        c3 = -a1 * a1
        c1 = 1 - c2 - c3
        filt = pd.Series(np.zeros(len(price)), index=price.index)
        for i in range(2, len(price)):
            filt.iloc[i] = c1 * (price.iloc[i] + price.iloc[i - 1]) / 2 + c2 * filt.iloc[i - 1] + c3 * filt.iloc[i - 2]
        return filt

    def percent_rank(series, window):
        """Calculate the percent rank over a rolling window."""
        return series.rolling(window).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1])*100
    
    #wave_duration = 50
    lower_band = 19
    #Pi = 3.141
    #angle = 2.0 * Pi / wave_duration
    #alpha1 = (1 - math.sin(angle)) / math.cos(angle)
    alpha1 = 0.639
    hp = calculate_hp(data_feed.tail(100), alpha1)
    # Apply the Super Smoother Filter
    filt = ss_filter(hp, lower_band)
    # Calculate the percent rank over the rolling window
    return percent_rank(filt, 100)
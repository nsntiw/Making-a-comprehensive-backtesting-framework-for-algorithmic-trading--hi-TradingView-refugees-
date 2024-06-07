#https://medium.com/@FMZQuant/ema-macd-supertrend-adx-atr-multi-indicator-trading-signal-strategy-9a6569b1f04d
import numpy as np
import pandas as pd

def MACD(stock_data):
    #MACD parameters
    fast_ma_length = 5
    slow_ma_length = 12
    signal_length = 9

    #calculate short and exponential long moving averages
    fast_ema = stock_data['Close'].ewm(span=fast_ma_length, adjust=False, min_periods = fast_ma_length).mean()
    slow_ema = stock_data['Close'].ewm(span=slow_ma_length, adjust=False, min_periods = slow_ma_length).mean()

    #calculate MACD and signal line
    macd = fast_ema - slow_ema
    signal = macd.ewm(span=signal_length, adjust=False, min_periods = signal_length).mean()

    print(macd)
    print(signal)
    #generate strategy signal
    #1 if long, -1 if short
    signal_bigger_than_macd = np.where(np.isnan(signal), 0, np.where(signal > macd, 1, -1))

    # 1 if long, -1 if short, 0 when it does not change
    MACD_signal = np.where(np.diff(signal_bigger_than_macd, prepend=0) != 0, signal_bigger_than_macd, 0)
    # Convert MACD_signal to a DataFrame with dates as indexes
    MACD_signal_df = pd.DataFrame(MACD_signal, index=stock_data.index, columns=['Signal'])

    print(MACD_signal_df)
    return(MACD_signal_df)
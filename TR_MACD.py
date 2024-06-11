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
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal_length, adjust=False, min_periods = signal_length).mean()

    #generate raw strategy values
    #1 if macd > signal and signal < 0, 0 if signal is nan or when it does not change
    MACD_long_entry_raw = np.where((macd_line > signal_line) & (signal_line < 0), 1, 0)
    #-1 if macd < signal
    MACD_long_exit_raw  = np.where((macd_line < signal_line), -1, 0)
    MACD_long_raw = MACD_long_entry_raw + MACD_long_exit_raw
    #1 if macd < signal and signal > 0, 0 if signal is nan or when it does not change
    MACD_short_entry_raw = np.where((macd_line < signal_line) & (signal_line > 0), 1, 0)
    #-1 if macd > signal
    MACD_short_exit_raw = np.where((macd_line > signal_line), -1, 0)
    MACD_short_raw = MACD_short_entry_raw + MACD_short_exit_raw

    #convert to strategy signal
    MACD_long_signal = np.where(np.diff(MACD_long_raw, prepend=0) != 0, MACD_long_raw, 0)
    MACD_short_signal = np.where(np.diff(MACD_short_raw, prepend=0) != 0, MACD_short_raw, 0)

    # Convert signal to a DataFrame with dates as indexes
    MACD_long_signal_df = pd.DataFrame(MACD_long_signal, index=stock_data.index, columns=['Signal'])
    MACD_short_signal_df = pd.DataFrame(MACD_short_signal, index=stock_data.index, columns=['Signal'])

    print(MACD_long_signal_df)
    return(MACD_long_signal_df, MACD_short_signal_df)
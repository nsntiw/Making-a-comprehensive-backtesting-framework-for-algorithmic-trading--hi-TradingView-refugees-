#https://youtu.be/_9Bmxylp63Y?si=LsMSMCmxBuaVE3sd
import numpy as np
import pandas as pd
from Strategy.Library import ATR

def Breakout(stock_data):
    #Breakout parameters
    SMA_length = 200
    ATR_length = 20

    #calculate ATR stop loss size, seven day low, seven day high, 200 day sma
    close = stock_data['Close']

    moving_average_filter = stock_data['Close'].rolling(SMA_length).mean()
    stop_loss_long =  stock_data['Close'] - 2 * ATR(stock_data, ATR_length)
    stop_loss_short =  stock_data['Close'] + 2 * ATR(stock_data, ATR_length)
    seven_day_low = stock_data['Low'].rolling(window=7).min().shift(1)
    seven_day_high = stock_data['High'].rolling(window=7).max().shift(1)

    #generate raw strategy values
    Breakout_long_entry_raw = np.where((close < seven_day_low) & (close > moving_average_filter), 1, 0)
    stop_loss_long = stop_loss_long.where(Breakout_long_entry_raw == 1).ffill()
    Breakout_long_exit_raw = np.where((close > seven_day_high) | (close < stop_loss_long), -1, 0)
    Breakout_long_raw = Breakout_long_entry_raw + Breakout_long_exit_raw

    Breakout_short_entry_raw = np.where((close > seven_day_high), 1, 0)
    stop_loss_short = stop_loss_short.where(Breakout_short_entry_raw == 1).ffill()
    Breakout_short_exit_raw = np.where(((close < seven_day_low) & (close > moving_average_filter)) | (close > stop_loss_short), -1, 0)
    Breakout_short_raw = Breakout_short_entry_raw + Breakout_short_exit_raw

    # Convert signal to a DataFrame with dates as indexes
    Breakout_long_signal = np.where(np.diff(Breakout_long_raw, prepend=0) != 0, Breakout_long_raw, 0)
    Breakout_short_signal = np.where(np.diff(Breakout_short_raw, prepend=0) != 0, Breakout_long_raw, 0)

    # Convert signal to a DataFrame with dates as indexes
    Breahout_long_signal_df = pd.DataFrame(Breakout_long_signal, index=stock_data.index, columns=['Signal'])
    Breahout_short_signal_df = pd.DataFrame(Breakout_short_signal, index=stock_data.index, columns=['Signal'])
    

    return(Breahout_long_signal_df, Breahout_short_signal_df)
#https://www.youtube.com/watch?v=EAok0kAHnCU&list=PLE4a3phdCOauXaK3f1QMI_fEIqEYTsH9I
import numpy as np
import pandas as pd

def MACD(stock_data):
    #MACD parameters
    short_ma_length = 5
    long_ma_length = 12

    #calculate short and long simple moving averages
    short_ma = stock_data['Close'].rolling(short_ma_length).mean()
    long_ma = stock_data['Close'].rolling(long_ma_length).mean()

    #generate strategy signal
    #1 if short_ma > long_ma, -1 if short_ma < long_ma, 0 if long_ma is nan
    short_bigger_than_long = np.where(np.isnan(long_ma), 0, np.where(short_ma > long_ma, 1, -1))
    # 1 if long, -1 if short, 0 when it does not change
    MACD_signal = np.where(np.diff(short_bigger_than_long, prepend=0) != 0, short_bigger_than_long, 0)
    # Convert MACD_signal to a DataFrame with dates as indexes
    MACD_signal_df = pd.DataFrame(MACD_signal, index=stock_data.index, columns=['Signal'])

    return(MACD_signal_df)

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
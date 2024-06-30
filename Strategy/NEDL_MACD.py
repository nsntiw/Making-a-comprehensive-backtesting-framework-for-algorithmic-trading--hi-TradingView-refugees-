#https://www.youtube.com/watch?v=EAok0kAHnCU&list=PLE4a3phdCOauXaK3f1QMI_fEIqEYTsH9I
from Strategy.Library import SMA

def MACD_long(data_feed):
    #MACD parameters
    short_ma_length, long_ma_length = 5, 12

    #Calculate short and long simple moving averages
    short_ma = SMA(data_feed['Close'], short_ma_length)
    long_ma = SMA(data_feed['Close'], long_ma_length)

    #Return strategy signal
    return (1, 0, 0) if short_ma > long_ma else (-1, 0, 0)

def MACD_short(data_feed):
    #MACD parameters
    short_ma_length, long_ma_length = 5, 12

    #Calculate short and long simple moving averages
    short_ma = SMA(data_feed['Close'], short_ma_length)
    long_ma = SMA(data_feed['Close'], long_ma_length)

    #Return strategy signal
    return (1, 0, 0) if short_ma < long_ma else (-1, 0, 0)
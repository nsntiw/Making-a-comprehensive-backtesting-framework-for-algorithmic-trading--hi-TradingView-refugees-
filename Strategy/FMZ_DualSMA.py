#https://medium.com/@FMZQuant/dual-moving-average-pressure-rebound-strategy-fa1170f9d8a2
from Strategy.Library import RSI, SMA


def DualSMA_long(data_feed):
    #SMA parameters
    short_ma_length, long_ma_length = 10, 200
    SL_rate, TP_rate = 5, 20

    #Calculate short and long simple moving averages
    close = data_feed['Close'].iloc[-1]
    short_ma = SMA(data_feed['Close'], short_ma_length)
    long_ma = SMA(data_feed['Close'], long_ma_length)
    rsi = RSI(data_feed['Close'], 3)

    #Return strategy signal
    if close > long_ma and close < short_ma and rsi < 30:
        return 1, (1-0.01*SL_rate) * close, (1+0.01*TP_rate) * close
    if close>short_ma and close < data_feed['Low'].iloc[-2]:
        return -1, 0, 0
    return 0, 0, 0
    
def DualSMA_short(stock_data):
    #no short selling
    return 0, 0, 0
from Strategy.Library import MACD, EMA

def MACD_long(data_feed):
    #MACD parameters
    short_ma_length, long_ma_length, signal_length, EMA_length = 5, 25, 9, 200
    macd, signal = MACD(data_feed['Close'], short_ma_length, long_ma_length, signal_length)
    ema_filter = EMA(data_feed['Close'], EMA_length)

    #Return strategy signal
    if(macd > signal and signal < 0 and data_feed['Close'].iloc[-1] > ema_filter):
        return 1, 0, 0
    if(macd < signal):
        return -1, 0, 0
    return 0, 0, 0

def MACD_short(data_feed):
    #MACD parameters
    short_ma_length, long_ma_length, signal_length, EMA_length = 5, 25, 9, 200
    macd, signal = MACD(data_feed['Close'], short_ma_length, long_ma_length, signal_length)
    ema_filter = EMA(data_feed['Close'], EMA_length)
                     
    #Return strategy signal
    if(macd < signal and signal > 0 and data_feed['Close'].iloc[-1] < ema_filter):
        return 1, 0, 0
    if(macd > signal):
        return -1, 0, 0
    return 0, 0, 0  
import signal
from Strategy.Library import EMA, MACD

def EMA_MACD_SuperTrend_ADX_long(data_feed):
    #Strategy parameters
    EMA_long_length = 26
    EMA_short_length = 12
    MACD_long_length = 12
    MACD_short_length = 26
    MACD_signal_length = 9
    ADX
    ATR = 

    #Calculate
    EMA_long = EMA(data_feed['Close'], EMA_long_length)
    EMA_short = EMA(data_feed['Close'], EMA_short_length)
    MACD_line, signal_line = MACD(data_feed['Close'], MACD_short_length, MACD_long_length, MACD_signal_length)

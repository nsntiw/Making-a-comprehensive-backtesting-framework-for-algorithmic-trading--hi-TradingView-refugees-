#https://medium.com/@FMZQuant/larry-connors-rsi2-mean-reversion-strategy-861f5a3579e3
    #When it is greater than the moving average，rsi>90 open short position，rsi<10 close short position
    #When it is less than the moving average，rsi<10 open long position，rsi>90 close long position

from Strategy.Library import RSI, SMA
from ta.momentum import RSIIndicator

def calculate_rsi(close_prices, period):
    rsi_indicator = RSIIndicator(close=close_prices, window=period)
    return rsi_indicator.rsi()

def RSI_long(data_feed):
    #RSI parameters
    rsi_period = 2
    rsi_oversold = 5
    rsi_overbought = 95
    SMA_length = 70

    rsi = calculate_rsi(data_feed['Close'].tail(30), rsi_period)
    SMA_filter = SMA(data_feed['Close'], SMA_length)

    #Return strategy signal
    long_cond = rsi.iloc[-1] < rsi_oversold and data_feed['Close'].iloc[-1] < SMA_filter
    short_cond = rsi.iloc[-1] > rsi_overbought and data_feed['Close'].iloc[-1] > SMA_filter
    #long_cond = (rsi.iloc[-1] > rsi_oversold and rsi.iloc[-2] <= rsi_oversold) and data_feed['Close'].iloc[-1] < SMA_filter

    if long_cond:
        return 1, 0, 0
    if (rsi.iloc[-1] > rsi_overbought and data_feed['Close'].iloc[-1] < SMA_filter) or short_cond:
        return -1, 0, 0
    else:
        return 0, 0, 0

#for some reason it doesn't generate short trades when crossunder is applied
def RSI_short(data_feed):
    #RSI parameters
    rsi_period = 2
    rsi_oversold = 5
    rsi_overbought = 95
    SMA_length = 70

    #Calculate RSI
    rsi = calculate_rsi(data_feed['Close'].tail(30), rsi_period)
    SMA_filter = SMA(data_feed['Close'], SMA_length)

    #Return strategy signal
    long_cond = rsi.iloc[-1] < rsi_oversold and data_feed['Close'].iloc[-1] < SMA_filter
    short_cond = rsi.iloc[-1] > rsi_overbought and data_feed['Close'].iloc[-1] > SMA_filter
    #short_cond =  (rsi.iloc[-1] < rsi_overbought and rsi.iloc[-2] >= rsi_overbought) and data_feed['Close'].iloc[-1] > SMA_filter

    if short_cond:
        return 1, 0, 0
    if (rsi.iloc[-1] < rsi_oversold and data_feed['Close'].iloc[-1] > SMA_filter) or long_cond:
        return -1, 0, 0
    else:
        return 0, 0, 0
    
#https://medium.com/@FMZQuant/larry-connors-rsi2-mean-reversion-strategy-861f5a3579e3
    #When it is greater than the moving average，rsi>90 open short position，rsi<10 close short position
    #When it is less than the moving average，rsi<10 open long position，rsi>90 close long position

from Strategy.Library import RSI, SMA
from ta.momentum import RSIIndicator, stoch_signal

def calculate_stoch(data_feed, stoch_period, SMA_period):
    stoch_indicator = stoch_signal(high = data_feed['High'], low = data_feed['Low'], close = data_feed['Close'], window = stoch_period, smooth_window = SMA_period)
    return stoch_indicator

def calculate_rsi(close_prices, period):
    rsi_indicator = RSIIndicator(close=close_prices, window=period)
    return rsi_indicator.rsi()

def RSI_long(data_feed):
    #RSI parameter
    stoch_period = 70
    SMA_period = 3
    rsi_period = 2
    oversold = 30
    overbought = 80
    SMA_length = 70

    k = calculate_stoch(data_feed.tail(75), stoch_period, SMA_period)
    rsi = calculate_rsi(data_feed['Close'].tail(10), rsi_period)

    #Return strategy signal
    long_cond = k.iloc[-1] > 80 and rsi.iloc[-1] > 30 and rsi.iloc[-2] <= 30
    long_close_cond = k.iloc[-1] < 55 and k.iloc[-2] >= 55 and rsi.iloc[-1] < 80

    if long_cond:
        return 1, 0, 0
    if long_close_cond:
        return -1, 0, 0
    else:
        return 0, 0, 0

#for some reason it doesn't generate short trades when crossunder is applied
def RSI_short(data_feed):
    return 0, 0, 0
    
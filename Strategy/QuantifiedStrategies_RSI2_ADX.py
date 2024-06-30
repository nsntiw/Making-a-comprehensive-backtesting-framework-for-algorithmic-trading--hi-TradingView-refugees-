#https://www.pinterest.com/pin/895723813376697782/

from Strategy.Library import RSI, ADX

def RSI_long(data_feed):
    return 0, 0, 0

#for some reason it doesn't generate short trades when crossunder is applied
def RSI_short(data_feed):
    #RSI parameters
    rsi_period = 2
    rsi_overbought = 90
    ADX_period = 5

    #Calculate RSI
    rsi = RSI(data_feed['Close'], rsi_period)
    ADX_value = ADX(data_feed, ADX_period)

    #Return strategy signal
    #if (rsi < rsi_overbought and rsi > rsi_overbought) and data_feed['Close'].iloc[-1] < SMA_filter:
    if  rsi > rsi_overbought and ADX_value > 35 and data_feed['Close'].iloc[-1] > data_feed['Close'].iloc[-2] > data_feed['Close'].iloc[-3]:
        return 1, 0, 0
    return -1, 0, 0
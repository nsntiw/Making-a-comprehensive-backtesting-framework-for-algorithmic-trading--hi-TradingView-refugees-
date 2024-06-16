#https://youtu.be/_9Bmxylp63Y?si=LsMSMCmxBuaVE3sd
from Strategy.Library import SMA, ATR, high, low
import numpy as np

def Breakout_long(stock_data):
    #Breakout parameters
    SMA_length = 200
    ATR_length = 20
    
    #Calculate ATR stop loss size, seven day low, seven day high, 200 day sma
    close = stock_data['Close'].iloc[-1]
    sma_filter = SMA(stock_data['Close'], SMA_length)
    atr = ATR(stock_data, ATR_length)
    stop_loss =  close - 2 * atr
    #stop_loss_short =  close + 2 * atr
    seven_day_low = low(stock_data['Low'].shift(1), 7)
    seven_day_high = high(stock_data['High'].shift(1), 7)

    #Return strategy signal
    if close < seven_day_low and close > sma_filter:
        if np.isnan(stop_loss):
            return 1, 0, 0
        else:
            return 1, 0, stop_loss
    if close > seven_day_high:
        return -1, 0, 0
    return 0, 0, 0
    
def Breakout_short(stock_data):
    #no short selling
    return 0, 0, 0
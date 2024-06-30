from ta.momentum import RSIIndicator
from Strategy.Library import ATR, EMA
#GOOGL setting  5 , close, 3 , 1  profitLevel at 75 shows win rate  87.21 %  profit factor 7.059
#GOOGL setting  8 , close, 3 , 1  profitLevel at 80 shows win rate  86.57 %  profit factor 18.96 
#SPY setting    5, close , 3, 3  profitLevel at 70  , shows win rate 80.34%  profit factor 2.348

#

def calculate_rsi(close_prices, period):
    rsi_indicator = RSIIndicator(close=close_prices, window=period)
    return rsi_indicator.rsi()

def find_pivot_low(data_feed, left_lookback, right_lookback):
    pivot_indexes = []
    
    for i in range(-right_lookback - 2 , -len(data_feed) - 1, -1):
        if data_feed.iloc[i] == min(data_feed.iloc[i - left_lookback : i + right_lookback + 1]):
            pivot_indexes.append(i)
        if len(pivot_indexes) == 2: #temp for this strategy, remove later
            return pivot_indexes
    return pivot_indexes

def find_pivot_high(data_feed, left_lookback, right_lookback):
    pivot_indexes = []
    
    for i in range(-right_lookback - 2, -len(data_feed) - 1, -1):
        if data_feed.iloc[i] == max(data_feed.iloc[i - left_lookback : i + right_lookback + 1]):
            pivot_indexes.append(i)
        if len(pivot_indexes) == 2:
            return pivot_indexes
    return pivot_indexes

def RSI_Div_Long(data_feed):
    #Parameters
    rsi_length = 9
    pivot_lookback_r = 3
    pivot_lookback_l = 1
    rsi_TP = 80

    #maxLookback = 60
    minLookback = 0
    
    #Calculate RSI
    rsi = calculate_rsi(data_feed['Close'].tail(30), rsi_length)
    pivot_low = find_pivot_low(rsi, pivot_lookback_l, pivot_lookback_r)
    pivot_high = find_pivot_high(rsi, pivot_lookback_l, pivot_lookback_r)
    
    if len(pivot_low) < 2 or len(pivot_high) < 2:
        return 0, 0, 0
    #Regular bullish
    rsiHL = rsi.iloc[-pivot_lookback_r] > rsi.iloc[pivot_low[1]]
    priceLL = data_feed['Low'].iloc[-pivot_lookback_r] < data_feed['Low'].iloc[pivot_low[1]]
    bullCond = priceLL and rsiHL and pivot_low[0] == -pivot_lookback_r - 2
    #Hidden bullish
    rsiHL = rsi.iloc[-pivot_lookback_r] < rsi.iloc[pivot_low[1]]
    priceLL = data_feed['Low'].iloc[-pivot_lookback_r] > data_feed['Low'].iloc[pivot_low[1]]
    hiddenBullCond = rsiHL and priceLL and pivot_low[0] == -pivot_lookback_r - 2

    #Regular breaish
    rsiLH = rsi.iloc[-pivot_lookback_r] < rsi.iloc[pivot_high[1]]
    priceHH = data_feed['High'].iloc[-pivot_lookback_r] > data_feed['High'].iloc[pivot_high[1]]
    bearCond = rsiLH and priceHH and pivot_high[0] == -pivot_lookback_r - 2

    #Hidden bearish
    rsiHH = rsi.iloc[-pivot_lookback_r] > rsi.iloc[pivot_high[1]]
    priceLH = data_feed['High'].iloc[-pivot_lookback_r] < data_feed['High'].iloc[pivot_high[1]]
    hiddenBearCond = rsiHH and priceLH and pivot_high[0] == -pivot_lookback_r - 2


    #stop loss
    #SL = data_feed['Close'].iloc[-1] * ATR(data_feed, 14)
    # and data_feed['Close'].iloc[-1] > EMA(data_feed['Close'], 50)
    if (bullCond or hiddenBullCond):
        return 1, 0, 0
    if rsi.iloc[-1] > rsi_TP or bearCond:
        return -1, 0, 0
    return 0, 0, 0

def RSI_Div_Short(data_feed):
    #Parameters
    rsi_period = 9
    lbL = 1
    lbR = 3
    
    # Calculate RSI
    rsi = calculate_rsi(data_feed['Close'], period=rsi_period)
    pivot_low = find_pivot_low(rsi, left_lookback=lbL, right_lookback=lbR)
    pivot_high = find_pivot_high(rsi, left_lookback=lbL, right_lookback=lbR)
    
    if(len(data_feed) <= lbR or pivot_low == None or pivot_high == None):
        return 0, 0, 0
    #regular bullish
    rsiHL = rsi.iloc[-lbR] > rsi.iloc[pivot_low]
    priceLL = data_feed['Low'].iloc[-lbR] < data_feed['Low'].iloc[pivot_low]
    bullcon = priceLL and rsiHL
    #hidden bullish
    rsiHL = rsi.iloc[-lbR] < rsi.iloc[pivot_low]
    priceLL = data_feed['Low'].iloc[-lbR] > data_feed['Low'].iloc[pivot_low]
    hiddenBullCond = rsiHL and priceLL

    #regular bearish
    rsiLH = rsi.iloc[-lbR] < rsi.iloc[pivot_high]
    priceHH = data_feed['High'].iloc[-lbR] < data_feed['High'].iloc[pivot_high]
    bearcon = rsiLH and priceHH
    #hidden bearish
    rsiHH = rsi.iloc[-lbR] > rsi.iloc[pivot_high]
    priceLH = data_feed['High'].iloc[-lbR] < data_feed['High'].iloc[pivot_high]
    hiddenBearCond = rsiHH and priceLH

    #stop loss
    #SL = data_feed['Close'].iloc[-1] * ATR(data_feed, 14)

    if bearcon or hiddenBearCond:
        return 1, 0, 0
    if rsi.iloc[-1] < 60 or bullcon or hiddenBullCond:
        return -1, 0, 0
    return 0, 0, 0
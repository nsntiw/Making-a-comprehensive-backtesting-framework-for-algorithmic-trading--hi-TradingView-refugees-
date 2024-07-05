#https://youtu.be/wy_Nv8JSg6Y?si=AdkRoZYmFuAQ9_Lt
#https://www.tradingview.com/script/qSLcZSyw-RSI-Divergence-Indicator-strategy/
#GOOGL setting  5, close, 3 , 1  profitLevel at 75 shows win rate  87.21 %  profit factor 7.059
#GOOGL setting  8, close, 3 , 1  profitLevel at 80 shows win rate  86.57 %  profit factor 18.96 
#SPY setting    5, close , 3, 3  profitLevel at 70  , shows win rate 80.34%  profit factor 2.348

#implement trailing stop loss
from ta.momentum import RSIIndicator
from Strategy.Library import ATR, EMA, find_pivot_low, find_pivot_high

def calculate_rsi(close_prices, period):
    rsi_indicator = RSIIndicator(close=close_prices, window=period)
    return rsi_indicator.rsi()

def in_range(pivots, min_lookback, max_lookback):
    bars = pivots[0] - pivots[1]
    return bars >= 5 and bars <= 60

def RSI_div_long(data_feed):
    #Parameters
    rsi_length = 9
    pivot_lookback_r = 3
    pivot_lookback_l = 1
    rsi_TP = 80

    max_lookback = 60
    min_lookback = 5
    
    #Calculate RSI
    rsi = calculate_rsi(data_feed['Close'].tail(30), rsi_length)
    pivot_low = find_pivot_low(rsi, pivot_lookback_l, pivot_lookback_r, 2)
    pivot_high = find_pivot_high(rsi, pivot_lookback_l, pivot_lookback_r, 2)
    
    if len(pivot_low) < 2 or len(pivot_high) < 2:
        return 0, 0, 0
    #Regular bullish
    rsiHL = rsi.iloc[-pivot_lookback_r] > rsi.iloc[pivot_low[1]]
    priceLL = data_feed['Low'].iloc[-pivot_lookback_r] < data_feed['Low'].iloc[pivot_low[1]]
    bullCond = priceLL and rsiHL and pivot_low[0] == -pivot_lookback_r - 2 and in_range(pivot_low, min_lookback, max_lookback)
    #Hidden bullish
    rsiLL = rsi.iloc[-pivot_lookback_r] < rsi.iloc[pivot_low[1]]
    priceHL = data_feed['Low'].iloc[-pivot_lookback_r] > data_feed['Low'].iloc[pivot_low[1]]
    hiddenBullCond = priceHL and rsiLL and pivot_low[0] == -pivot_lookback_r - 2 and in_range(pivot_low, min_lookback, max_lookback)

    #Regular breaish
    rsiLH = rsi.iloc[-pivot_lookback_r] < rsi.iloc[pivot_high[1]]
    priceHH = data_feed['High'].iloc[-pivot_lookback_r] > data_feed['High'].iloc[pivot_high[1]]
    bearCond = rsiLH and priceHH and pivot_high[0] == -pivot_lookback_r - 2 and in_range(pivot_high, min_lookback, max_lookback)

    #Hidden bearish
    rsiHH = rsi.iloc[-pivot_lookback_r] > rsi.iloc[pivot_high[1]]
    priceLH = data_feed['High'].iloc[-pivot_lookback_r] < data_feed['High'].iloc[pivot_high[1]]
    hiddenBearCond = rsiHH and priceLH and pivot_high[0] == -pivot_lookback_r - 2 and in_range(pivot_high, min_lookback, max_lookback)


    #stop loss
    #SL = data_feed['Close'].iloc[-1] * ATR(data_feed, 14)
    # and data_feed['Close'].iloc[-1] > EMA(data_feed['Close'], 50)
    if (bullCond or hiddenBullCond):
        return 1, False, False
    if rsi.iloc[-1] > rsi_TP or bearCond:
        return -1, False, False
    return 0, False, False

def RSI_div_short(data_feed):
    return 0, 0, 0
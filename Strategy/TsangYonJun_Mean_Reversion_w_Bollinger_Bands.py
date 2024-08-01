from Strategy.Library import RSI, SMA

def MeanReversionLong(data_feed):
    #MeanReversion parameters
    length = 20
    multi = 2.5

    sma = SMA(data_feed['Close'], length)
    dev = multi * data_feed['Close'].tail(length).std()
    #print(data_feed['Close'].tail(length).std())
    upper = sma + dev
    lower = sma - dev
    rsi = RSI(data_feed['Close'], 14)

    #Return strategy signal
    if(data_feed['Close'].iloc[-1] < lower and rsi < 50):
        return 1, 0, 0
    if(data_feed['Close'].iloc[-1] > upper and rsi > 50):
        return -1, 0, 0
    return 0, 0, 0

def MeanReversionShort(data_feed):
    return 0, 0, 0
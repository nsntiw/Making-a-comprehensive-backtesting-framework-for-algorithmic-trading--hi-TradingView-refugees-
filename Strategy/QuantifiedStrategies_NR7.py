def NR7_long(data_feed):
    if len(data_feed) < 7:
        return 0, 0, 0
    range6 = [data_feed['High'].iloc[-i] - data_feed['Low'].iloc[-i] for i in range(1, 8)]
    if range6.index(min(range6)) == 0:
        return 1, 0, 0
    elif data_feed['Close'].iloc[-1] > data_feed['High'].iloc[-2]:
        return -1, 0, 0
    return 0, 0, 0

#for some reason it doesn't generate short trades when crossunder is applied
def NR7_short(data_feed):
    return 0, 0, 0
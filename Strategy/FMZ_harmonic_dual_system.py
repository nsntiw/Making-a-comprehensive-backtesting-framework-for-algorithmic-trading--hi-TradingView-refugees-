#https://medium.com/@FMZQuant/harmonic-dual-system-strategy-3b9b680c94f9

def calculate_harmonec_values(data_feed):
    def harm_average(x, y, z):
        return 3 / (1 / x + 1 / y + 1 / z)
    #Initialize arrays to store T1 to T6
    T1 = [harm_average(data_feed.iloc[-i], data_feed.iloc[-i-1], data_feed.iloc[-i-2]) for i in range(19, 0, -1)]
    T2 = [harm_average(T1[-i-2], T1[-i-1], T1[-i]) for i in range(12, 0, -1)]
    T3 = [harm_average(T2[-i-2], T2[-i-1], T2[-i]) for i in range(9, 0, -1)]
    T4 = [harm_average(T3[-i-2], T3[-i-1], T3[-i]) for i in range(6, 0, -1)]
    T5 = [harm_average(T4[-i-2], T4[-i-1], T4[-i]) for i in range(3, 0, -1)]
    T6 = [harm_average(T5[-3], T5[-2], T5[-1])]
    return T1, T2, T3, T4, T5, T6



def Harmonic_long(data_feed):
    if len(data_feed) < 21:
        return 0, 0, 0
    T1, T2, T3, T4, T5, T6 = calculate_harmonec_values(data_feed['Close'])
    T1_current = T1[0]
    T2_current = T2[0]
    T3_current = T3[0]
    T4_current = T4[0]
    T5_current = T5[0]
    T6_current = T6[0]

    # Determine buy and sell signals
    X1 = min(T1_current, T2_current, T3_current)
    X2 = max(T4_current, T5_current, T6_current)
    X3 = min(T1_current, T2_current)
    X4 = max(T3_current, T4_current)

    if X1 > X2:
        return 1, 0, 0
        
    if X3 < X4:
        return -1, 0, 0
    return 0, 0, 0

def Harmonic_short(data_feed):
    if len(data_feed) < 21:
        return 0, 0, 0
    T1, T2, T3, T4, T5, T6 = calculate_harmonec_values(data_feed['Close'])
    T1_current = T1[0]
    T2_current = T2[0]
    T3_current = T3[0]
    T4_current = T4[0]
    T5_current = T5[0]
    T6_current = T6[0]

    # Determine buy and sell signals
    X1 = min(T1_current, T2_current, T3_current)
    X2 = max(T4_current, T5_current, T6_current)
    X3 = min(T1_current, T2_current)
    X4 = max(T3_current, T4_current)

    if X3 < X4:
        return 1, 0, 0
    if X1 > X2:
        return -1, 0, 0
    return 0, 0, 0

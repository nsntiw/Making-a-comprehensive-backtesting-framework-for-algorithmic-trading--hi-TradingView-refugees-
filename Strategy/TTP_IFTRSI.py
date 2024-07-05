#IFT
#https://www.tradingview.com/v/LxiuxNm4/
#Strategy
#https://youtu.be/yv-6xM-qcNU?si=JpBeym1w2o_tO_TR
#https://www.tradingview.com/script/Nw4PDAwY-Inverse-Fisher-Transform-on-RSI-for-backtest-w-alerts/

from Strategy.Library import inverse_fisher_transform, TTP_volatility_filter, SMA
from ta.momentum import RSIIndicator
from ta.trend import CCIIndicator
from ta.volume import MFIIndicator
import pandas as pd

def calculate_rsi(close, period):
    rsi_indicator = RSIIndicator(close=close, window=period)
    return rsi_indicator.rsi()

def calculate_cci(high, low, close, period):
    cci_indicator = CCIIndicator(high=high, low=low, close=close, window=period)
    return cci_indicator.cci()

def calculate_mfi(high, low, close, volume, period):
    mfi_indicator = MFIIndicator(high=high, low=low, close=close, volume=volume, window=period)
    return mfi_indicator.money_flow_index()


def IFTRSI_long(data_feed):
    #RSI, CCI, MFI parameters
    rsi_period = 5
    cci_period = 5
    mfi_period = 5
    #Strategy settings
    enable_rsi = True
    enable_cci = True
    enable_mfi = True
    combination = 0 #Lowest, highest, average, median
    buy_on_reversal = False
    sell_on_reversal = False
    enable_volatility_filter = False
    min_volatility = 20
    max_volatility = 60
    oversold = -0.9
    overbought = 0.996
    
    #Calculate IFT of signals
    signals = []
    if enable_rsi:
        rsi = calculate_rsi(data_feed['Close'].tail(25), rsi_period)
        IFTRSI = inverse_fisher_transform(rsi, 9)
        signals.append(IFTRSI)
    if enable_cci:
        cci = calculate_cci(data_feed['High'].tail(25), data_feed['Low'].tail(25), data_feed['Close'].tail(25), cci_period)
        IFTCCI = inverse_fisher_transform(cci, 9)
        signals.append(IFTCCI)
    if enable_mfi:
        mfi = calculate_mfi(data_feed['High'].tail(25), data_feed['Low'].tail(25), data_feed['Close'].tail(25), data_feed['Volume'].tail(25), mfi_period)
        IFTMFI = inverse_fisher_transform(mfi, 9)
        signals.append(IFTMFI)

    #Combine signals
    if combination == 0:
        signal = pd.concat(signals, axis=1).min(axis=1)
    elif combination == 1:
        signal = pd.concat(signals, axis=1).max(axis=1)
    elif combination == 2:
        signal = pd.concat(signals, axis=1).mean(axis=1)
    elif combination == 3:
        signal = pd.concat(signals, axis=1).median(axis=1)

    #Return strategy signal
    buy_cond = signal.iloc[-1] > oversold and signal.iloc[-2] <= oversold if buy_on_reversal else signal.iloc[-1] < oversold
    if enable_volatility_filter:
        volatility_filter = TTP_volatility_filter(data_feed['Volume']).iloc[-1]
        buy_cond = buy_cond and max_volatility < volatility_filter > min_volatility

    sell_cond = signal.iloc[-1] < overbought and signal.iloc[-2] >= overbought if sell_on_reversal else signal.iloc[-1] > overbought

    if buy_cond:
        return 1, False, False
    if sell_cond:
        return -1, False, False
    else:
        return 0, False, False

def IFTRSI_short(data_feed):
    return 0, 0, 0
    
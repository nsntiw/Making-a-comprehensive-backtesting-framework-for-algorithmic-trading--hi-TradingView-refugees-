import numpy as np
import pandas as pd

def SMA(data_feed, length):
    return data_feed[-length:].mean()

def MACD(data_feed, lenght):
    return 1
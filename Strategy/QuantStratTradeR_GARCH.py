import pandas as pd
from arch import arch_model
from Strategy.Library import MACD

def calculate_garch_volatility(close_prices):
    if len(close_prices) < 100:
        return pd.DataFrame(columns=['cond_vol'])
    
    # Create an ARCH model
    model = arch_model(close_prices[-100:], vol='GARCH', p=1, q=1)

    # Fit the model
    if len(close_prices) % 100 == 0:
        res = model.fit(update_freq = 0, disp = 'off')

    # Return the forecasted volatility for the last observation
    forecasted_volatility = res.conditional_volatility
    return pd.DataFrame(forecasted_volatility)

def GARCH_long(data_feed):
    short_ma_length, long_ma_length, signal_length = 5, 25, 9

    #Calculate GARCH volatility
    garch_prediction = calculate_garch_volatility(100 * data_feed['Close'].pct_change().dropna())

    macd, signal = MACD(garch_prediction['cond_vol'], short_ma_length, long_ma_length, signal_length)
    macd1, signal1 = MACD(data_feed['Close'], short_ma_length, long_ma_length, signal_length)

    #Generate signals
    if signal > macd and signal1 < macd1:
        return 1, 0, 0  # Buy signal
    elif  signal < macd:
        return -1, 0, 0  # Sell signal
    else:
        return 0, 0, 0  # No signal

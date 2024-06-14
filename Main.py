#importing packages
import numpy as np
import pandas as pd
pd.options.display.float_format = "{:,.2f}".format

#--------------------------------------
#Download or read downloaded stock data csv files
#NEDL_MACD
#stock_name = 'XOM'
#starting_date = '2016-01-01'
#ending_date = '2021-03-18'
#NEDL_RSI
stock_name = 'KO'
starting_date = '2016-01-01'
ending_date = '2021-03-21'
#TR_MACD
#stock_name = 'EURJPY=X'
#starting_date = '2002-07-01'
#ending_date = '2024-02-05'
#CriticalTrading_Breakout
#stock_name = 'SPY'
#starting_date = '2007-12-30'
#ending_date = '2021-03-18'
import IO_handler
stock_data = IO_handler.get_stock_data(stock_name, starting_date, ending_date)
#--------------------------------------
#specifying backtesting parameters
fee = 0.0005 #implement
enable_long = True
enable_short = True
pyramiding_num_trades = 0

#--------------------------------------
#Calculate stock percentage and log returns
stock_data['% Return'] = stock_data['Close'].pct_change()
#Log returns overestimates negative returns and underestimates positive returns
stock_data['Log Return'] = np.log(stock_data['Close'] / stock_data['Close'].shift(1))
stock_data['Cumulative % Return'] = np.cumprod(1+stock_data['% Return'])

import Plotting_Printing
print(f'Stock Data for {stock_name}:'), Plotting_Printing.print_df(stock_data)
#--------------------------------------
#from Strategy.NEDL_MACD import MACD_long,MACD_short
#strategy_long, strategy_short = MACD_long, MACD_short
from Strategy.NEDL_RSI import RSI_long, RSI_short
strategy_long, strategy_short = RSI_long, RSI_short
#form Strategy.TR_MACD import MACD_long, MACD_short
#long_signal, short_signal = MACD(stock_data)
#from Strategy.CriticalTrading_Breakout import Breakout
#long_signal, short_signal = Breakout(stock_data)

#--------------------------------------
#Generate trades
import Backtesting
long_trades, short_trades, cumulative_return = Backtesting.generate_trades(stock_data, strategy_long, strategy_short, enable_long, enable_short)

#Print trades list
print("Long Trades:"), Plotting_Printing.print_df(long_trades)
print("Short Trades:"), Plotting_Printing.print_df(short_trades)
print("Cumulative:"), Plotting_Printing.print_df(cumulative_return)

#styler = long_trades.style.background_gradient()
#styler
#--------------------------------------
#Print TV states and plot equity curve (percentage)
import Plotting_Printing
Plotting_Printing.print_TV_stats(stock_data, cumulative_return[2:], long_trades[1:], short_trades[1:])
long_non_nan = long_trades.dropna(subset=['Cumulative Return'])
short_non_nan = short_trades.dropna(subset=['Cumulative Return'])
cumulative_non_nan = cumulative_return.dropna(subset=['Cumulative Return'])
Plotting_Printing.equity_curve(stock_data, cumulative_non_nan, long_non_nan, short_non_nan)

#--------------------------------------
#Plotting 1D histogram
data = cumulative_return['Return'].dropna()*100 
default_bin_size = int(len(cumulative_return['Return'])**0.5)

#Plotting_Printing.hist1d_base(data, default_bin_size)
Plotting_Printing.hist1d_stdev_mu(data, default_bin_size)
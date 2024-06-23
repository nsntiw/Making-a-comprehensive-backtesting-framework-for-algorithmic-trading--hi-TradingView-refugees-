#importing packages
import os
term_size = os.get_terminal_size()
import numpy as np
import pandas as pd

import Util.IO_handler as IO_handler
import Util.Plotting_Printing as Plotting_Printing
import Util.Backtesting as Backtesting
import Util.MonteCarlo as MonteCarlo

#--------------------------------------
#Download or read downloaded stock data csv files
stock_input = []
#NEDL_MACD
#stock_input.append({'name': 'XOM', 'starting_date': '2016-01-01', 'ending_date': '2021-03-18'})
#NEDL_RSI
#stock_input.append({'name': 'KO', 'starting_date': '2016-01-01', 'ending_date': '2021-03-21'})
#TR_MACD
#stock_input.append({'name': 'EURJPY=X', 'starting_date': '2002-07-01', 'ending_date': '2024-02-05'})
#CriticalTrading_Breakout, CriticalTrading_Seasonality, FMZ_Seasonality
stock_input.append({'name': 'SPY', 'starting_date': '2007-12-30', 'ending_date': '2021-03-18'})
#CriticalTrading_Seasonality
stock_input.append({'name': 'TLT', 'starting_date': '2007-12-30', 'ending_date': '2021-03-18'})

#stock_input.append({'name': 'BTC-USD', 'starting_date': '2018-12-30', 'ending_date': '2024-03-18'})

print('-' * term_size.columns)
stock_data = [IO_handler.get_stock_data(e['name'], e['starting_date'], e['ending_date']) for e in stock_input]

#import yfinance as yf
#stock_data = [yf.download('BTC-USD', period="1y", interval = '1h')]
#[1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
#stock_data = [yf.download('SPY', start = '2007-12-30', end = '2021-03-18', interval = '1d')]
#--------------------------------------
#specifying backtesting parameters
fee = 0.0005 #implement
enable_long, enable_short = True, False
pyramiding_num_trades = 0

#--------------------------------------
def calc_returns(stock_data):
    #Calculate stock percentage and log returns
    stock_data['% Return'] = stock_data['Close'].pct_change()
    #Log returns overestimates negative returns and underestimates positive returns
    stock_data['Log Return'] = np.log(stock_data['Close'] / stock_data['Close'].shift(1))
    stock_data['Total % Return'] = np.cumprod(1+stock_data['% Return'])
[calc_returns(e) for e in stock_data]

print('-' * term_size.columns)
for e1, e2 in zip(stock_input, stock_data):
    print(f'Stock Data for {e1['name']}:'), Plotting_Printing.print_df(e2)
#--------------------------------------
strategy_long, strategy_short = [], []
#from Strategy.NEDL_MACD import MACD_long, MACD_short
#strategy_long.append(MACD_long), strategy_short.append(MACD_short)
#from Strategy.NEDL_RSI import RSI_long, RSI_short
#strategy_long.append(RSI_long), strategy_short.append(RSI_short)
#from Strategy.TR_MACD_high_low import MACD_long, MACD_short
#strategy_long.append(MACD_long), strategy_short.append(MACD_short)
#from Strategy.CriticalTrading_Breakout import Breakout_long, Breakout_short
#strategy_long.append(Breakout_long), strategy_short.append(Breakout_short)
from Strategy.CriticalTrading_Seasonality import SPY_seasonality_long, SPY_seasonality_short, TLT_seasonality_long, TLT_seasonality_short
strategy_long.append(SPY_seasonality_long), strategy_short.append(SPY_seasonality_short)
strategy_long.append(TLT_seasonality_long), strategy_short.append(TLT_seasonality_short)
#from Strategy.Larry_Connors_RSI2 import RSI_long, RSI_short
#strategy_long.append(RSI_long), strategy_short.append(RSI_short)
#from Strategy.FMZ_DualSMA import DualSMA_long, DualSMA_long
#strategy_long.append(DualSMA_long), strategy_short.append(DualSMA_long)
#--------------------------------------
#Generate trades
print('-' * term_size.columns)
print(f'Backtesting on: {[e['name'] for e in stock_input]}')
print(f'Long: {enable_long}, Strategies: {[e.__name__ for e in strategy_long]}')
print(f'Short: {enable_short}, Strategies: {[e.__name__ for e in strategy_short]}')
long_trades, short_trades, total_return = Backtesting.generate_trades(stock_data, strategy_long, strategy_short, enable_long, enable_short)

#Print trades list
print('-' * term_size.columns)
print("Long Trades:"), Plotting_Printing.print_df(long_trades)
print("Short Trades:"), Plotting_Printing.print_df(short_trades)
print("Total:"), Plotting_Printing.print_df(total_return)

#styler = long_trades.style.background_gradient()
#styler

#--------------------------------------
#Print TV states and plot equity curve (percentage)
print('-' * term_size.columns)
Plotting_Printing.print_TV_stats(stock_data[0], total_return, long_trades, short_trades, enable_long, enable_short)
long_non_nan = long_trades.dropna(subset=['Total Return'])
short_non_nan = short_trades.dropna(subset=['Total Return'])
cumulative_non_nan = total_return.dropna(subset=['Total Return'])
Plotting_Printing.equity_curve(stock_data[0], cumulative_non_nan, long_non_nan, short_non_nan)

#--------------------------------------
#Plotting 1D histogram
data = total_return['Return'].dropna() * 100

#Plotting_Printing.hist1d_base(data)
Plotting_Printing.hist1d_stdev_mu(data, 2)

if enable_long and enable_short:
    long_non_nan['Length'] = (long_non_nan['Date2'] - long_non_nan['Date1']).dt.days
    short_non_nan['Length'] = (short_non_nan['Date2'] - short_non_nan['Date1']).dt.days
    data1 = pd.concat([long_non_nan[['Length']], short_non_nan[['Length']]])
if enable_long:
    long_non_nan['Length'] = (long_non_nan['Date2'] - long_non_nan['Date1']).dt.days
    data1 = long_non_nan['Length']
if enable_short:
    short_non_nan['Length'] = (short_non_nan['Date2'] - short_non_nan['Date1']).dt.days
    data1 = short_non_nan['Length']

#Plotting_Printing.hist2d_base(data, data1, 2)

#--------------------------------------
#Montecarlo simulation
montecarlo_results = MonteCarlo.montecarlo(cumulative_non_nan, 1000)
Plotting_Printing.montecarlo_equity_curve(montecarlo_results)

annualized_return = []
for e in montecarlo_results:
    equity_curve = np.cumprod(1 + e)
    annualized_return.append(equity_curve[-1])
    #implement annulalisation
Plotting_Printing.hist1d_stdev_mu(annualized_return, 2)
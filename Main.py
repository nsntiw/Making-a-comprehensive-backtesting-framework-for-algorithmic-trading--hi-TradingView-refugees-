#importing packages
import os
term_size = os.get_terminal_size() #To print linebreaks
import numpy as np
import pandas as pd

import Util.IO_handler as IO_handler
import Util.Plotting_Printing as Plotting_Printing
import Util.Backtesting as Backtesting
import Util.MonteCarlo as MonteCarlo

#--------------------------------------
#Download or read downloaded stock data csv files
stock_input = []
#Interval: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
stock_input.append({'name': 'SPY', 'starting_date': '2005-02-27', 'ending_date': '2024-06-24', 'interval': '1d'})
#stock_input.append({'name': 'EURJPY=X', 'starting_date': '2002-07-01', 'ending_date': '2024-02-05', 'interval': '1d'})

print('-' * term_size.columns)
stock_data = [IO_handler.get_stock_data(e['name'], e['starting_date'], e['ending_date'], e['interval']) for e in stock_input]

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
#from Strategy.QuantifiedStrategies_RSI2_ADX import RSI_short, RSI_short
#strategy_long.append(RSI_short), strategy_short.append(RSI_short)
#from Strategy.QuantifiedStrategies_NR7 import NR7_long, NR7_short
#strategy_long.append(NR7_long), strategy_short.append(NR7_short)

#from Strategy.QuantStratTradeR_GARCH import GARCH_long
#strategy_long.append(GARCH_long), strategy_short.append(GARCH_long)

from Strategy.TTP_RSI_Div import RSI_Div_Long, RSI_Div_Short
strategy_long.append(RSI_Div_Long), strategy_short.append(RSI_Div_Short)
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
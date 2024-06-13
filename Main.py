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
#Overestimates negative returns and underestimates positive returns
stock_data['Log Return'] = np.log(stock_data['Close'] / stock_data['Close'].shift(1))
stock_data['Cumulative % Return'] = np.cumprod(1+stock_data['% Return'])
print(f'Stock Data for {stock_name}:'), print(stock_data)
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
print("Long Trades:"), print(long_trades)
print("Short Trades:"), print(short_trades)
print("Cumulative:"), print(cumulative_return)

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
#Calculate and print annualized return, risk, sharpe ratio
#Calculate return and risk
annualized_BnH_return = stock_data['Cumulative % Return'].iloc[-1] **(252/len(stock_data)) - 1
annualized_algo_retrn = cumulative_return['Cumulative Return'].dropna().iloc[-1] **(252/len(stock_data)) - 1
annualized_BnH_risk = np.std(stock_data['% Return'])*(252)**(1/2)
annualized_algo_risk = np.std(cumulative_return['Return'])*(252)**(1/2)
#print annualized return and risk
print(f'BnH strategy return and risk: {round(annualized_BnH_return*100,2)}% and {round(annualized_BnH_risk*100,2)}%')
print(f'Algo strategy return and risk: {round(annualized_algo_retrn*100,2)}% and {round(annualized_algo_risk*100,2)}%') 
#calculate and plot annualized sharpe ratio
risk_free_rate = 0.0211
BnH_sharpe_ratio = (annualized_BnH_return - risk_free_rate) / annualized_BnH_risk
algo_sharpe_ratio = (annualized_algo_retrn - risk_free_rate) / annualized_algo_risk
algo_sharpe_ratio_VS_BnH = (annualized_algo_retrn - annualized_BnH_return) / annualized_algo_risk
print(f'BnH strategy Sharpe ratio vs riskfree: {round(BnH_sharpe_ratio, 2)}')
print(f'Algo strategy Sharpe ratio vs riskfree: {round(algo_sharpe_ratio, 2)}')
print(f'Algo strategy Sharpe ratio vs BnH: {round(algo_sharpe_ratio_VS_BnH, 2)}')

#--------------------------------------
#Plotting 1D histogram
data = cumulative_return['Return'].dropna()*100 
default_bin_size = int(len(cumulative_return['Return'])**0.5)

#Plotting_Printing.hist1d_base(data, default_bin_size)
Plotting_Printing.hist1d_stdev_mu(data, default_bin_size)
#importing packages
import numpy as np
import pandas as pd
import yfinance as yf
import math

#--------------------------------------
#define functions
def num_current_trades(df):
    return df['Exit Date'].isnull().sum()

def calc_returns(entry_price, exit_price):
    return (exit_price - entry_price) / entry_price

#--------------------------------------
#download stock data
import IO_handler

#stock_name = 'EURJPY=X'
#starting_date = '2002-07-01'
#ending_date = '2024-02-05'

stock_name = 'XOM'
starting_date = '2016-01-01'
ending_date = '2021-03-18'

#stock_name = 'SPY'
#starting_date = '2007-12-30'
#ending_date = '2021-03-18'

stock_data = IO_handler.get_stock_data(stock_name, starting_date, ending_date)
print(f'Stock Data for {stock_name}:'), print(stock_data)
#--------------------------------------
#specifying backtesting parameters
fee = 0.0005 #implement
enable_long = True
enable_short = True
pyramiding_num_trades = 0

#--------------------------------------
#stock percentage and log return array
stock_data['Return'] = stock_data['Close'].pct_change()
stock_data['Log Return'] = np.log(stock_data['Close'] / stock_data['Close'].shift(1))

#--------------------------------------
#from NEDL_MACD_Strategy import MACD
#strategy_signal = MACD(stock_data)
#from TR_MACD import MACD
#long_signal, short_signal = MACD(stock_data)

#from CriticalTrading_Breakout import Breakout
#long_signal, short_signal = Breakout(stock_data)

from NEDL_MACD_Strategy import MACD_long, MACD_short
strategy_long = MACD_long
strategy_short = MACD_short

#--------------------------------------
#generade trades
#add data for day 0 such that the curves start at 1
#'Entry Date', 'Exit Date' , 'Buying Price', 'Selling Price', 'Return'
initial_date = stock_data.index[0]
initial_price = stock_data['Close'].iloc[0]
long_trades = pd.DataFrame({'Entry Date': initial_date, 'Exit Date': initial_date, 
                            'Entry Price': initial_price, 'Exit Price': initial_price, 
                            'Return': 0}, index=[0])

short_trades = pd.DataFrame({'Entry Date': initial_date, 'Exit Date': initial_date, 
                             'Entry Price': initial_price, 'Exit Price': initial_price, 
                             'Return': 0}, index=[0])

for i in range(len(stock_data)):
    if enable_long:
        if(strategy_long(i, stock_data) == -1 and num_current_trades(long_trades) == 1):
            exit_index = long_trades[long_trades['Exit Date'].isnull()].index[0]
            long_trades.at[exit_index, 'Exit Date'] = stock_data.index[i]
            long_trades.at[exit_index, 'Exit Price'] = stock_data['Close'].iloc[i]
            long_trades.at[exit_index, 'Return'] = calc_returns(long_trades.at[exit_index, 'Entry Price'], long_trades.at[exit_index, 'Exit Price'])
        if(strategy_long(i, stock_data) == 1 and num_current_trades(long_trades) + num_current_trades(short_trades) == 0):
            new_row = pd.DataFrame({
                'Entry Date': [stock_data.index[i]], 
                'Entry Price': [stock_data['Close'].iloc[i]]
            })
            long_trades = pd.concat([long_trades, new_row], ignore_index=True)
    if enable_short:
        if(strategy_short(i, stock_data) == -1 and num_current_trades(short_trades) == 1):
            exit_index = short_trades[short_trades['Exit Date'].isnull()].index[0]
            short_trades.at[exit_index, 'Exit Date'] = stock_data.index[i]
            short_trades.at[exit_index, 'Exit Price'] = stock_data['Close'].iloc[i]
            short_trades.at[exit_index, 'Return'] = calc_returns(short_trades.at[exit_index, 'Entry Price'], short_trades.at[exit_index, 'Exit Price'])
        if(strategy_short(i, stock_data) == 1 and num_current_trades(short_trades) + num_current_trades(short_trades) == 0):
            new_row = pd.DataFrame({
                'Entry Date': [stock_data.index[i]], 
                'Entry Price': [stock_data['Close'].iloc[i]]
            })
            short_trades = pd.concat([short_trades, new_row], ignore_index=True)

#calculate cumulative returns
cumulative_return = pd.concat([long_trades[['Exit Date', 'Return']], short_trades[['Exit Date', 'Return']]])
cumulative_return = cumulative_return.rename(columns={'Exit Date': 'Date'})
cumulative_return.sort_values('Date', inplace=True)
# Print trades
print("Long Trades:"), print(long_trades)
print("Short Trades:"), print(short_trades)
print("Cumulative:"), print(cumulative_return)

#--------------------------------------
#visualizing equity curve (percentage)
import Plotting
Plotting.equity_curve(stock_data, cumulative_return, long_trades, short_trades)

#--------------------------------------
#print TV stats
print(f'Net Profit, Total Closed Trades, Percent Profitable, Profit Factor, Max Drawdown, Avg Trade, Avg # Bars in Trades')
print((long_trades['Return'] > 0).sum()/len(long_trades))
print((short_trades['Return'] > 0).sum()/len(short_trades))

#--------------------------------------
#calculate and print annualized return, risk, sharpe ratio
#calculate return and risk
annualized_BnH_return = np.prod(1+stock_data['Return'])**(252/len(stock_data)) - 1
annualized_algo_retrn = np.prod(1+cumulative_return['Return'])**(252/len(stock_data)) - 1
annualized_BnH_risk = np.std(stock_data['Return'])*(252)**(1/2)
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
#calculate and print annualized log return, risk, sharpe ratio
#overestimates negative returns and underestimates positive returns

#--------------------------------------
#Plotting 1D histogram
data = cumulative_return['Return']*100 
default_bin_size = int(len(cumulative_return['Return'])**0.5)

Plotting.hist1d_base(data, default_bin_size)
Plotting.hist1d_stdev_mu(data, default_bin_size)
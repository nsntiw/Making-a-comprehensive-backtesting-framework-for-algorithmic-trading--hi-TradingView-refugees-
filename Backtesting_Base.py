#importing packages
import numpy as np
import pandas as pd
pd.options.display.float_format = "{:,.2f}".format
import yfinance as yf
import math

#--------------------------------------
#define functions
def num_current_trades(trades):
    return trades['Exit Date'].isnull().sum()

def calc_returns(entry_price, exit_price, long):
    if long:
        return (exit_price - entry_price) / entry_price
    else:
        return (entry_price - exit_price) / entry_price

def calc_run_up(data_feed, trades, long):
    entry_date = trades['Entry Date'].iloc[-1]
    entry_price = trades['Entry Price'].iloc[-1]
    if long:
        #Equity_on_Entry - Min_Equity + Numbers_of_Contracts * (Current_High - Entry_Price)
        high = data_feed.loc[entry_date:, 'High'].values
        return max(high) - entry_price
    else:
        #Equity_on_Entry - Min_Equity + Numbers_of_Contracts * (Entry_Price - Current_Low)
        low = data_feed.loc[entry_date:, 'Low'].values
        return entry_price - min(low)

def calc_drawdown(data_feed, trades, long):
    entry_date = trades['Entry Date'].iloc[-1]
    entry_price = trades['Entry Price'].iloc[-1]
    if long:
        #Equity_on_Entry - Min_Equity + Numbers_of_Contracts * (Current_High - Entry_Price)
        low = data_feed.loc[entry_date:, 'Low'].values
        return entry_price - min(low)
    else:
        #Equity_on_Entry - Min_Equity + Numbers_of_Contracts * (Entry_Price - Current_Low)
        high = data_feed.loc[entry_date:, 'High'].values
        return max(high) - entry_price
#--------------------------------------
#Download or read downloaded stock data csv files
import IO_handler

#NEDL_MACD
stock_name = 'XOM'
starting_date = '2016-01-01'
ending_date = '2021-03-18'
#NEDL_RSI
#stock_name = 'KO'
#starting_date = '2016-01-01'
#ending_date = '2021-03-21'
#TR_MACD
#stock_name = 'EURJPY=X'
#starting_date = '2002-07-01'
#ending_date = '2024-02-05'
#CriticalTrading_Breakout
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
#Calculate stock percentage and log returns
stock_data['Return'] = stock_data['Close'].pct_change()
#Overestimates negative returns and underestimates positive returns
stock_data['Log Return'] = np.log(stock_data['Close'] / stock_data['Close'].shift(1))

#--------------------------------------
from Strategy.NEDL_MACD import MACD_long,MACD_short
strategy_long, strategy_short = MACD_long, MACD_short

#from Strategy.NEDL_RSI import RSI_long, RSI_short
#strategy_long = RSI_long
#strategy_short = RSI_short

#form Strategy.TR_MACD import MACD_long, MACD_short
#long_signal, short_signal = MACD(stock_data)

#from Strategy.CriticalTrading_Breakout import Breakout
#long_signal, short_signal = Breakout(stock_data)

#--------------------------------------
#Generade long and short trades
initial_date = stock_data.index[0]
initial_price = stock_data['Close'].iloc[0]
#Entry Date, Exit Date, Entry Price, Exit Price, Return, Cumulative Return, Run-up, Drawdown
#Add initial data for day 0 such that the equity curves start at 1
long_trades = pd.DataFrame({'Entry Date': initial_date, 'Exit Date': initial_date, 
                            'Entry Price': initial_price, 'Exit Price': initial_price, 
                            'Return': 0, 'Cumulative Return': 1, 'Run-up': 0, 'Drawdown': 0}, index=[0])

short_trades = pd.DataFrame({'Entry Date': initial_date, 'Exit Date': initial_date, 
                             'Entry Price': initial_price, 'Exit Price': initial_price, 
                             'Return': 0, 'Cumulative Return': 1, 'Run-up': 0, 'Drawdown': 0}, index=[0])

for i in range(1, len(stock_data) + 1):
    #Use data feed instead indexing stock data
    data_feed = stock_data.iloc[:i]
    if enable_long:
        #exit trade
        if(strategy_long(data_feed) == -1 and num_current_trades(long_trades) == 1):
            exit_index = long_trades[long_trades['Exit Date'].isnull()].index[0]
            long_trades.at[exit_index, 'Exit Date'] = data_feed.index[-1]
            long_trades.at[exit_index, 'Exit Price'] = data_feed['Close'].iloc[-1]
            long_trades.at[exit_index, 'Return'] = calc_returns(long_trades.at[exit_index, 'Entry Price'], long_trades.at[exit_index, 'Exit Price'], True)
            long_trades.at[exit_index, 'Cumulative Return'] = long_trades.at[exit_index-1, 'Cumulative Return'] * (1 + long_trades.at[exit_index, 'Return'])
            long_trades.at[exit_index, 'Run-up'] = calc_run_up(data_feed, long_trades, True)
            long_trades.at[exit_index, 'Drawdown'] = calc_drawdown(data_feed, long_trades, True)
        #enter trade
        if(strategy_long(data_feed) == 1 and num_current_trades(long_trades) + num_current_trades(short_trades) == 0):
            new_row = pd.DataFrame({
                'Entry Date': [data_feed.index[-1]], 
                'Entry Price': [data_feed['Close'].iloc[-1]]
            })
            long_trades = pd.concat([long_trades, new_row], ignore_index=True)
    if enable_short:
        #exit trade
        if(strategy_short(data_feed) == -1 and num_current_trades(short_trades) == 1):
            exit_index = short_trades[short_trades['Exit Date'].isnull()].index[0]
            short_trades.at[exit_index, 'Exit Date'] = data_feed.index[-1]
            short_trades.at[exit_index, 'Exit Price'] = data_feed['Close'].iloc[-1]
            short_trades.at[exit_index, 'Return'] = calc_returns(short_trades.at[exit_index, 'Entry Price'], short_trades.at[exit_index, 'Exit Price'], False)
            short_trades.at[exit_index, 'Cumulative Return'] = short_trades.at[exit_index-1, 'Cumulative Return'] + short_trades.at[exit_index, 'Return']
            short_trades.at[exit_index, 'Run-up'] = calc_run_up(data_feed, short_trades, False)
            short_trades.at[exit_index, 'Drawdown'] = calc_drawdown(data_feed, short_trades, False)
        #enter trade
        if(strategy_short(data_feed) == 1 and num_current_trades(short_trades) + num_current_trades(short_trades) == 0):
            new_row = pd.DataFrame({
                'Entry Date': [data_feed.index[-1]], 
                'Entry Price': [data_feed['Close'].iloc[-1]]
            })
            short_trades = pd.concat([short_trades, new_row], ignore_index=True)

#--------------------------------------
#Get cumulative returns by concatenating long_trades and short_trades
cumulative_return = pd.concat([long_trades[['Exit Date', 'Return']], short_trades[['Exit Date', 'Return']]])
cumulative_return = cumulative_return.rename(columns={'Exit Date': 'Date'})
cumulative_return.sort_values('Date', inplace=True)
#Make the index sequential
cumulative_return.reset_index(drop=True, inplace=True)
cumulative_return['Cumulative Return'] = np.cumprod(1+cumulative_return['Return'])

#Print trades list
print("Long Trades:"), print(long_trades)
print("Short Trades:"), print(short_trades)
print("Cumulative:"), print(cumulative_return)

#a = long_trades.style.background_gradient()
from IPython.display import display
#display(a)
#--------------------------------------
#Print TV states and plot equity curve (percentage)
import Plotting_Printing
long_non_nan = long_trades.dropna(subset=['Return'])
short_non_nan = short_trades.dropna(subset=['Return'])
cumulative_non_nan = cumulative_return.dropna(subset=['Return'])
Plotting_Printing.print_TV_stats(cumulative_non_nan)
Plotting_Printing.print_TV_stats1(stock_data, cumulative_non_nan, long_non_nan, short_non_nan)
Plotting_Printing.equity_curve(stock_data, cumulative_non_nan, long_non_nan, short_non_nan)


#--------------------------------------
#Calculate and print annualized return, risk, sharpe ratio
#Calculate return and risk
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
#Plotting 1D histogram
data = cumulative_return['Return'].dropna()*100 
default_bin_size = int(len(cumulative_return['Return'])**0.5)

#Plotting_Printing.hist1d_base(data, default_bin_size)
Plotting_Printing.hist1d_stdev_mu(data, default_bin_size)
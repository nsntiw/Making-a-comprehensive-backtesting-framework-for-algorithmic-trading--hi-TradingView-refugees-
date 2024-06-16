#importing packages
import numpy as np
import pandas as pd
from tqdm import tqdm

#--------------------------------------
#Define functions
def check_exit(close, signal, trades, is_long):
    if is_long:
        if trades['SL'].iloc[-1] == 0 and trades['TP'].iloc[-1] == 0:
            return signal == -1 and num_open_trades(trades) >= 1
        if trades['SL'].iloc[-1] == 0:
            return (signal == -1 or trades['TP'].iloc[-1] <= close) and num_open_trades(trades) >= 1
        if trades['TP'].iloc[-1] == 0:
            return (signal == -1 or trades['SL'].iloc[-1] >= close) and num_open_trades(trades) >= 1
        return (signal == -1 or trades['TP'].iloc[-1] <= close or trades['SL'].iloc[-1] >= close) and num_open_trades(trades) >= 1
    else:
        if trades['SL'].iloc[-1] == 0 and trades['TP'].iloc[-1] == 0:
            return signal == -1 and num_open_trades(trades) >= 1
        if trades['SL'].iloc[-1] == 0:
            return (signal == -1 or trades['TP'].iloc[-1] >= close) and num_open_trades(trades) >= 1
        if trades['TP'].iloc[-1] == 0:
            return (signal == -1 or trades['SL'].iloc[-1] <= close) and num_open_trades(trades) >= 1
        return (signal == -1 or trades['TP'].iloc[-1] >= close or trades['SL'].iloc[-1] <= close) and num_open_trades(trades) >= 1
    
def check_entry():
    pass
def num_open_trades(trades):
    count = 0
    #iterate in reverse, return when it hits a non null value
    for e in reversed(trades['Exit Date']):
        if pd.isnull(e):
            count += 1
        else:
            return count

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


def generate_trades(stock_data, strategy_long, strategy_short, enable_long, enable_short):
    initial_date = stock_data.index[0]
    initial_price = stock_data['Close'].iloc[0]
    #Entry Date, Exit Date, Entry Price, Exit Price, Return, Cumulative Return, Run-up, Drawdown
    #Add initial data for day 0 such that the equity curves start at 1
    long_trades = pd.DataFrame({'Entry Date': initial_date, 'Exit Date': initial_date, 
                                'Entry Price': initial_price, 'TP' : 0, 'SL': 0,
                                'Exit Price': initial_price, 'Return': 0, 'Total Return': 1,
                                'Run-up': 0, 'Drawdown': 0}, index=[0])
    short_trades = pd.DataFrame({'Entry Date': initial_date, 'Exit Date': initial_date, 
                                'Entry Price': initial_price, 'TP' : 0, 'SL': 0,
                                'Exit Price': initial_price, 'Return': 0, 'Total Return': 1,
                                'Run-up': 0, 'Drawdown': 0}, index=[0])
    temp_long = []
    temp_short = []

    for i in tqdm(range(1, len(stock_data) + 1)):
        #Use data feed instead indexing stock data
        data_feed = stock_data.iloc[:i]
        close = data_feed['Close'].iloc[-1]
        if enable_long:
            #exit trade
            signal, take_profit, stop_loss = strategy_long(data_feed)
            if(signal == 0):
                continue
            if check_exit(close, signal, long_trades, True):
                exit_index = long_trades[long_trades['Exit Date'].isnull()].index[0]
                long_trades.loc[exit_index, ['Exit Date', 'Exit Price', 'Return', 'Total Return', 'Run-up', 'Drawdown']] = [
                    data_feed.index[-1],
                    close,
                    calc_returns(long_trades.at[exit_index, 'Entry Price'], close, True),
                    long_trades.at[exit_index-1, 'Total Return'] * (1 + calc_returns(long_trades.at[exit_index, 'Entry Price'], close, True)),
                    calc_run_up(data_feed, long_trades, True),
                    calc_drawdown(data_feed, long_trades, True)
                ]
            #enter trade
            if(signal == 1 and num_open_trades(long_trades) + num_open_trades(short_trades) == 0):
                new_row = pd.DataFrame({
                    'Entry Date': data_feed.index[-1],
                    'Entry Price': close,
                    'TP': take_profit,
                    'SL': stop_loss
                }, index=[0])
                long_trades = pd.concat([long_trades, new_row], ignore_index=True)
        if enable_short:
            #exit trade
            signal, TP, SL = strategy_short(data_feed)
            if(signal == 0):
                continue
            if check_exit(close, signal, short_trades, False):
                exit_index = short_trades[short_trades['Exit Date'].isnull()].index[0]
                short_trades.loc[exit_index, ['Exit Date', 'Exit Price', 'Return', 'Total Return', 'Run-up', 'Drawdown']] = [
                    data_feed.index[-1],
                    data_feed['Close'].iloc[-1],
                    calc_returns(short_trades.at[exit_index, 'Entry Price'], close, False),
                    short_trades.at[exit_index-1, 'Total Return'] + calc_returns(short_trades.at[exit_index, 'Entry Price'], close, False),
                    calc_run_up(data_feed, short_trades, False),
                    calc_drawdown(data_feed, short_trades, False)
                ]
            #enter trade
            if(signal == 1 and num_open_trades(short_trades) + num_open_trades(short_trades) == 0):
                new_row = pd.DataFrame({
                    'Entry Date': [data_feed.index[-1]], 
                    'Entry Price': [close],
                    'TP': [TP], 'SL': [SL]
                }, index=[0])
                short_trades = pd.concat([short_trades, new_row], ignore_index=True)


    #--------------------------------------
    #Get cumulative returns by concatenating long_trades and short_trades
    cumulative_return = pd.concat([long_trades[['Exit Date', 'Return']], short_trades[['Exit Date', 'Return']]])
    cumulative_return = cumulative_return.rename(columns={'Exit Date': 'Date'})
    #Sort by date first
    cumulative_return.sort_values('Date', inplace=True)
    #Make the indexs sequential
    cumulative_return.reset_index(drop=True, inplace=True)
    cumulative_return['Total Return'] = np.cumprod(1+cumulative_return['Return'])
    
    return long_trades, short_trades, cumulative_return
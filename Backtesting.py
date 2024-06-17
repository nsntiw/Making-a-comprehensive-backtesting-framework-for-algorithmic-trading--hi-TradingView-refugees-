#importing packages
import numpy as np
import pandas as pd
import collections
from tqdm import tqdm

#--------------------------------------
#Define functions
def check_exit(close, signal, e, is_long):
    if is_long:
        if e['SL'] == 0 and e['TP'] == 0:
            return signal == -1
        if e['SL'] == 0:
            return (signal == -1 or e['TP'] <= close)
        if e['TP'] == 0:
            return (signal == -1 or e['SL'] >= close)
        return signal == -1 or e['TP'] <= close or e['SL'] >= close
    else:
        if e['SL'] == 0 and e['TP'] == 0:
            return signal == -1
        if e['SL'] == 0:
            return (signal == -1 or e['TP'] >= close)
        if e['TP'] == 0:
            return (signal == -1 or e['SL'] <= close)
        return (signal == -1 or e['TP'] >= close or e['SL'] <= close)

def exit_trades(date, close, signal, trades, open_trades, is_long):
    exited_trades = []
    for e in list(open_trades):
        if check_exit(close, signal, e, is_long):
            exited_trade = open_trades.popleft()
            returns = calc_returns(exited_trade['Entry Price'], close, is_long)
            exited_trades.append({
                'Entry Date': exited_trade['Entry Date'],
                'Entry Price': exited_trade['Entry Price'],
                'TP': exited_trade['TP'],
                'SL': exited_trade['SL'],
                'Exit Date': date,  # Use appropriate date here
                'Exit Price': close,
                'Return': returns,
                #'Run-up': calc_run_up(close, exited_trade, is_long),
                #'Drawdown': calc_drawdown(close, exited_trade, is_long)
            })
    return exited_trades

def check_entry(signal, open_long, open_short, is_long):
    if is_long:
        return signal == 1 and len(open_long) + len(open_short) == 0
    return signal == 1 and len(open_short) + len(open_long) == 0

def enter_trades(date, close, signal, take_profit, stop_loss, open_long, open_short, is_long):
    if is_long:
        if check_entry(signal, open_long, open_short, is_long):
            open_long.append({'Entry Date': date,
                                'Entry Price': close,
                                'TP': take_profit,
                                'SL': stop_loss})
    else:
        if check_entry(signal, open_long, open_short, is_long):
            open_short.append({'Entry Date': date,
                                'Entry Price': close,
                                'TP': take_profit,
                                'SL': stop_loss})

def calc_returns(entry_price, exit_price, is_long):
    if is_long:
        return (exit_price - entry_price) / entry_price
    return (entry_price - exit_price) / entry_price

def calc_run_up(data_feed, trades, is_long):
    entry_date = trades['Entry Date'].iloc[-1]
    entry_price = trades['Entry Price'].iloc[-1]
    if is_long:
        #Equity_on_Entry - Min_Equity + Numbers_of_Contracts * (Current_High - Entry_Price)
        high = data_feed.loc[entry_date:, 'High'].values
        return max(high) - entry_price
    else:
        #Equity_on_Entry - Min_Equity + Numbers_of_Contracts * (Entry_Price - Current_Low)
        low = data_feed.loc[entry_date:, 'Low'].values
        return entry_price - min(low)

def calc_drawdown(data_feed, trades, is_long):
    entry_date = trades['Entry Date'].iloc[-1]
    entry_price = trades['Entry Price'].iloc[-1]
    if is_long:
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
                                'Exit Price': initial_price, 'Return': 0,
                                'Run-up': 0, 'Drawdown': 0}, index=[0])
    short_trades = pd.DataFrame({'Entry Date': initial_date, 'Exit Date': initial_date, 
                                'Entry Price': initial_price, 'TP' : 0, 'SL': 0,
                                'Exit Price': initial_price, 'Return': 0,
                                'Run-up': 0, 'Drawdown': 0}, index=[0])
    open_long, open_short = [collections.deque() for _ in range(2)]

    for i in tqdm(range(1, len(stock_data) + 1)):
        #Use data feed instead indexing stock data
        data_feed = stock_data.iloc[:i]
        close = data_feed['Close'].iloc[-1]
        if enable_long:
            #no trade
            signal, take_profit, stop_loss = strategy_long(data_feed)
            if(signal == 0):
                continue
            #exit trade
            temp = pd.DataFrame.from_dict(exit_trades(data_feed.index[-1], close, signal, long_trades, open_long, True))
            long_trades = pd.concat([long_trades, temp], ignore_index=True)
            #enter trade
            enter_trades(data_feed.index[-1], close, signal, take_profit, stop_loss, open_long, open_short, True)
        if enable_short:
            #no trade
            signal, take_profit, stop_loss = strategy_short(data_feed)
            if(signal == 0):
                continue
            #exit trade
            temp = pd.DataFrame.from_dict(exit_trades(data_feed.index[-1], close, signal, short_trades, open_short, False))
            short_trades = pd.concat([short_trades, temp], ignore_index=True)
            #enter trade
            enter_trades(data_feed.index[-1], close, signal, take_profit, stop_loss, open_long, open_short, False)

    #--------------------------------------
    long_trades['Total Return'] = np.cumprod(1 + long_trades['Return'])
    short_trades['Total Return'] = np.cumprod(1 + short_trades['Return'])
    #Get cumulative returns by concatenating long_trades and short_trades
    cumulative_return = pd.concat([long_trades[['Exit Date', 'Return']], short_trades[['Exit Date', 'Return']]])
    cumulative_return = cumulative_return.rename(columns={'Exit Date': 'Date'})
    #Sort by date first
    cumulative_return.sort_values('Date', inplace=True)
    #Make the indexs sequential
    cumulative_return.reset_index(drop=True, inplace=True)
    cumulative_return['Total Return'] = np.cumprod(1 + cumulative_return['Return'])
    
    return long_trades, short_trades, cumulative_return
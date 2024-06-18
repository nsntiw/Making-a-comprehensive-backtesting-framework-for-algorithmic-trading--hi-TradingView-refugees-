#importing packages
import numpy as np
import pandas as pd
import collections
from tqdm import tqdm

#--------------------------------------
#Define functions
def check_exit(asset, close, signal, e, is_long):
    if asset != e['Asset']:
        return False
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
def exit_trades(asset, data_feed, close, signal, open_trades, is_long):
    exited_trades = []
    for e in list(open_trades):
        if check_exit(asset, close, signal, e, is_long):
            open_trades.remove(e)
            returns = calc_returns(e['P1'], close, is_long)
            exited_trades.append({
                'Asset': asset,
                'Date1': e['Date1'],
                'P1': e['P1'],
                'TP': e['TP'],
                'SL': e['SL'],
                'Date2': data_feed.index[-1],  # Use appropriate date here
                'P2': close,
                'Return': returns,
                'Run-up': calc_run_up(data_feed, e['Date1'], e['P1'], is_long),
                'Drawdown': calc_drawdown(data_feed, e['Date1'], e['P1'], is_long),
            })
    return exited_trades

def check_entry(signal, open_long, open_short, is_long):
    if is_long:
        return signal == 1 and len(open_long) + len(open_short) == 0
    return signal == 1 and len(open_short) + len(open_long) == 0

def enter_trades(asset, date, close, take_profit, stop_loss, open_long, open_short, is_long):
    if is_long:
        open_long.append({'Asset': asset,
                            'Date1': date,
                            'P1': close,
                            'TP': take_profit,
                            'SL': stop_loss})
    else:
        open_short.append({'Asset': asset,
                            'Date1': date,
                            'P1': close,
                            'TP': take_profit,
                            'SL': stop_loss})

def calc_returns(entry_price, exit_price, is_long):
    if is_long:
        return (exit_price - entry_price) / entry_price
    return (entry_price - exit_price) / entry_price

def calc_run_up(data_feed, entry_date, entry_price, is_long):
    #Equity_on_Entry - Min_Equity + Numbers_of_Contracts * (Current_High - Entry_Price)
    if is_long:
        high = data_feed.loc[entry_date:, 'High'].max()
        return (high - entry_price) / entry_price
    #Equity_on_Entry - Min_Equity + Numbers_of_Contracts * (Entry_Price - Current_Low)
    else:
        low = data_feed.loc[entry_date:, 'Low'].min()
        return (entry_price - low) / entry_price

def calc_drawdown(data_feed, entry_date, entry_price, is_long):
    #Equity_on_Entry - Min_Equity + Numbers_of_Contracts * (Current_High - Entry_Price)
    if is_long:
        low = data_feed.loc[entry_date:, 'Low'].min()
        return (entry_price - low) / entry_price
    #Equity_on_Entry - Min_Equity + Numbers_of_Contracts * (Entry_Price - Current_Low)
    else:
        high = data_feed.loc[entry_date:, 'High'].max()
        return (high - entry_price) / entry_price

def generate_trades(stock_data1, strategy_long1, strategy_short1, enable_long, enable_short):
    #Entry Date, Exit Date, Entry Price, Exit Price, Return, Cumulative Return, Run-up, Drawdown
    long_trades = pd.DataFrame(columns=['Asset', 'Date1', 'P1', 'TP', 'SL', 'Date2', 'P2', 'Return', 'Run-up', 'Drawdown'])
    short_trades = pd.DataFrame(columns=['Asset', 'Date1', 'P1', 'TP', 'SL', 'Date2', 'P2', 'Return', 'Run-up', 'Drawdown'])
    open_long, open_short = [collections.deque() for _ in range(2)]

    for i in tqdm(range(1, len(stock_data1[0]) + 1)):
        for asset, (stock_data, strategy_long, strategy_short) in enumerate(zip(stock_data1, strategy_long1, strategy_short1)):
            #Use data feed instead indexing stock data
            data_feed = stock_data.iloc[:i]
            close = data_feed['Close'].iloc[-1]
            if enable_long:
                signal, take_profit, stop_loss = strategy_long(data_feed)
                #no trade
                if(signal == 0):
                    continue
                #exit trade
                temp = pd.DataFrame.from_dict(exit_trades(asset, data_feed, close, signal, open_long, True))
                if not temp.empty:
                    long_trades = pd.concat([long_trades, temp], ignore_index=True)
                #enter trade
                if check_entry(signal, open_long, open_short, True):
                    enter_trades(asset, data_feed.index[-1], close, take_profit, stop_loss, open_long, open_short, True)
            if enable_short:
                signal, take_profit, stop_loss = strategy_short(data_feed)
                #no trade
                if(signal == 0):
                    continue
                #exit trade
                temp = pd.DataFrame.from_dict(exit_trades(asset, data_feed.index[-1], close, signal, open_short, False))
                if not temp.empty:
                    short_trades = pd.concat([short_trades, temp], ignore_index=True)
                #enter trade
                if check_entry(signal, open_long, open_short, False):
                    enter_trades(asset, data_feed.index[-1], close, take_profit, stop_loss, open_long, open_short, False)

    #--------------------------------------
    #Fill in open trades
    long_trades = pd.concat([long_trades, pd.DataFrame(open_long)], ignore_index=True)
    short_trades = pd.concat([short_trades, pd.DataFrame(open_short)], ignore_index=True)
    #Calculate total return
    long_trades['Total Return'] = np.cumprod(1 + long_trades['Return'])
    short_trades['Total Return'] = np.cumprod(1 + short_trades['Return'])
    #Get cumulative returns by concatenating long_trades and short_trades
    cumulative_return = pd.concat([long_trades[['Date2', 'Return']], short_trades[['Date2', 'Return']]])
    cumulative_return = cumulative_return.rename(columns={'Date2': 'Date'})
    #Sort by date first
    cumulative_return.sort_values('Date', inplace=True)
    #Make the indexs sequential
    cumulative_return.reset_index(drop=True, inplace=True)
    cumulative_return['Total Return'] = np.cumprod(1 + cumulative_return['Return'])
    
    return long_trades, short_trades, cumulative_return
#importing packages
import numpy as np
import pandas as pd
import yfinance as yf
import math
import plotting

#--------------------------------------
#download stock data
import IO_handler

stock_name = 'EURJPY=X'
starting_date = '2002-07-01'
ending_date = '2024-02-05'

#stock_name = 'XOM'
#starting_date = '2015-12-30'
#ending_date = '2021-03-18'

stock_data = IO_handler.get_stock_data(stock_name, starting_date, ending_date)
print(f'Stock Data for {stock_name}:'), print(stock_data)
#--------------------------------------
#specifying backtesting parameters
fee = 0.0005 #implement
enable_long = True
enable_short = True

#--------------------------------------
#stock percentage and log return array
stock_data['Return'] = stock_data['Close'].pct_change()
stock_data['Log Return'] = np.log(stock_data['Close'] / stock_data['Close'].shift(1))

#--------------------------------------
#from NEDL_MACD_Strategy import MACD
#strategy_signal = MACD(stock_data)

from TR_MACD import MACD
long_signal, short_signal = MACD(stock_data)

#--------------------------------------
#generade trades
long_trades = pd.DataFrame(columns=['Entry Date', 'Exit Date' , 'Entry Price', 'Exit Price', 'Return'])
short_trades = pd.DataFrame(columns=['Entry Date', 'Exit Date', 'Entry Price', 'Exit Price', 'Return'])

#add data for day 0 such that the curves start at 1
#'Entry Date', 'Exit Date' , 'Buying Price', 'Selling Price', 'Return'
long = [[stock_data.index[0]], [stock_data['Close'].iloc[0]], [stock_data['Close'].iloc[0]], [stock_data.index[0]]] 
short = [[stock_data.index[0]], [stock_data['Close'].iloc[0]], [stock_data['Close'].iloc[0]], [stock_data.index[0]]] 

# Handling long signals
if enable_long:
    for i in range(len(long_signal)):
        if long_signal['Signal'].iloc[i] == 1 and len(long[0]) == len(long[1]):
            long[0].append(long_signal.index[i])
            long[2].append(stock_data['Close'].iloc[i])
        elif long_signal['Signal'].iloc[i] == -1 and len(long[0]) > len(long[3]):
            long[3].append(long_signal.index[i])
            long[1].append(stock_data['Close'].iloc[i])
    for _ in range(len(long[0]) - len(long[3])):
        long[3].append(np.nan)
        long[1].append(np.nan)

# Handling short signals
if enable_short:
    for i in range(len(short_signal)):
        if short_signal['Signal'].iloc[i] == 1 and len(short[0]) == len(short[1]):
            short[0].append(short_signal.index[i])
            short[2].append(stock_data['Close'].iloc[i])
        elif short_signal['Signal'].iloc[i] == -1 and len(short[0]) > len(short[3]):
            short[3].append(short_signal.index[i])
            short[1].append(stock_data['Close'].iloc[i])
    for _ in range(len(short[0]) - len(short[3])):
        short[3].append(np.nan)
        short[1].append(np.nan)

#Add trade data to dataframe
long_trades = pd.DataFrame({
    'Entry Date': long[0], 'Entry Price': long[2], 'Exit Date': long[3], 'Exit Price': long[1],
    'Return': [(sp - bp) / sp for sp, bp in zip(long[1], long[2])]
})
short_trades = pd.DataFrame({
    'Entry Date': short[0], 'Entry Price': short[2], 'Exit Date': short[3], 'Exit Price': short[1],
    'Return': [(sp - bp) / sp for sp, bp in zip(short[2], short[1])]
})
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
plotting.equity_curve(stock_data, cumulative_return, long_trades, short_trades)

#--------------------------------------
#print TV stats
print(f'Net Profit, Total Closed Trades, Percent Profitable, Profit Factor, Max Drawdown, Avg Trade, Avg # Bars in Trades')
print((long_trades['Return'] > 0).sum()/len(long_trades))
print((short_trades['Return'] > 0).sum()/len(short_trades))

#--------------------------------------
#calculate and print annualized return, risk, sharpe ratio
#calculate return and risk
annualized_BnH_return = np.prod(1+stock_data['Return'])**(252/len(stock_data)) - 1
annualized_MACD_retrn = np.prod(1+cumulative_return['Return'])**(252/len(stock_data)) - 1
annualized_BnH_risk = np.std(stock_data['Return'])*(252)**(1/2)
annualized_MACD_risk = np.std(cumulative_return['Return'])*(252)**(1/2)
#print annualized return and risk
print(f'buy-and-hold strategy return and risk: {round(annualized_BnH_return*100,2)}% and {round(annualized_BnH_risk*100,2)}%')
print(f'MACD strategy return and risk: {round(annualized_MACD_retrn*100,2)}% and {round(annualized_MACD_risk*100,2)}%') 
#calculate and plot annualized sharpe ratio
risk_free_rate = 0.0211
BnH_sharpe_ratio = (annualized_BnH_return - risk_free_rate) / annualized_BnH_risk
MACD_sharpe_ratio = (annualized_MACD_retrn - risk_free_rate) / annualized_MACD_risk
MACD_sharpe_ratio_VS_BnH = (annualized_MACD_retrn - annualized_BnH_return) / annualized_MACD_risk
print(f'BnH strategy Sharpe ratio vs riskfree: {round(BnH_sharpe_ratio, 2)}')
print(f'MACD strategy Sharpe ratio vs riskfree: {round(MACD_sharpe_ratio, 2)}')
print(f'MACD strategy Sharpe ratio vs BnH: {round(MACD_sharpe_ratio_VS_BnH, 2)}')

#--------------------------------------
#calculate and print annualized log return, risk, sharpe ratio
#overestimates negative returns and underestimates positive returns

#--------------------------------------
#Plotting 1D histogram
data = cumulative_return['Return']*100 
default_bin_size = int(len(cumulative_return['Return'])**0.5)

plotting.hist1d_base(data, default_bin_size)
plotting.hist1d_stdev_mu(data, default_bin_size)
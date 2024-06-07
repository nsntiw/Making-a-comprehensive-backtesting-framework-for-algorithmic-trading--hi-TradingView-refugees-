#importing packages
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import math

#--------------------------------------
#download stock data
#stock = []
#stock_data = []

stock = 'EURJPY=X'
#stock.append('XOM')
stock_data = yf.download(stock, '2016-01-01', '2021-03-17')
print(f'Stock Data for {stock}:'), print(stock_data)

#--------------------------------------
#specifying backtesting parameters
fee = 0.0005 #implement

#--------------------------------------
#stock percentage and log return array
stock_data['Return'] = stock_data['Close'].pct_change()
stock_data['Log Return'] = np.log(stock_data['Close'] / stock_data['Close'].shift(1))

#--------------------------------------
from NEDL_MACD_Strategy import MACD
strategy_signal = MACD(stock_data)

#from TR_MACD import MACD
#strategy_signal = MACD(stock_data)

#--------------------------------------
#generade trades
long_trades = pd.DataFrame(columns=['Entry Date', 'Exit Date' , 'Buying Price', 'Selling Price', 'Return'])
short_trades = pd.DataFrame(columns=['Entry Date', 'Exit Date', 'Selling Price', 'Buying Price', 'Return'])
long = [[] for _ in range(4)] #'Entry Date', 'Exit Date' , 'Buying Price', 'Selling Price', 'Return'
short = [[] for _ in range(4)]#'Entry Date', 'Exit Date', 'Selling Price', 'Buying Price', 'Return'

#add data for day 0 such that the curves start at 1
long[0].append(stock_data.index[0])
long[1].append(stock_data['Close'].iloc[0])
long[2].append(stock_data['Close'].iloc[0])
long[3].append(stock_data.index[0])
short[0].append(stock_data.index[0])
short[1].append(stock_data['Close'].iloc[0])
short[2].append(stock_data['Close'].iloc[0])
short[3].append(stock_data.index[0])

for i in range(len(strategy_signal)):
    if strategy_signal['Signal'].iloc[i] == 1:
        long[0].append(stock_data.index[i])
        long[2].append(stock_data['Close'].iloc[i])
        if len(short[0]) > len(short[3]):
            short[3].append(stock_data.index[i])
            short[1].append(stock_data['Close'].iloc[i])
    elif strategy_signal['Signal'].iloc[i] == -1:
        short[0].append(stock_data.index[i])
        short[2].append(stock_data['Close'].iloc[i])
        if len(long[0]) > len(long[3]):
            long[3].append(stock_data.index[i])
            long[1].append(stock_data['Close'].iloc[i])
# Adding remaining sells if any buy is left unmatched for long and short trades
for _ in range(len(long[0]) - len(long[3])):
    long[3].append(np.nan)
    long[1].append(np.nan)
for _ in range(len(short[0]) - len(short[3])):
    short[3].append(np.nan)
    short[1].append(np.nan)

#Add trade data to dataframe
long_trades = pd.DataFrame({
    'Entry Date': long[0], 'Buying Price': long[2], 'Exit Date': long[3], 'Selling Price': long[1],
    'Return': [(sp - bp) / sp for sp, bp in zip(long[1], long[2])]
})
short_trades = pd.DataFrame({
    'Entry Date': short[0], 'Selling Price': short[2], 'Exit Date': short[3], 'Buying Price': short[1],
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
plt.plot(stock_data.index, np.cumprod(1+stock_data['Return']), label = 'Buy and Hold')
#Use step because plt.plot will draw a straight line between datapoints that exists
plt.step(cumulative_return['Date'], np.cumprod(1+cumulative_return['Return']), label = "Cumulative")
plt.step(long_trades['Exit Date'], np.cumprod(1+long_trades['Return']), label = 'Long')
plt.step(short_trades['Exit Date'], np.cumprod(1+short_trades['Return']), label = 'Short')

plt.title('Stock Price'), plt.xlabel('Time (Trading days)'), plt.ylabel('Price'), plt.legend()
plt.grid(True)
plt.show()

#--------------------------------------
#print TV stats
print(f'Net Profit, Total Closed Trades, Percent Profitable, Profit Factor, Max Drawdown, Avg Trade, Avg # Bars in Trades')
print((long_trades['Return'] > 0).sum()/len(long_trades))
print((short_trades['Return'] > 0).sum()/len(short_trades))

#--------------------------------------
#calculate and print annualized return, risk, sharpe ratio
#calculate return and risk
annualized_BnH_return = np.prod(1+stock_data['Return'])**(252/len(stock_data)) - 1
annualized_MACD_retrn = np.prod(1+cumulative_return['Return'])**(252/len(cumulative_return)) - 1
annualized_BnH_risk = np.std(stock_data['Return'])*(252)**(1/2)
annualized_MACD_risk = np.std(cumulative_return['Return'])*(252)**(1/2)
#print annualized return and risk
print(f'buy-and-hold strategy return and risk: {round(annualized_BnH_return*100,2)}+% and {round(annualized_BnH_risk*100,2)}+%')
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
#Plotting 1D histogram, base
default_bin_size = int(len(cumulative_return['Return'])**0.5)
data = cumulative_return['Return']*100
plt.hist(data, default_bin_size)
plt.xlabel('Values'), plt.ylabel('Frequency'), plt.title("Returns Histogram"), plt.grid(True)
plt.show()

#--------------------------------------
#plot heatmap histogram with SD and mean
#https://matplotlib.org/3.1.1/gallery/statistics/hist.html
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

fig, axs = plt.subplots(tight_layout=True)
# N is the count in each bin, bins is the lower-limit of the bin
N, bins, patches = axs.hist(data, bins=default_bin_size)
# We'll color code by height, but you could use any scalar
fracs = N / N.max()
# we need to normalize the data to 0..1 for the full range of the colormap
norm = colors.Normalize(fracs.min(), fracs.max())
# Now, we'll loop through our objects and set the color of each accordingly
for thisfrac, thispatch in zip(fracs, patches):
    color = plt.cm.viridis(norm(thisfrac))
    thispatch.set_facecolor(color)
# We can also normalize our inputs by the total number of counts
axs.hist(data, bins=default_bin_size, density=True)

#--------------------------------------
#standard deviation +1 -1 and mean
mean = np.mean(data)
stdev = np.std(data)
plt.axvline(x=mean+stdev, color='#2ca02c', alpha=0.7, label = f'{mean+stdev}')
plt.axvline(x=mean-stdev, color='#2ca02c', alpha=0.7, label = f'{mean-stdev}')
plt.axvline(x=mean, color='#d3212d', alpha=0.7, label = f'{mean}')

plt.xlabel('Values'), plt.ylabel('Frequency'), plt.title("Returns Histogram"), plt.legend(), plt.grid(True)
plt.show()
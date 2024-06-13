from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import pandas as pd
from scipy import stats

def print_TV_stats(Cumulative):
    table = []
    table.append(["Net Profit", "Total Closed Trades", "Percent Profitable", "Profit Factor", "Max Drawdown", "Avg Trade", "Avg # Bars in Trades"])

    net_profit = (np.cumprod(1+Cumulative['Return']).iloc[-1] - 1)*100
    total_closed_trades = len(Cumulative)
    percent_profitable = (Cumulative['Return'] > 0).sum()/total_closed_trades

    gross_profits = Cumulative[Cumulative['Return'] > 0]['Return'].sum()
    gross_losses = Cumulative[Cumulative['Return'] < 0]['Return'].sum()
    profit_factor = gross_profits / abs(gross_losses)
    max_drawdown = 0
    avg_trade = net_profit/total_closed_trades
    avg_num_bars_in_trades = 0


    table.append([f'{net_profit:.2f}%', total_closed_trades, f'{percent_profitable:.2f}%', f'{profit_factor:.2f}', max_drawdown, f'{avg_trade:.2f}%', avg_num_bars_in_trades])
    print(tabulate(table))

def print_TV_stats1(stock, cumulative, long, short):
    cum_net_profit = (np.cumprod(1+cumulative['Return']).iloc[-1] - 1) * 100
    long_net_profit = (np.cumprod(1+long['Return']).iloc[-1] - 1) * 100
    short_net_profit = (np.cumprod(1+short['Return']).iloc[-1] - 1) * 100
    cum_gross_profits = cumulative[cumulative['Return'] > 0]['Return'].sum() * 100
    long_gross_profits = long[long['Return'] > 0]['Return'].sum() * 100
    short_gross_profits = short[short['Return'] > 0]['Return'].sum() * 100
    cum_gross_losses = cumulative[cumulative['Return'] < 0]['Return'].sum() * 100
    long_gross_losses = long[long['Return'] < 0]['Return'].sum() * 100
    short_gross_losses = short[short['Return'] < 0]['Return'].sum() * 100
    #max run-up
    #max drawdown
    BnH_return = (np.cumprod(1+stock['Return']).iloc[-1] - 1)*100
    #sharpe ratio
    #sortino ratio
    cum_profit_factor = cum_gross_profits / abs(cum_gross_losses)
    long_profit_factor = long_gross_profits / abs(long_gross_losses)
    short_profit_factor = short_gross_profits / abs(short_gross_losses)
    #max contracts held
    open_pl = 0
    long_total_open_trades = 0
    short_total_open_trades = 0
    #refactor into loop
    if long['Exit Date'].iloc[-1] == pd.NaT:
        open_pl += (stock['Close'].iloc[-1] - long['Entry Price'].iloc[-1]) / long['Entry Price'].iloc[-1]
        long_total_open_trades += 1
    if short['Exit Date'].iloc[-1] == pd.NaT:
        open_pl += (short['Entry Price'].iloc[-1] - stock['Close'].iloc[-1]) / short['Entry Price'].iloc[-1]
        short_total_open_trades += 1
    #commission paid
    cum_total_closed_trades = len(cumulative)
    long_total_closed_trades = len(long)
    short_total_closed_trades = len(short)
    cum_total_open_trades =long_total_open_trades + short_total_open_trades
    table = []
    table.append(["Stats", "Cumulative", "Long", "Short"])
    table.append(["Net Profit",f'{cum_net_profit:.2f}%',f'{long_net_profit:.2f}%',f'{short_net_profit:.2f}%'])
    table.append(["Gross Profit",f'{cum_gross_profits:.2f}%',f'{long_gross_profits:.2f}%',f'{short_gross_profits:.2f}%'])
    table.append(["Gross Loss",f'{cum_gross_losses:.2f}%',f'{long_gross_losses:.2f}%',f'{short_gross_losses:.2f}%'])
    table.append(["Max Run-up"])
    table.append(["Max Drawdown"])
    table.append(["Buy & Hold Return", BnH_return])
    table.append(["Sharpe Ratio"])
    table.append(["Sortino Ratio"])
    table.append(["Profit Factor",cum_profit_factor,long_profit_factor,short_profit_factor])
    table.append(["Max Contracts Held"])
    table.append(["Open PL", open_pl])
    table.append(["Commission Paid"])
    table.append(["Total Closed Trades",cum_total_closed_trades,long_total_closed_trades,short_total_closed_trades])
    table.append(["Total Open Trades",cum_total_open_trades, long_total_open_trades, short_total_open_trades])
    table.append(["Number Winning Trades"])
    table.append(["Number Losing Trades"])
    table.append(["Percent Profitable"])
    table.append(["Avg Trade"])
    table.append(["Avg Winning Trade"])
    table.append(["Avg Losing Trade"])
    table.append(["Ratio Avg Win / Avg Loss"])
    table.append(["Largest Winning Trade"])
    table.append(["Largest Losing Trade"])
    table.append(["Avg # Bars in Trades"])
    table.append(["Avg # Bars in Winning Trades"])
    table.append(["Avg # Bars in Losing Trades"])
    table.append(["Margin Calls"])
    print(tabulate(table))

def equity_curve(stock_data, cumulative_return, long_trades, short_trades):
    #visualizing equity curve (percentage)
    plt.plot(stock_data.index, np.cumprod(1+stock_data['Return']), label = 'Buy and Hold')
    #Use step because plt.plot will draw a straight line between datapoints that exists
    plt.step(cumulative_return['Date'], cumulative_return['Cumulative Return'], label = "Cumulative")
    plt.step(long_trades['Exit Date'], long_trades['Cumulative Return'], label = 'Long')
    plt.step(short_trades['Exit Date'], short_trades['Cumulative Return'], label = 'Short')

    plt.title('Stock Price'), plt.xlabel('Time (Trading days)'), plt.ylabel('Price'), plt.legend()
    plt.grid(True)
    plt.show()

def hist1d_base(data, bin):
    plt.hist(data, bin)
    plt.xlabel('Values'), plt.ylabel('Frequency'), plt.title("Returns Histogram"), plt.grid(True)
    plt.show()

def hist1d_stdev_mu(data,bin):
    # N is the count in each bin, bins is the lower-limit of the bin
    N, bins, patches = plt.hist(data, bins=bin)
    # We'll color code by height, but you could use any scalar
    fracs = N / N.max()
    # we need to normalize the data to 0..1 for the full range of the colormap
    norm = colors.Normalize(fracs.min(), fracs.max())
    # Now, we'll loop through our objects and set the color of each accordingly
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    #--------------------------------------
    #standard deviation +1 -1 and mean
    mean = np.mean(data)
    stdev = np.std(data)
    plt.axvline(x=mean+stdev, color='#2ca02c', alpha=0.7, label = f'{mean+stdev}')
    plt.axvline(x=mean-stdev, color='#2ca02c', alpha=0.7, label = f'{mean-stdev}')
    plt.axvline(x=mean, color='#d3212d', alpha=0.7, label = f'{mean}')

    # Normal distribution curve
    bin_width = bins[1] - bins[0]
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    kde = stats.gaussian_kde(data) #* len(data) * bin_width
    p = kde(x)* len(data) * bin_width
    plt.plot(x, p, 'k', linewidth=2, label='Probability Density Function')


    plt.xlabel('Values'), plt.ylabel('Frequency'), plt.title("Returns Histogram"), plt.legend(), plt.grid(True)
    plt.show()
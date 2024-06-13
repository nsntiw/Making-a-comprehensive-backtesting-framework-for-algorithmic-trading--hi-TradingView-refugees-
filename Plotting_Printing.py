from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import pandas as pd
from scipy import stats

def print_TV_stats(stock, cumulative, long, short):
    C_NP = (cumulative['Cumulative Return'].dropna().iloc[-1] - 1) * 100
    L_NP = (long['Cumulative Return'].dropna().iloc[-1] - 1) * 100
    S_NP = (short['Cumulative Return'].dropna().iloc[-1] - 1) * 100
    C_GP = cumulative[cumulative['Return'] > 0]['Return'].sum() * 100
    L_GP = long[long['Return'] > 0]['Return'].sum() * 100
    S_GP = short[short['Return'] > 0]['Return'].sum() * 100
    C_GL = cumulative[cumulative['Return'] < 0]['Return'].sum() * 100
    L_GL = long[long['Return'] < 0]['Return'].sum() * 100
    S_GL = short[short['Return'] < 0]['Return'].sum() * 100
    #max run-up
    #max drawdown
    BnH_Return = (stock['Cumulative % Return'].iloc[-1] - 1) * 100

    #Additional stats
    #Annualized percentage return and risk
    A_BnH_Return = ((1 + BnH_Return / 100) ** (252 / len(stock)) - 1) * 100
    A_BnH_Risk = stock['% Return'].std() * (252)**(1/2) * 100
    A_C_Return = ((1 + C_NP / 100) ** (252 / len(stock)) - 1) * 100
    A_C_Risk = cumulative['Return'].dropna().std() * (252)**(1/2) * 100
    A_L_Return = ((1 + L_NP / 100) ** (252 / len(stock)) - 1) * 100
    A_L_Risk = long['Return'].dropna().std() * (252)**(1/2) * 100
    A_S_Return = ((1 + S_NP / 100) ** (252 / len(stock)) - 1) * 100
    A_S_Risk = short['Return'].dropna().std() * (252)**(1/2) * 100
    #Annualized Sharpe ratio
    risk_free_rate = 0.0211
    A_BnH_SR = (A_BnH_Return / 100 - risk_free_rate) / (A_BnH_Risk / 100)
    A_C_SR = (A_C_Return / 100 - risk_free_rate) / (A_C_Risk / 100)
    A_L_SR = (A_L_Return / 100 - risk_free_rate) / (A_L_Risk / 100)
    A_S_SR = (A_S_Return / 100 - risk_free_rate) / (A_S_Risk / 100)
    A_C_vs_BnH_SR = (A_C_Return / 100 - A_BnH_Return / 100) / A_C_Risk / 100

    #sortino ratio

    C_PF = C_GP / abs(C_GL)
    L_PF = L_GP / abs(L_GL)
    S_PF = S_GP / abs(S_GL)
    #max contracts held
    open_pl = 0
    L_TOT = 0
    S_TOT = 0
    if np.isnan(long['Return'].iloc[-1]):#refactor into loop
        open_pl += (stock['Close'].iloc[-1] - long['Entry Price'].iloc[-1]) / long['Entry Price'].iloc[-1]
        L_TOT += 1
    if np.isnan(short['Return'].iloc[-1]):
        open_pl += (short['Entry Price'].iloc[-1] - stock['Close'].iloc[-1]) / short['Entry Price'].iloc[-1]
        S_TOT += 1
    C_TOT = L_TOT + S_TOT
    C_TCT = len(cumulative) - C_TOT 
    L_TCT = len(long) - L_TOT
    S_TCT = len(short) - S_TOT
    C_AT = C_NP / C_TCT 
    L_AT = L_NP / L_TCT
    S_AT = S_NP / S_TCT
    #commission paid
    C_NWT = (cumulative['Return'] > 0).sum()
    L_NWT = (long['Return'] > 0).sum()
    S_NWT = (short['Return'] > 0).sum()
    C_NLT = (cumulative['Return'] <= 0).sum()
    L_NLT = (long['Return'] <= 0).sum()
    S_NLT = (short['Return'] <= 0).sum()
    C_PP = C_NWT / C_TCT * 100
    L_PP = L_NWT / L_TCT * 100
    S_PP = S_NWT / S_TCT * 100
    C_AWT = C_GP /C_NWT
    L_AWT = L_GP /L_NWT
    S_AWT = S_GP /S_NWT
    C_ALT = C_GL / C_NLT
    L_ALT = L_GL / L_NLT
    S_ALT = S_GL / S_NLT
    C_RAWAL = C_AWT / abs(C_ALT)
    L_RAWAL = L_AWT / abs(L_ALT)
    S_RAWAL = S_AWT / abs(S_ALT)
    C_LWT = cumulative['Return'].max() * 10
    L_LWT = long['Return'].max() * 100
    S_LWT = short['Return'].max() * 100
    C_LLT = cumulative['Return'].min() * 100
    L_LLT = long['Return'].min() * 100
    S_LLT = short['Return'].min() * 100
    C_ANBIT = 0
    L_ANBIT = 0
    S_ANBIT = 0
    C_ANBIWT = 0
    L_ANBIWT = 0
    S_ANBIWT = 0
    C_ANBILT = 0
    L_ANBILT = 0
    S_ANBILT = 0

    table = []
    table.append(["Net Profit",f'{C_NP:.2f}%',f'{L_NP:.2f}%',f'{S_NP:.2f}%'])
    table.append(["Gross Profit",f'{C_GP:.2f}%',f'{L_GP:.2f}%',f'{S_GP:.2f}%'])
    table.append(["Gross Loss",f'{C_GL:.2f}%',f'{L_GL:.2f}%',f'{S_GL:.2f}%'])
    table.append(["Max Run-up"])
    table.append(["Max Drawdown"])
    #table.append(["BnH Return",f'{BnH_Return:.2f}%'])
    #table.append(["Sharpe Ratio",C_SR,L_SR,S_SR])
    #Additional stats
    table.append(["BnH Annulized Return, Risk",f'{A_BnH_Return:.2f}%, {A_BnH_Risk:.2f}%'])
    table.append(["BnH Annulized Sharpe Ratio",f'{A_BnH_SR:.2f}'])
    table.append(["Algo Annulized Return, Risk",f'{A_C_Return:.2f}%, {A_C_Risk:.2f}%',f'{A_L_Return:.2f}%, {A_L_Risk:.2f}%',f'{A_S_Return:.2f}%, {A_S_Risk:.2f}%'])
    table.append(["Algo Annulized Sharpe Ratio", f'{A_C_SR:.2f}',f'{A_L_SR:.2f}',f'{A_S_SR:.2f}'])
    
    #------------------------
    table.append(["Sortino Ratio"])
    table.append(["Profit Factor",f'{C_PF:.2f}',f'{L_PF:.2f}',f'{S_PF:.2f}'])
    table.append(["Max Contracts Held"])
    table.append(["Open PL", f'{open_pl:.2f}%'])
    table.append(["Commission Paid"])
    table.append(["Total Closed Trades",C_TCT,L_TCT,S_TCT])
    table.append(["Total Open Trades",C_TOT, L_TOT, S_TOT])
    table.append(["Number Winning Trades",C_NWT,L_NWT,S_NWT])
    table.append(["Number Losing Trades",C_NLT,L_NLT,S_NLT])
    table.append(["Percent Profitable",f'{C_PP:.2f}%',f'{L_PP:.2f}%',f'{S_PP:.2f}%'])
    table.append(["Avg Trade",f'{C_AT:.2f}%',f'{L_AT:.2f}%',f'{S_AT:.2f}%'])
    table.append(["Avg Winning Trade",f'{C_AWT:.2f}%',f'{L_AWT:.2f}%',f'{S_AWT:.2f}%'])
    table.append(["Avg Losing Trade",f'{C_ALT:.2f}%',f'{L_ALT:.2f}%',f'{S_ALT:.2f}%'])
    table.append(["Ratio Avg Win / Avg Loss",f'{C_RAWAL:.2f}',f'{L_RAWAL:.2f}',f'{S_RAWAL:.2f}'])
    table.append(["Largest Winning Trade",f'{C_LWT:.2f}%',f'{L_LWT:.2f}%',f'{S_LWT:.2f}%'])
    table.append(["Largest Losing Trade",f'{C_LLT:.2f}%',f'{L_LLT:.2f}%',f'{S_LLT:.2f}%'])
    table.append(["Avg # Bars in Trades"])
    table.append(["Avg # Bars in Winning Trades"])
    table.append(["Avg # Bars in Losing Trades"])
    table.append(["Margin Calls"])
    print(tabulate(table))

def equity_curve(stock_data, cumulative_return, long_trades, short_trades):
    #visualizing equity curve (percentage)
    plt.plot(stock_data.index, stock_data['Cumulative % Return'], label = 'Buy and Hold')
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
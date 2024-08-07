from tkinter import E
from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import pandas as pd
from scipy import stats
import math

def format_df_value(x):
    if isinstance(x, (int, float)):
        if abs(x) >= 1e6:
            return f'{x:.2e}' #Scientific notation with two decimal places for large numbers
        else:
            return f'{x:.2f}' #2 decimal places
    elif isinstance(x, pd.Timestamp):
        return x.strftime('%Y-%m-%d') #Format datetime objects to YYYY-MM-DD
    return str(x)  # Return as string for non-numeric and non-datetime values

def print_df(df):
    #2 decimal places
    formatted_df = df.map(format_df_value)
    #For dataframes with dates as indexes
    if isinstance(df.index, pd.DatetimeIndex):
        formatted_df.index = df.index.strftime('%Y-%m-%d')
    print(tabulate(formatted_df, headers = df.columns.tolist(), tablefmt="github", numalign="right", stralign="right"))

def print_TV_stats(stock, total, long, short, enable_long, enable_short): #No longer passing in cumulative, long, short with slice indexing to get rid of initial trade
    C_GP = (np.prod(1 + total[total['Return'] > 0]['Return']) - 1) * 100
    L_GP = (np.prod(1 + long[long['Return'] > 0]['Return']) - 1) * 100
    S_GP = (np.prod(1 + short[short['Return'] > 0]['Return']) - 1) * 100
    C_GL = (np.prod(1 + -total[total['Return'] < 0]['Return']) - 1) * 100
    L_GL = (np.prod(1 + -long[long['Return'] < 0]['Return']) - 1) * 100
    S_GL = (np.prod(1 + -short[short['Return'] < 0]['Return']) - 1) * 100
    C_NWT = (total['Return'] > 0).sum()
    L_NWT = (long['Return'] > 0).sum()
    S_NWT = (short['Return'] > 0).sum()
    C_NLT = (total['Return'] <= 0).sum()
    L_NLT = (long['Return'] <= 0).sum()
    S_NLT = (short['Return'] <= 0).sum()
    C_NP, C_PF, L_NP, L_TOT, L_PF, S_NP, S_TOT, S_PF, open_pl = 0,0,0,0,0,0,0,0,0
    C_TCT, L_TCT, S_TCT = 0, 0, 0
    C_PP,L_PP,S_PP  = 0, 0, 0
    C_AT,L_AT,S_AT = 0, 0, 0
    L_ANBIT, L_ANBIWT, L_ANBILT = 0, 0, 0
    S_ANBIT, S_ANBIWT, S_ANBILT = 0, 0, 0
    C_ANBIT, C_ANBIWT, C_ANBILT = 0, 0, 0
    if enable_long:
        L_NP = (long['Total Return'].dropna().iloc[-1] - 1) * 100
        L_PF = L_GP / abs(L_GL)
        if np.isnan(long['Return'].iloc[-1]):#refactor into loop
            open_pl += (stock['Close'].iloc[-1] - long['P1'].iloc[-1]) / long['P1'].iloc[-1]
            L_TOT += 1
        L_TCT = len(long) - L_TOT
        L_AT = L_NP / L_TCT
        L_PP = L_NWT / L_TCT * 100
        L_ANBIT = long['Length'].sum() / len(long)
        try:
            L_ANBIWT = long[long['Return'] > 0]['Length'].sum() / len(total[total['Return'] > 0])
        except:
            pass
        try:
            L_ANBILT = long[long['Return'] < 0]['Length'].sum() / len(long[long['Return'] < 0])
        except:
            pass
    if enable_short:
        S_NP = (short['Total Return'].dropna().iloc[-1] - 1) * 100
        S_PF = S_GP / abs(S_GL)
        if np.isnan(short['Return'].iloc[-1]):
            open_pl += (short['P1'].iloc[-1] - stock['Close'].iloc[-1]) / short['P1'].iloc[-1]
            S_TOT += 1
        S_TCT = len(short) - S_TOT
        S_AT = S_NP / S_TCT
        S_PP = S_NWT / S_TCT * 100
        S_ANBIT = short['Length'].sum() / len(short)
        try:
            S_ANBIWT = short[short['Return'] > 0]['Length'].sum() / len(short[short['Return'] > 0])
        except:
            pass
        try:
            S_ANBILT = short[short['Return'] < 0]['Length'].sum() / len(short[short['Return'] < 0])
        except:
            pass
    try:
        C_NP = (total['Total Return'].dropna().iloc[-1] - 1) * 100
        C_PF = C_GP / abs(C_GL)
        C_TOT = L_TOT + S_TOT
        C_TCT = len(total) - C_TOT
        C_AT = C_NP / C_TCT
        C_PP = C_NWT / C_TCT * 100
        C_ANBIT = total['Length'].sum() / len(total)
        C_ANBIWT = total[total['Return'] > 0]['Length'].sum() / len(total[total['Return'] > 0])
        C_ANBILT = total[total['Return'] < 0]['Length'].sum() / len(total[total['Return'] < 0])
    except:
        print('The backtest produced no trades')
    
    L_MRU = long['Run-up'].max() * 100
    S_MRU = short['Run-up'].max() * 100
    C_MRU = max(L_MRU, S_MRU)
    L_MDD = long['Drawdown'].max() * 100
    S_MDD = short['Drawdown'].max() * 100
    C_MDD = max(L_MDD, S_MDD)
    BnH_Return = (stock['Total % Return'].iloc[-1] - 1) * 100
    A_BnH_Return = ((1 + BnH_Return / 100) ** (252 / len(stock)) - 1) * 100
    A_BnH_Risk = stock['% Return'].std() * (252)**(1/2) * 100
    A_C_Return = ((1 + C_NP / 100) ** (252 / len(stock)) - 1) * 100
    A_C_Risk = total['Return'].dropna().std() * (252)**(1/2) * 100
    A_L_Return = ((1 + L_NP / 100) ** (252 / len(stock)) - 1) * 100
    A_L_Risk = long['Return'].dropna().std() * (252)**(1/2) * 100
    A_S_Return = ((1 + S_NP / 100) ** (252 / len(stock)) - 1) * 100
    A_S_Risk = short['Return'].dropna().std() * (252)**(1/2) * 100
    risk_free_rate = 0.02
    A_BnH_ShR = (A_BnH_Return / 100 - risk_free_rate) / (A_BnH_Risk / 100)
    A_C_ShR = (A_C_Return / 100 - risk_free_rate) / (A_C_Risk / 100)
    A_L_ShR = (A_L_Return / 100 - risk_free_rate) / (A_L_Risk / 100)
    A_S_ShR = (A_S_Return / 100 - risk_free_rate) / (A_S_Risk / 100)
    A_BnH_Risk_Down = stock[stock['% Return'] < 0]['% Return'].std() * (252)**(1/2) * 100
    A_C_Risk_Down = total[total['Return'] < 0]['Return'].dropna().std() * (252)**(1/2) * 100
    A_L_Risk_Down = long[long['Return'] < 0]['Return'].dropna().std() * (252)**(1/2) * 100
    A_S_Risk_Down = short[short['Return'] < 0]['Return'].dropna().std() * (252)**(1/2) * 100
    A_BnH_SoR = (A_BnH_Return / 100 - risk_free_rate) / (A_BnH_Risk_Down / 100)
    A_C_SoR = (A_C_Return / 100 - risk_free_rate) / (A_C_Risk_Down / 100)
    A_L_SoR = (A_L_Return / 100 - risk_free_rate) / (A_L_Risk_Down / 100)
    A_S_SoR = (A_S_Return / 100 - risk_free_rate) / (A_S_Risk_Down / 100)
    #max contracts held
    
    #commission paid

    C_AWT = C_GP /C_NWT
    L_AWT = L_GP /L_NWT
    S_AWT = S_GP /S_NWT
    C_ALT = C_GL / C_NLT
    L_ALT = L_GL / L_NLT
    S_ALT = S_GL / S_NLT
    C_RAWAL = C_AWT / abs(C_ALT)
    L_RAWAL = L_AWT / abs(L_ALT)
    S_RAWAL = S_AWT / abs(S_ALT)
    C_LWT = total['Return'].max() * 100
    L_LWT = long['Return'].max() * 100
    S_LWT = short['Return'].max() * 100
    C_LLT = total['Return'].min() * 100
    L_LLT = long['Return'].min() * 100
    S_LLT = short['Return'].min() * 100

    table = []
    table.append(["Net Profit",f'{C_NP:.2f}%',f'{L_NP:.2f}%',f'{S_NP:.2f}%'])
    table.append(["Gross Profit",f'{C_GP:.2f}%',f'{L_GP:.2f}%',f'{S_GP:.2f}%'])
    table.append(["Gross Loss",f'{C_GL:.2f}%',f'{L_GL:.2f}%',f'{S_GL:.2f}%'])
    table.append(["Max Run-up",f'{C_MRU:.2f}%',f'{L_MRU:.2f}%',f'{S_MRU:.2f}%'])
    table.append(["Max Drawdown",f'{C_MDD:.2f}%',f'{L_MDD:.2f}%',f'{S_MDD:.2f}%'])
    table.append(["BnH Annualized Return, Risk",f'{A_BnH_Return:.2f}%, {A_BnH_Risk:.2f}%'])
    table.append(["BnH Annualized Sharpe Ratio",f'{A_BnH_ShR:.2f}'])
    table.append(["Algo Annualized Return, Risk",f'{A_C_Return:.2f}%, {A_C_Risk:.2f}%',f'{A_L_Return:.2f}%, {A_L_Risk:.2f}%',f'{A_S_Return:.2f}%, {A_S_Risk:.2f}%'])
    table.append(["Algo Annualized Sharpe Ratio", f'{A_C_ShR:.4f}',f'{A_L_ShR:.4f}',f'{A_S_ShR:.4f}'])
    table.append(["BnH Annualized Return, Risk",f'{A_BnH_Return:.2f}%, {A_BnH_Risk_Down:.2f}%'])
    table.append(["BnH Annualized Sortino Ratio",f'{A_BnH_SoR:.2f}'])
    table.append(["Algo Annualized Return, Risk",f'{A_C_Return:.2f}%, {A_C_Risk_Down:.2f}%',f'{A_L_Return:.2f}%, {A_L_Risk_Down:.2f}%',f'{A_S_Return:.2f}%, {A_S_Risk_Down:.2f}%'])
    table.append(["Algo Annualized Sortino Ratio", f'{A_C_SoR:.4f}',f'{A_L_SoR:.4f}',f'{A_S_SoR:.4f}'])
    
    #------------------------
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
    table.append(["Avg # Bars in Trades", f'{C_ANBIT:.2f}', f'{L_ANBIT:.2f}', f'{S_ANBIT:.2f}'])
    table.append(["Avg # Bars in Winning Trades", f'{C_ANBIWT:.2f}', f'{L_ANBIWT:.2f}', f'{S_ANBIWT:.2f}'])
    table.append(["Avg # Bars in Losing Trades", f'{C_ANBILT:.2f}', f'{L_ANBILT:.2f}', f'{S_ANBILT:.2f}'])
    table.append(["Margin Calls"])
    print(tabulate(table, headers = ['Stats','Cumulative','Long','Short'], tablefmt="simple_grid"))

def equity_curve(stock_data, total, long, short):
    _, (ax1, ax2) = plt.subplots(nrows = 2, sharex = True, height_ratios = [2.5, 1])
    #visualizing equity curve (percentage)
    ax1.plot(stock_data.index, stock_data['Total % Return'], label = 'Buy and Hold')

    #Add initial datapoint so the curves start at 1 on day 0
    cum_date = [stock_data.index[0]] + total['Date'].tolist()
    cum_return = [1] + total['Total Return'].tolist()
    long_date = [stock_data.index[0]] + long['Date2'].tolist()
    long_return = [1] + long['Total Return'].tolist()
    short_date = [stock_data.index[0]] + short['Date2'].tolist()
    short_return = [1] + short['Total Return'].tolist()

    #Use step because plt.plot will draw a straight line between datapoints
    ax1.step(cum_date, cum_return, label = "Total")
    ax1.step(long_date, long_return, label = 'Long')
    ax1.step(short_date, short_return, label = 'Short')

    ax1.set_title('Equity curve'), ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True)

    long_drawdown = [0] + [-e for e in long['Drawdown'].tolist()]
    ax2.step(long_date, long_drawdown, label = "Drawdown")
    ax2.set_xlabel('Date'), ax2.set_ylabel('Drawdown')
    ax2.legend()
    ax2.grid(True)
    
    plt.subplots_adjust(hspace=0)
    plt.tight_layout()
    plt.show()

def calc_bin(data, formula_num):
    if formula_num == 1:
        #Sturges' Formula, assumes normal distribution 
        return int(math.log(len(data), 2)) + 1
    if formula_num == 2:
        #Rice Rule, similar to Sturges' formula but generally results in a larger number of bins
        return int(len(data) ** 0.5) * 2
    #Scott's Rule, based on minimizing the integrated mean squared error for the histogram as an estimator of the probability density function
    bin_width = int((3.5 * np.std(data))/(len(data) ** (1/3)))
    return int((max(data) - min(data)) / bin_width)

def hist1d_base(data, formula_num):
    bin = calc_bin(data, formula_num)
    plt.hist(data, bin)
    plt.xlabel('Values'), plt.ylabel('Frequency'), plt.title("Returns Histogram"), plt.grid(True)
    plt.show()

def hist1d_stdev_mu(data, formula_num):
    bin = calc_bin(data, formula_num)
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

def hist2d_base(data, data1, formula_num):
    bin = calc_bin(data, formula_num)
    plt.hist2d(data, data1, bin)
    plt.show()

def montecarlo_equity_curve(montecarlo_results):
    final_values = []
    equity_curve = []
    for e in montecarlo_results:
        equity_curve.append(np.cumprod(1 + e))
        final_values.append(equity_curve[-1][-1])
    min_index = np.argmin(final_values)
    #floating point problem with directly indexing the medium
    mid_index = np.argmin(np.abs(np.array(final_values) - np.median(final_values)))
    max_index = np.argmax(final_values)
    
    for i, e in enumerate(equity_curve):
        if i == min_index:
            plt.plot(e, color='red', linewidth=1,zorder=10)
        elif i == max_index:
            plt.plot(e, color='green', linewidth=1,zorder=10)
        elif i == mid_index:
            plt.plot(e, color='yellow', linewidth=1,zorder=10)
        else:
            plt.plot(e, color='gray', linewidth=1,zorder=0)
    plt.xlabel('Trade #'), plt.ylabel('Equity')
    plt.grid(True)
    plt.show()

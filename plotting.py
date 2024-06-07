import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import numpy as np

def equity_curve(stock_data, cumulative_return, long_trades, short_trades):
    #visualizing equity curve (percentage)
    plt.plot(stock_data.index, np.cumprod(1+stock_data['Return']), label = 'Buy and Hold')
    #Use step because plt.plot will draw a straight line between datapoints that exists
    plt.step(cumulative_return['Date'], np.cumprod(1+cumulative_return['Return']), label = "Cumulative")
    plt.step(long_trades['Exit Date'], np.cumprod(1+long_trades['Return']), label = 'Long')
    plt.step(short_trades['Exit Date'], np.cumprod(1+short_trades['Return']), label = 'Short')

    plt.title('Stock Price'), plt.xlabel('Time (Trading days)'), plt.ylabel('Price'), plt.legend()
    plt.grid(True)
    plt.show()
    
def hist1d_base(data, bin):
    plt.hist(data, bin)
    plt.xlabel('Values'), plt.ylabel('Frequency'), plt.title("Returns Histogram"), plt.grid(True)
    plt.show()

def hist1d_stdev_mu(data,bin):
    _, axs = plt.subplots(tight_layout=True)
    # N is the count in each bin, bins is the lower-limit of the bin
    N, bins, patches = axs.hist(data, bins=bin)
    # We'll color code by height, but you could use any scalar
    fracs = N / N.max()
    # we need to normalize the data to 0..1 for the full range of the colormap
    norm = colors.Normalize(fracs.min(), fracs.max())
    # Now, we'll loop through our objects and set the color of each accordingly
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)
    # We can also normalize our inputs by the total number of counts
    axs.hist(data, bins=bin, density=True)

    #--------------------------------------
    #standard deviation +1 -1 and mean
    mean = np.mean(data)
    stdev = np.std(data)
    plt.axvline(x=mean+stdev, color='#2ca02c', alpha=0.7, label = f'{mean+stdev}')
    plt.axvline(x=mean-stdev, color='#2ca02c', alpha=0.7, label = f'{mean-stdev}')
    plt.axvline(x=mean, color='#d3212d', alpha=0.7, label = f'{mean}')

    plt.xlabel('Values'), plt.ylabel('Frequency'), plt.title("Returns Histogram"), plt.legend(), plt.grid(True)
    plt.show()
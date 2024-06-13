import os
import yfinance as yf
import pandas as pd

def get_stock_data(stock_name, starting_date, ending_date):
    #print all files in the folder "Stock_data"
    path = os.path.dirname(os.path.realpath(__file__)) + "/Stock_data/"
    print("Stock Data Downloaded:")
    [print(e) for e in os.listdir(path)]

    #read or download and save
    name = f'{path}{stock_name}.csv'
    try:
        stock_data = pd.read_csv(name, index_col='Date', parse_dates=True)
        stock_data = stock_data[starting_date:ending_date]
        print("Read")
        return stock_data
    except:
        stock_data = yf.download(stock_name, starting_date, ending_date)
        stock_data.to_csv(path_or_buf = name)
        print("Downloaded")
        return stock_data
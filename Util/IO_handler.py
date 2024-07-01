import os
import yfinance as yf
import pandas as pd

def get_stock_data(stock_name, starting_date, ending_date, interval):
    #Construct the path to the Stock_data folder
    main_script_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    stock_data_path = os.path.join(main_script_path, 'Stock_data')
    #Print all files in the folder "Stock_data"
    print("Stock Data Downloaded:")
    [print(e) for e in os.listdir(stock_data_path)]

    #read or download and save
    name = os.path.join(stock_data_path, f'{stock_name}.csv')
    try:
        stock_data = pd.read_csv(name, index_col='Date', parse_dates=True)
        #Filter the data within the date range
        if starting_date in stock_data.index and ending_date in stock_data.index:
            stock_data = stock_data[starting_date:ending_date]
            print("Read")
            return stock_data
        raise Exception #Proceed to except block if dates not found
    except:
        stock_data = yf.download(stock_name, starting_date, ending_date, interval = interval)
        stock_data.to_csv(path_or_buf = name)
        print("Downloaded")
        return stock_data
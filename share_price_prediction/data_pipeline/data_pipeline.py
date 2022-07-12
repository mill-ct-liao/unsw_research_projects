import numpy as np
import pandas as pd
import yfinance as yf

class data_loader:
    def __init__(self, codes=None, data=None, dates=None):
        self.codes = codes if codes is not None else None
        self.data = data if data is not None else None
        self.dates = dates if dates is not None else None
        
    def collect_data(self, start_date, end_date):
        for code in self.codes:
            try:
                company_prices = yf.Ticker(code + '.AX').history(start=start_date, end=end_date)
                company_prices['code'] = code
                historical_prices = pd.concat([historical_prices, company_prices])
            except:
                print('begin')
                historical_prices = yf.Ticker(code + '.AX').history(start=start_date, end=end_date)
                historical_prices['code'] = code
        return historical_prices
    
    def prepare_data(self, target, window_size, horizon_size):
        def time_window(start_date, end_date):
            return self.data.loc[(self.data.Date >= start_date)&(self.data.Date <= end_date)\
                      ,['Open','High','Low','Close','Volume','code']]

        def time_agg(x_timed_data, y_timed_data):
            x = np.array(x_timed_data.groupby(['code']).agg({'High':list, 'Low':list,\
                                                             'Open':list, 'Close':list,\
                                                             'Volume':list, 'code':list}).values.tolist())
            y = np.array(y_timed_data.groupby(['code']).agg({target:list}).values.tolist())
            return x, y

        print('total time:' , len(self.dates)-window_size-horizon_size+1)
        for time in range(len(self.dates)-window_size-horizon_size+1):
            x_start_date, x_end_date = self.dates[time].strftime("%Y-%m-%d"), self.dates[time+window_size-1].strftime("%Y-%m-%d")
            y_start_date, y_end_date = self.dates[time+window_size].strftime("%Y-%m-%d"), self.dates[time+window_size+horizon_size-1].strftime("%Y-%m-%d")
            try:
                x_timed_data = time_window(x_start_date, x_end_date)
                y_timed_data = time_window(y_start_date, y_end_date)
                x, y = time_agg(x_timed_data, y_timed_data)
                X = np.append(X, x, axis=0)
                Y = np.append(Y, y, axis=0)
            except:
                x_timed_data = time_window(x_start_date, x_end_date)
                y_timed_data = time_window(y_start_date, y_end_date)
                X, Y = time_agg(x_timed_data, y_timed_data)            
        return X, Y
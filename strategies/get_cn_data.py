import baostock as bs
import tushare as ts
import pandas as pd
import datetime
import os

class stock_data:

    def __init__(self, ticker = "000001"):
        if ticker[0] == '6':
            ticker = 'sh.' + ticker
        else:
            ticker = 'sz.' + ticker

        self.ticker = ticker
        self.today = datetime.datetime.today().strftime("%Y-%m-%d")

    def get_ticker(self):
        return self.ticker


    def get_stock_price(self, folder = "../cn_intraday"):
        #get intraday data online
        lg = bs.login(user_id="anonymous", password="123456")
        print('login respond error_code:'+lg.error_code)
        print('login respond  error_msg:'+lg.error_msg)
        ticker = self.ticker
        dateToday = self.today
        rs = bs.query_history_k_data_plus(ticker,
            "date,code,open,close,high,low,volume",
            start_date='2017-01-01', end_date= dateToday,
            frequency="d", adjustflag="3")
        print('query_history_k_data_plus respond error_code:'+rs.error_code)
        print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

        # convert to dataframe
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # append results
            data_list.append(rs.get_row_data())

        intraday = pd.DataFrame(data_list, columns=rs.fields)


        #if history, append at end
        file = folder + "/" + ticker + ".csv"
        if os.path.exists(file):
            history = pd.read_csv(file, index_col = 0)
            intraday.append(history)

        #save
        intraday.to_csv(file)
        print("intraday for [" + ticker + "] saved.")
        bs.logout()


    def get_ticker_list(self, folder = "/Users/zhouzijian/myproject/Backtest-Platform"):

        #save to a local file
        dateToday = self.today
        tickersRawData = ts.get_stock_basics()
        tickers = tickersRawData.index.to_list()
        return pd.DataFrame(tickers)
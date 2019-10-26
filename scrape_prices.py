import pandas as pd
import requests
import os
import sys
"""
Format:
    start_date =  '2010-1-1'  # follows this format: 2012-1-1
    end_date = '2019-10-1'      # follows this format: 2012-1-1
    ticker =  'AAPL'      # ticker symbol

Tiingo API:
Unique Symbols per Month 500
Max Requests Per Hour 500
Max Requests Per Day 20,000

Do look at Tiingo's API documentation for more limitation.
url: https://api.tiingo.com/documentation/general/overview
"""

def scrape_ticker(start_date, end_date,ticker, token`):
    api_call = "https://api.tiingo.com/tiingo/daily/{}/prices?startDate={}&endDate={}&token={}&resampleFreq=daily".format(ticker,start_date, end_date, token)
    stock_prices = requests.get(api_call)
    df_json = stock_prices.json()
    df = pd.DataFrame(df_json)
    df.index = df['date']
    df.drop('date', axis=1)

    if os.path.isdir('./data/'):
        df.to_csv("./data/{}.csv".format(ticker))
        print("Sent to data!")
    else:
        os.mkdir('./data/')
        df.to_csv("./data/{}.csv".format(ticker))
        print("Sent to data!")

# start_date, end_date,ticker
token = input("Enter token here: ")  #your Tiingo API token here
start_date = input('Enter start date (YYYY-M-D): \n')
end_date = input('Enter end date (YYYY-M-D): \n')
ticker = input('Input ticker:\n')
scrape_ticker(start_date, end_date, ticker)
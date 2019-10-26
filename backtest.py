import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class backtesting():

    def __init__(self, file):
        self.equity = dict()
        self.file = file


    def back_test(self):

    	f = self.file

    	f['change'] = f['adjClose'] - f['adjOpen']
    	f['accum'] = np.cumsum(f['change'])

    	self.equity = f['accum'].to_dict()


    def plot_equity_curve(self):

    	plt.plot(self.equity.values())
    	plt.show()


ticker = input("Ticker to backtest: \n")
file_path = './data/{}.csv'.format(ticker)

bt = backtesting(pd.read_csv(file_path))

bt.back_test()

bt.plot_equity_curve()


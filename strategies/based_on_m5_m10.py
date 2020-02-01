import pandas as pd
import numpy as np
import math
import get_cn_data as gcd
import matplotlib.pyplot as plt



ticker_name = str(input("enter ticker name: "))
getter = gcd.stock_data(ticker_name)
ticker = getter.get_ticker()
getter.get_stock_price()



df = pd.read_csv("../cn_intraday/" + ticker + '.csv')



for i in range(10):
    df['move' + str(i)] = df['close'].shift(i)


df['m3'] = df[['move0', 'move1', 'move2']].sum(axis = 1, skipna = False) / 3
df['m5'] = df[['move0', 'move1', 'move2', 'move3', 'move4']].sum(axis = 1, skipna = False) / 5
df['m10'] = df[['move0', 'move1', 'move2', 'move3', 'move4', 'move5', 'move6', 'move7', 'move8', 'move9']].sum(axis = 1, skipna = False) / 10

df['delta1'] = df['m3'] - df['m5']
df['delta2'] = df['m5'] - df['m10']

df['delta1'] = (df['delta1'] - df['delta1'].mean()) / df['delta1'].std()
df['delta2'] = (df['delta2'] - df['delta2'].mean()) / df['delta2'].std()

df['delta_score'] = df[['delta1', 'delta2']].sum(axis = 1, skipna = False) / 2
df['alpha'] = df['delta_score'].shift(1)

capital = 1000000
df['capital_alloc'] = df['alpha'] * capital
df['pct_change'] = df['close'].pct_change()
df['daily_pnl'] = df['capital_alloc'] * df['pct_change']

sharpe = np.sqrt(252) * (df['daily_pnl'].mean() - 0.04 / 252) / df['daily_pnl'].std()
print("sharpe ratio is:", sharpe)

plt.plot(df['daily_pnl'].cumsum())
plt.show()




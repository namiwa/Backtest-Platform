# pirce is 3% higher, volume is 30% more => buy
# price is 5% lower || volume 50 30% lower => sell

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import get_cn_data as gcd

ticker_name = str(input("Enter ticker number: "))
getter = gcd.stock_data(ticker_name)
getter.get_stock_price()
ticker = getter.get_ticker()

CAPITAL = 1000000

file = "../cn_intraday/" + ticker + ".csv"
df = pd.read_csv(file)


# strategy
df['pct_change_adj'] = df['close'].pct_change() - 0.03
df['vol_change_adj'] = df['volume'].pct_change() - 0.15

df['delta'] = (df['pct_change_adj'] > 0) & (df['vol_change_adj'] > 0)
df['delta'][df['delta'] == True] = 1
df['delta'][df['delta'] == False] = 0
df['delta2'] = (df['pct_change_adj'] < 0) & (df['vol_change_adj'] < 0)
df['delta2'][df['delta2'] == True] = -1
df['delta2'][df['delta2'] == False] = 0
df['delta_score'] = df[['delta', 'delta2']].sum(axis = 1, skipna = False)
df['alpha'] = df['delta_score'].shift(1)

# test
df['capital_alloc'] = df['alpha'] * CAPITAL
df['pct_change'] = df['close'].pct_change()
df['daily_pnl'] = df['capital_alloc'] * df['pct_change']

sharpe = np.sqrt(252) * (df['daily_pnl'].mean() - 0.04 / 252) / df['daily_pnl'].std()
print("sharpe ratio is:", sharpe)

plt.plot(df['daily_pnl'].cumsum())
plt.show()
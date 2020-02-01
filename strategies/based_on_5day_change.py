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
df['delta'] = df['close'].diff()
df['delta'][df['delta'] > 0] = 1
df['delta'][df['delta'] < 0] = -1
df['delta'][df['delta'] == 0] = 0
for i  in range(5):
	df['delta' + str(i)] = df['delta'].shift(i)

df['delta_score'] = df[['delta', 'delta0', 'delta1', 'delta2', 'delta3', 'delta4']].sum(axis = 1, skipna = False)
df['alpha'] = -df['delta_score'].shift(1)
df['alpha_adjusted'] = df['alpha'] / 5
df['capital_alloc'] = df['alpha_adjusted'] * CAPITAL
df['pct_change'] = df['close'].pct_change()
df['daily_pnl'] = df['capital_alloc'] * df['pct_change']

# calculate sharpe ratio (if using daily data)
sharpe = np.sqrt(252) * (df['daily_pnl'].mean() - 0.04 / 252) / df['daily_pnl'].std()
print('sharpe ratio is : ', sharpe)


# plot graph
plt.plot(df['daily_pnl'].cumsum())
plt.show()
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Dense, LSTM, BatchNormalization
from keras.models import Sequential, load_model
import get_cn_data as gcd

need_num = 50
training_num = 150
epoch = 10
batch_size = 512
capital = 1000000

ticker = str(input("Enter Ticker Number: "))

getter = gcd.stock_data(ticker)
getter.get_stock_price()
ticker = getter.get_ticker()

data = pd.read_csv("../cn_intraday/" + ticker + ".csv")
dataset = data.iloc[:, 3:4].values
training_dataset = dataset[:training_num]
sc = MinMaxScaler(feature_range = (-1, 1))


training_dataset_scaled = sc.fit_transform(X=training_dataset)

x_train = []
y_train = []

for i in range(need_num, training_dataset_scaled.shape[0]):
	x_train.append(training_dataset_scaled[i - need_num : i])
	y_train.append(training_dataset_scaled[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

file = "../models/" + ticker + ".model"
model = None
if os.path.exists(file):
	model = load_model(file)
else:
	model = Sequential()
	model.add(LSTM(units = 128, return_sequences = True, input_shape = [x_train.shape[1], 1]))
	model.add(BatchNormalization())

	model.add(LSTM(units = 128))
	model.add(BatchNormalization())

	model.add(Dense(units = 1))

	model.compile(loss = "mse", optimizer = "rmsprop")
	model.fit(x_train, y_train, epochs = epoch, batch_size = batch_size)

	model.save(file)


inputs = dataset[training_num - need_num:]
inputs = inputs.reshape(-1, 1)
inputs = sc.transform(inputs)

predictions = []



for i in range(need_num, inputs.shape[0]):
	predictions.append(inputs[i - need_num: i, 0])

predictions = np.array(predictions)
predictions = np.reshape(predictions, (predictions.shape[0], predictions.shape[1], 1))


real_price = dataset[training_num:]
predicted_price = model.predict(predictions)

def predict(dataset):
	latest = dataset[-need_num:]

	for i in range(need_num):
		tmp = latest[np.newaxis,:,:]
		cur = (model.predict(tmp) * 0.1 + 1) * (latest[-1][0])
		latest = np.append(latest[1:], cur, axis = 0)

	plt.plot(latest, color = 'blue', label = 'predicted price')

predict(dataset)

#calculate charpe
def calc_sharpe(d, predicted_price):
	data = d.copy()
	data = data.iloc[training_num:]
	data['alpha'] = pd.DataFrame(predicted_price.flatten())
	data['allocated_capital'] = capital * data['alpha']
	data['pct_change'] = data['close'].pct_change()
	data['daily_pnl'] = data['allocated_capital'] * data['pct_change']

	#plt.plot(data['daily_pnl'].cumsum(), color = 'red', label = 'predicted pnl')

	return np.sqrt(252) * data['daily_pnl'].mean() / data['daily_pnl'].std()


print(calc_sharpe(data, predicted_price))


plt.xlabel(xlabel = 'Time')
plt.ylabel(ylabel = 'Returns/Prices')
plt.legend()
plt.show()


'''
predicted_price = sc.inverse_transform(predicted_price)
plt.plot(real_price, color='red', label='Real Stock Price')
plt.plot(predicted_price, color='blue', label='Predicted Stock Price')
plt.title(label = ticker + " prediction")
plt.xlabel(xlabel='Time')
plt.ylabel(ylabel= ticker + ' Stock Price')
plt.legend()
plt.show()
'''



















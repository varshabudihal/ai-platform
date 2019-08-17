# -*- coding: utf-8 -*-
"""Apple_stock_using_RNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LED8-TqLyp4TCOordD18VZkQEmFcOw6a

### Why Should you invest in this Stock?

Imagine someone who is new into the stock market world and he wants to know what price the particular stock would be and why should he invest in it to gain the benefits?

I have tried to create a model which gives insight of a stock for over 14 years of data which would help an individual to look at past trends and decide if they want to invest into it.
Here I have taken into consideration Apple Stock from year 2006 to 2019 and fit a model over it to determine if the model predicts the real stock market price.

### Important Imports
"""

import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet

import mlflow
import mlflow.sklearn

def eval_metrics(actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

# Commented out IPython magic to ensure Python compatibility.
#Visualization Imports

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
# %matplotlib inline

from pandas_datareader import DataReader
from datetime import datetime
#Do this to not worry about floating number later

from __future__ import division

tech_comp = ['AAPL']

end = datetime(2019,8,15)

start = datetime(end.year-14,end.month,end.day)

for stock in tech_comp:
  globals()[stock] = DataReader(stock,'yahoo',start,end)

AAPL.describe()

data = pd.DataFrame(AAPL)

data.describe()

data.info()

"""###Split data into training and testing set with 80% of the data going into training"""

# Commented out IPython magic to ensure Python compatibility.
training, testing = train_test_split(data, test_size=0.2, random_state=0)
print("Total sample size = %i; training sample size = %i, testing sample size = %i"\
#      %(data.shape[0],training.shape[0],testing.shape[0]))

"""###In order to pick particular columns - in this project "Open" ioc is done so that column can be selected by index numbers"""

df_train_s = training.iloc[:,2:3].values
df_test_s = testing.iloc[:,2:3].values

"""### Plotted the Adj Closing price of Apple stock. Seems like the price for Apple is always an Upward trend."""

data["Adj Close"][:'2016'].plot(figsize=(16,4),legend=True)
data["Adj Close"]['2017':].plot(figsize=(16,4),legend=True)
plt.legend(['Training set on 80% data','Test set on rest 20%'])
plt.title('Apple stock price')
plt.show()

"""### Plotted the number of Stocks purchased by people. Seems like the stock purchase went stable post 2015. We can see that the stocks were purchased at a high volume from years mid 2006 to 2014"""

data['Volume'][:'2016'].plot(figsize=(16,4),legend=True)
data['Volume']['2017':].plot(figsize=(16,4),legend=True)
plt.legend(['Training set on 80% data','Test set on rest 20%'])
plt.title('Apple stock price')
plt.show()

# Feature Scaling

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range=(0,1))
training_scaled = sc.fit_transform(training)

"""### 60 Timestamps ..since the data will train the model on previous 60 rows to predict the next value"""

# Creating a data structure with 60 timestamps and 1 output

X_train = []
y_train = []
for i in range(60, 2820):
    X_train.append(training_scaled[i - 60 : i , 0])
    y_train.append(training_scaled[i,0])
    
X_train, y_train = np.array(X_train) , np.array(y_train)

# Reshaping

X_train = np.reshape(X_train,(X_train.shape[0], X_train.shape[1], 1))

# Importing keras libs and packages

from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, GRU, Bidirectional
from keras.optimizers import SGD
import math
from sklearn.metrics import mean_squared_error

# The LSTM architecture
regressor = Sequential()
# First LSTM layer with Dropout regularisation
regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1],1)))
regressor.add(Dropout(0.2))
# Second LSTM layer
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))
# Third LSTM layer
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))
# Fourth LSTM layer
regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))
# The output layer
regressor.add(Dense(units=1))

# Compiling the RNN
regressor.compile(optimizer='rmsprop',loss='mean_squared_error')
# Fitting to the training set
regressor.fit(X_train,y_train,epochs=50,batch_size=32)

real_stock_price = testing.iloc[: , 2:3].values

dataset_total = pd.concat((training["Adj Close"], testing["Adj Close"]) , axis = 0)
inputs = dataset_total[len(dataset_total) - len(testing) - 60 :].values
inputs = inputs.reshape(-1 , 1)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
inputs= scaler.fit_transform(inputs)
inputs = scaler.transform(inputs)

X_test = []
for i in range(60, 705):
    X_test.append(inputs[i - 60 : i , 0])

X_test = np.array(X_test)
X_test = np.reshape(X_test , (X_test.shape[0] , X_test.shape[1] , 1))
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = scaler.inverse_transform(predicted_stock_price)

plt.plot(real_stock_price, color = 'red' , label = ' Real Apple Stock Price')
plt.plot(predicted_stock_price, color = 'blue' , label = 'Predicted Apple Stock Price')
plt.title('Apple Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Apple Stock Price') 
plt.legend()
plt.show()

"""### The above plot displays the real stock price vs the predicted. The predicted stock price is a straight line which might be because of the data. Since it is a large dataset, and divding it randomly might have caused some noise. Besides that, it can also be infered that the stock price is almost always constant over the years giving the individual who invested a stable stock to consider for a long run. 
###There is also a possibility that money would have gained value over the years. This I could say is because Apple buying volumes are constant and the price of closing value for the day varies.
"""








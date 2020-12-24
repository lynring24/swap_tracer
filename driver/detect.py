from pandas import DataFrame
from pandas import Series
from pandas import concat
from pandas import read_csv
from pandas import datetime
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from math import sqrt
from matplotlib import pyplot
import numpy
import sys

# frame a sequence as a supervised learning problem
def timeseries_to_supervised(data, lag=1):
    df = DataFrame(data)
    columns = [df.shift(i) for i in range(1, lag+1)]
    print (columns)
    columns.append(df)
    df = concat(columns, axis=1)
    df.fillna(0, inplace=True)
    return df

# create a differenced series
def difference(dataset, interval=1):
	diff = list()
	for i in range(interval, len(dataset)):
		value = dataset[i] - dataset[i - interval]
		diff.append(value)
	return Series(diff)


# load dataset
series = read_csv(sys.argv[1] , header=0, index_col=0, squeeze=True, usecols=['timestamp', 'address', 'mode'])
series = series[series['mode']=='map']
series = series.drop('mode', axis=1)

# transform data to be stationary
#raw_values = series.values
#diff_values = difference(raw_values, 1)

# transform data to be supervised learning
#upervised = timeseries_to_supervised(diff_values, 1)

# split data into train and test-sets
#rain, test = supervised_values[0:-12], supervised_values[-12:]

# calculate differences

series['diff'] = series['address'].diff(periods=1).abs()

#hist = series.groupby('diff').agg(['count'])

#print(hist)

# create historgram by the abs(diff) 
norm = series['diff'].value_counts(normalize=True).sort_values(ascending=False).to_frame()

percentage_20 = int(len(norm) *  0.2)
print(norm.head(5))
sum_20 = norm.head(percentage_20)['diff'].sum()
print(sum_20)

# print(norm.query("index==4096.0"))
norm.loc[4096.0, 'diff']


print ("\n")
if norm.loc[4096, 'diff'] > 0.5 or sum_20 >0.5:
    print ("[Stat] Linear Access Pattern Detected \n")
else:
    print ("[Stat] Linear Access Pattern Not Detected \n")





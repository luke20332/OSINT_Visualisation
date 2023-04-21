"""
ARIMA, aka AutoRegressive Integrated Moving Average is a machine learning method used to predict future values based on time series data

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import polars as pl
from pathlib import Path

import sklearn
from sklearn import *
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_selection import r_regression

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARMA


# Read the data
data = pd.read_excel('conflicts\SIPRI-Milex-data-1949-2022.xlsx', sheet_name='Constant (2021) US$', index_col=0, header=5)
data = data.drop(['Unnamed: 1', 'Notes'], axis=1)

# Unused index names:
extra_index = ['Africa', 'North Africa','sub-Saharan Africa','Americas','Central America and the Caribbean',
'North America', 'South America','Asia & Oceania', 'Oceania','South Asia', 'East Asia','South East Asia','Central Asia',
'Europe','Eastern Europe','Western Europe','Middle East']

data = data.drop(extra_index, axis=0)
data = data.drop(data.iloc[0])

data = data.fillna(-1)
data = data.replace(['...', 'xxx'], -1)

# Reading in UCDP data
prio_df = pd.read_csv('conflicts\\ucdp-prio-acd-221.csv', header=0)


# remove unnecessary columns
remove_columns = ['incompatibility', 'territory_name', 'cumulative_intensity', 'type_of_conflict','start_date', 
        'start_prec', 'start_date2', 'start_prec2', 'ep_end',
       'ep_end_date', 'ep_end_prec', 'gwno_a', 'gwno_a_2nd', 'gwno_b',
       'gwno_b_2nd', 'gwno_loc', 'region', 'version']


# total military expenditure for each year
total_mil_exp_year = data.sum(axis=0)
total_mil_exp_year = total_mil_exp_year.sort_values(ascending=False)


df = pd.DataFrame(list(zip(total_mil_exp_year.index, total_mil_exp_year.values)),columns = ["years", "expenditure"]  
)
df = df.sort_values(["years"])


ucdp_num_conflicts_year = prio_df.groupby('year')['conflict_id'].count()
#ucdp_num_conflicts_year = ucdp_num_conflicts_year.sort_values(ascending=False)
#print(ucdp_num_conflicts_year.values[4:]) # yearly number of conflicts from 1950 onwards

"""
UNCOMMENT FOR CONFLICTS"""
#df["conflict"] = ucdp_num_conflicts_year.values[3:]

# df should now have values for total global milex and conflicts based on the year 

#df.plot(x='years', y='expenditure',kind='line')
#plt.show()

df.index = pd.to_datetime(df.years, format='%Y')


df = df.drop('years', axis=1)

print(df)

"""
plt.figure(figsize=(16,7))
fig = plt.figure(1)
ax1 = fig.add_subplot(111)
ax1.set_xlabel("time")
ax1.set_ylabel("Expenditure")
ax1.plot(df)
plt.show()
"""

# checking stationality

#find rolling average of the mean and standard deviation
rollMean = df.rolling(12).mean()
rollStd = df.rolling(12).std()

plt.figure(figsize=(16,7))
fig = plt.figure(1)

orig = plt.plot(df, color='blue', label='Original')
mean = plt.plot(rollMean, color = 'red', label='Rolling Mean')
std = plt.plot(rollStd, color = 'black', label = 'Rolling Std')
plt.legend(loc='best')
plt.title('Rolling Mean & Std dev')
plt.savefig("rollingmeanandstddev.png")
plt.show()


# to be stationary, rolling mean and std dev need to be stationary - so the data is not stationary
# can take a log transform to make it stationary

ts_log = np.log(df) # log tranform of series
plt.plot(ts_log)
plt.show()

# not stationary still, so we decompose into seasonal components.

from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(ts_log, model = 'multiplicative')
# diff components = s

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.figure(figsize=(16,7))
fig = plt.figure(1)

plt.subplot(411)
plt.plot(ts_log, label = 'Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal, label='Seasonality')
plt.legend(loc='best')
plt.plot(residual, label='Residuals')
plt.legend(loc='best')

plt.show()

"""
time series broken down into 4 components
firs = original
2 = trend component
3 = seasonality
4 - residual
trend component contributes more
not stationary, so create a differencing time series
"""

# shift up by 1, subtract from original
# log it then find difference
# expect differnce to be stationary
plt.figure(figsize=(16,7))
fig = plt.figure(1)
ts_log_diff = ts_log - ts_log.shift()
plt.plot(ts_log_diff)


# find rolling stats

rollMean = ts_log_diff.rolling(12).mean()
rollStd = ts_log_diff.rolling(12).std()

orig = plt.plot(ts_log_diff, color='blue', label='Original')
#differnced time series 

mean = plt.plot(rollMean, color='red', label='RollingMean')
std = plt.plot(rollStd, color='black', label = 'Rolling Std')
plt.legend(loc='best')
plt.title("rolling mean and std dev")
plt.show()

# no upward pattern in mean and std dev, so should be stationary - not a major difference between 2 differences of means

# can do dickey fuller test to cross validate

from statsmodels.tsa.stattools import acf, pacf
lag_acf = acf(ts_log_diff, nlags=20)
lag_pacf = pacf(ts_log_diff, nlags=20)
# determine order of ar component and ma component
# auto correlation and partial


import statsmodels.api as sm
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(ts_log_diff.dropna(), lags=35, ax = ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(ts_log_diff.dropna(), lags=35, ax=ax2)
plt.show()


#when doing arima, dont know what order or ar, ma, i are good for model
# charts help
# highlighted part = confidence intervals
# first line that crosses highlist = line of order
# 1 in autocorrelation AR
# 1 then 2 in partial MA
# (1,0,1) or (1,0,2)

from statsmodels.tsa.arima.model import ARIMA


plt.figure(figsize = (16,8))
model = ARIMA(ts_log, order = (1,0,1))
results_ARIMA = model.fit()
plt.plot(ts_log_diff)
plt.plot(results_ARIMA.fittedvalues, color='red')
plt.show()

# taking results back to original scale

ARIMA_diff_predictions = pd.Series(results_ARIMA.fittedvalues, copy = True)
print(ARIMA_diff_predictions.head())


ARIMA_diff_predictions_cumsum = ARIMA_diff_predictions.cumsum()
print(ARIMA_diff_predictions_cumsum)

ARIMA_log_prediction = pd.Series(ts_log.iloc[0], index=ts_log.index)
ARIMA_log_prediction = ARIMA_log_prediction.add(ARIMA_diff_predictions_cumsum, fill_value=0)
ARIMA_log_prediction.head()



plt.figure(figsize=(12,8))
predictions_ARIMA = np.exp(ARIMA_log_prediction)
plt.plot(df)
plt.plot(predictions_ARIMA)
#plt.title("RMSE: %.4f"% np.sqrt(sum((predictions_ARIMA-(df))**2)/len(df)))
plt.show()

#*len(df)

print(results_ARIMA.predict(10,20))

future = results_ARIMA.predict(70,90)
print(future)

import pmdarima as pm

def arimamodel(timeseries):
    automodel = pm.auto_arima(timeseries,
                              start_p=3,
                              start_q=3,
                              max_p = 5,
                              max_q = 5,
                              test = 'adf',
                              seasonal=True,
                              trace=True)
    return automodel

print(arimamodel(ts_log))
# returns 1,1,3
# doesnt return anything = not hte best way to make the data stationary


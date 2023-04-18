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

df["conflict"] = ucdp_num_conflicts_year.values[3:]

# df should now have values for total global milex and conflicts based on the year 

df.plot(x='years', y='conflict',kind='line')
#plt.show()

# need to run an Augmented Dickey-Fuller test on the data, which retains parameters of the data, determining whether or not the data is stationary or not

def ad_test(dataset):
    dftest = adfuller(dataset, autolag='AIC')
    print("1 - ADF:{}".format(dftest[0]))
    print("2 - p_value:{}".format(dftest[1]))
    print("3 - Num of lags:{}".format(dftest[2]))
    print("4 - num of observations used for ADF regression and critical values calculation:{}".format(dftest[3]))
    print("5 - Critical values:")
    for key, val in dftest[4].items():
        print("\t", key,": ", val)


ad_test(df['conflict'])

# P-Value = probability, 0.725, so it is not stationary

from pmdarima import auto_arima
import warnings
warnings.filterwarnings("ignore")

stepwise_fit = auto_arima(df['conflict'], trace=True, suppress_warnings=True)
#stepwise_fit.summary()


from statsmodels.tsa.arima.model import ARIMA 

train = df.iloc[:-15]
test = df.iloc[-15:]

print(train.shape, test.shape)

model=ARIMA(train['conflict'],order=(0,1,0))
model = model.fit()
model.summary()
print(model.summary())

start = len(train)
end = len(train) + len(test)-1
pred = model.predict(start=start, end=end, typ='levels')
print(pred)

pred.plot(legend=True)
test['conflict'].plot(legend=True)
plt.show()
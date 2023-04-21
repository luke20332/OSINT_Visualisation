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
import sklearn.cluster as cluster
from sklearn.model_selection import train_test_split, cross_val_score

from sklearn.linear_model import ElasticNet

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

#prio_df = prio_df.drop(remove_columns, axis=1)


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

#print(df.head)

# the testing dataframes - pre conflict

df_pre_67 = df.iloc[:18,:]
df_post_67 = df.iloc[18:,:]

df_pre_91 = df.iloc[:39,:]
df_post_91 = df.iloc[39:,:]

df_pre_15 = df.iloc[:66,:]
df_post_15 = df.iloc[66:,:]


df_pre_80 = df.iloc[:30,:]
df_post_80 = df.iloc[30:,:]

print(df_pre_80)

"""
fig, ax = plt.subplots(figsize=(6,4))
ax.scatter(df['years'], df['conflict'])
ax.plot(df['years'], df['conflict'])
ax.set_xlabel('Years')
ax.set_ylabel('Conflicts')
plt.show()
"""

# got the splitted dataframes, now need to linear regression on teh expendituere
# data so that if similar trends are present then conflict is likely - or will spike

regr67 = LinearRegression()
regr67.fit(np.array(list(df_pre_67['years'])).astype(float).reshape(-1,1), np.array(list(df_pre_67['conflict'])).astype(float))

print("sklearn's prediction for weight and bias")
print('w_1 = {:.2f}'.format(regr67.coef_.item()))
print('b = {:.2f}'.format(regr67.intercept_.item()))

y_pred_67 = regr67.predict(np.array(list(df['years'])).astype(float).reshape(-1,1))

regr91 = LinearRegression()
regr91.fit(np.array(list(df_pre_91['years'])).astype(float).reshape(-1,1), np.array(list(df_pre_91['conflict'])).astype(float))

print("sklearn's prediction for weight and bias")
print('w_1 = {:.2f}'.format(regr91.coef_.item()))
print('b = {:.2f}'.format(regr91.intercept_.item()))

y_pred_91 = regr91.predict(np.array(list(df['years'])).astype(float).reshape(-1,1))

regr15 = LinearRegression()
regr15.fit(np.array(list(df_pre_15['years'])).astype(float).reshape(-1,1), np.array(list(df_pre_15['conflict'])).astype(float))

print("sklearn's prediction for weight and bias")
print('w_1 = {:.2f}'.format(regr15.coef_.item()))
print('b = {:.2f}'.format(regr15.intercept_.item()))

y_pred_15 = regr15.predict(np.array(list(df['years'])).astype(float).reshape(-1,1))


fig,ax = plt.subplots(figsize=(6,4))
ax.scatter(df['years'],df['conflict'])
ax.plot(df['years'], y_pred_67, y_pred_91, y_pred_15)
#ax.plot(df['years'],df['expenditure'])
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()

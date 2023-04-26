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

df_pre_10 = df.iloc[:61,:]
df_post_10 = df.iloc[61:,:]

print(df_post_10)

"""
fig, ax = plt.subplots(figsize=(6,4))
ax.scatter(df['years'], df['conflict'])
ax.plot(df['years'], df['conflict'])
ax.set_xlabel('Years')
ax.set_ylabel('Conflicts')
plt.show()
"""


regr10 = LinearRegression() # train on pre 2010 data
regr10.fit(np.array(list(df_pre_10['expenditure'])).astype(float).reshape(-1,1), np.array(list(df_pre_10['conflict'])).astype(float))

print("sklearn's prediction for weight and bias")
print('w_1 = {:.2f}'.format(regr10.coef_.item()))
print('b = {:.2f}'.format(regr10.intercept_.item()))

y_pred_10 = regr10.predict(np.array(list(df['expenditure'])).astype(float).reshape(-1,1))


# an attribute of the data, not the model
#pearsonsR = r_regression(np.array(list(df_pre_10['expenditure'])).reshape(-1,1), df_pre_10['conflict'])
#print("pre 2010 r = ".format(pearsonsR))

print("We get a mean squared error of {} with a simple linear regression model".format(mean_squared_error(df['conflict'], y_pred_10)))

fig,ax = plt.subplots(figsize=(6,4))
ax.scatter(df['expenditure'],df['conflict'])
ax.plot(df['expenditure'], y_pred_10)
#ax.plot(df['years'],df['expenditure'])
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.savefig("linear-reg-prepost-2010.png")
plt.show()





# training model on the pre 2010 data
poly_10 = PolynomialFeatures(degree=2)
x_poly_10 = poly_10.fit_transform(np.array(list(df_pre_10['expenditure'])).reshape(-1,1))
regr10.fit(x_poly_10, df_pre_10['conflict'])


x_plot_10 = np.linspace(min(df['expenditure']),max(df['expenditure']),73).reshape(-1, 1)
y_pred_poly = regr10.predict(poly_10.transform(x_plot_10))


fig, ax = plt.subplots(figsize=(6,4))
ax.scatter(df['expenditure'], df['conflict'])
ax.plot(x_plot_10, y_pred_poly, '-r')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()

print("We get a mean squared error of {} with a polynomial linear regression model".format(mean_squared_error(df['conflict'],y_pred_poly)))

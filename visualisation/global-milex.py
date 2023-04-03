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

prio_df = prio_df.drop(remove_columns, axis=1)

# Filtering UCDP data
print(data.head())
print(prio_df.head())
# total military expenditure for each country
total_mil_exp = data.sum(axis=1)
total_mil_exp = total_mil_exp.sort_values(ascending=False)

"""
# Plotting the data 
plt.figure(figsize=(20,10))
sns.barplot(x=total_mil_exp.index[:10], y=total_mil_exp.values[:10])
plt.title('Total Military Expenditure by Country')
plt.xlabel('Country')
plt.ylabel('Total Military Expenditure, Trillions')
plt.xticks(rotation=90)
#plt.show()
"""

# total military expenditure for each year
total_mil_exp_year = data.sum(axis=0)
total_mil_exp_year = total_mil_exp_year.sort_values(ascending=False)

print(type(total_mil_exp_year))

"""
# Plotting the data
plt.figure(figsize=(20,10))
sns.barplot(x=total_mil_exp_year.index, y=total_mil_exp_year.values)
plt.title('Total Military Expenditure by Year')
plt.xlabel('Year')
plt.ylabel('Total Military Expenditure')
plt.xticks(rotation=90)
#plt.show()
"""

regr = LinearRegression()
regr.fit(np.array(list(total_mil_exp_year.index)).astype(float).reshape(-1,1), np.array(list(total_mil_exp_year.values)).astype(float))

poly = PolynomialFeatures(degree = 2, include_bias=False)

poly_features = poly.fit_transform(np.array(list(total_mil_exp_year.index)).reshape(-1,1))

poly_reg_model = LinearRegression()
poly_reg_model.fit(poly_features, np.array(list(total_mil_exp_year.values)))

x_vals = np.linspace(1949, 2020, 72).reshape(-1, 1)
y_predicted = poly_reg_model.predict(poly.transform(x_vals))

plt.figure()
plt.scatter(np.array(list(total_mil_exp_year.index)), np.array(list(total_mil_exp_year.values)))
#plt.plot(np.array(list(keys)), y_predicted, c = "red")
plt.plot(x_vals, y_predicted, c = "red")
plt.show()


#pred22 = poly_reg_model.predict(poly.transform([[2022]]))
#print(total_mil_exp_year.values[0]) #2021 value
#print(pred22)

total_mil_exp_year.to_dict()

years_forecast = list(total_mil_exp_year.index)

for i in range(1,9):
    years_forecast.append(2021+i)
    #milex_forecast.append(poly_reg_model.predict(poly.transform([[2021+i]]))[0])
    total_mil_exp_year[2021+i] = poly_reg_model.predict(poly.transform([[2021+i]]))[0]

total_mil_exp_year.to_dict()

poly_forecast = PolynomialFeatures(degree = 2, include_bias=False)

poly_forecast_features = poly_forecast.fit_transform(np.array(years_forecast).reshape(-1,1))

poly_forecast_reg_model = LinearRegression()
poly_forecast_reg_model.fit(poly_forecast_features, np.array(total_mil_exp_year.values))

x_forecast_vals = np.linspace(1949, 2029, 81).reshape(-1, 1)
y_forecast_predicted = poly_forecast_reg_model.predict(poly_forecast.transform(x_forecast_vals))


plt.figure()
plt.scatter(years_forecast, list(total_mil_exp_year.values))
#plt.plot(np.array(list(keys)), y_predicted, c = "red")
plt.plot(x_forecast_vals, y_forecast_predicted, c = "red")
plt.show()
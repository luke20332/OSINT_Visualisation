"""
In this file I will attempt multiple linear regression, with the feature variables being number of conflicts and total global expenditure, which have both been plotted as a function of time



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
import sklearn.cluster as cluster


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

"""
# Filtering UCDP data
print(data.head())
print(prio_df.head())
# total military expenditure for each country
total_mil_exp = data.sum(axis=1)
total_mil_exp = total_mil_exp.sort_values(ascending=False)
"""

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

#print(total_mil_exp_year.index)
#print(total_mil_exp_year.values)

#print(zip(total_mil_exp_year.index, total_mil_exp_year.values))

#create a dataframe with the columns being years, global miitary expenditure and number of global conflicts.

df = pd.DataFrame(list(zip(total_mil_exp_year.index, total_mil_exp_year.values)),columns = ["years", "expenditure"]  
)
df = df.sort_values(["years"])

print(df.head)

ucdp_num_conflicts_year = prio_df.groupby('year')['conflict_id'].count()
#ucdp_num_conflicts_year = ucdp_num_conflicts_year.sort_values(ascending=False)
print(ucdp_num_conflicts_year.values[4:]) # yearly number of conflicts from 1950 onwards

df["conflict"] = ucdp_num_conflicts_year.values[3:]

print(df.head)

sns.scatterplot(x=df["expenditure"], y=df["conflict"])
plt.show()
# graph shows a positive correlation between global expenditure and total conflict around the world

#regr = LinearRegression()
#regr.fit(df['expenditure'], df['conflict'])

x_bias = np.concatenate((np.ones(73).reshape(-1,1), np.array(list(df['expenditure'])).reshape(-1,1)), axis=1)

w_fit = np.linalg.lstsq(x_bias, df['conflict'], rcond=None)[0]
y_pred = np.dot(x_bias, w_fit)

fig,ax = plt.subplots(figsize=(6,4))
ax.scatter(df['expenditure'],df['conflict'])
ax.plot(df['expenditure'], y_pred, '-r')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()

pearsonsR = r_regression(np.array(list(df['expenditure'])).reshape(-1,1), df['conflict'])
print("We get a Pearson's Correlation Coefficient of {}, which is suggests a strong positive correlation between global expenditure and total conflict around the world.".format(pearsonsR[0]))

print("We get a mean squared error of {} with a simple linear regression model".format(mean_squared_error(df['conflict'], y_pred)))




# polynomial regression model

regr = LinearRegression()
poly = PolynomialFeatures(degree=4)
x_poly = poly.fit_transform(np.array(list(df['expenditure'])).reshape(-1,1))
regr.fit(x_poly, df['conflict'])

x_plot = np.linspace(min(df['expenditure']),max(df['expenditure']),73).reshape(-1, 1)
y_pred_poly = regr.predict(poly.transform(x_plot))

fig, ax = plt.subplots(figsize=(6,4))
ax.scatter(df['expenditure'], df['conflict'])
ax.plot(x_plot, y_pred_poly, '-r')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()

print("We get a mean squared error of {} with a polynomial linear regression model".format(mean_squared_error(df['conflict'],y_pred_poly)))

# coefficient of determination R^2
# The proportion of the variation in the dependent variable (conflict) that is predictable from the independent, so in essence it is a measure of how good the model is at predicting the dependent variable.

print("The coefficient of determination for the linear model is {}".format(r2_score(df['conflict'],y_pred)))
print("\n")
print("The coefficient of determination for the polynomial model is {}".format(r2_score(df['conflict'],y_pred_poly)))

print("This suggests that the polynomial model, with degree 2 is better at estimating the rate of conflict around the world based on the global expenditure of that year")
"""
we would like x to be the independtent variables (a subset of the dataframe), and Y to be the dependent variable we would like to predict
for this scenario, lets try to predict global conflict based on year and global expenditure

does it make sense to regress against year? - NO
"""



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
# summary statistics for conflict and expenditure

#mean for total expenditure in a year
print("The mean for total expenditure in a year {}".format(df['expenditure'].mean()))

# mean for number of conflicts per year
print("The mean for total conflict per year is {}".format(df['conflict'].mean()))

#plt.plot(df['expenditure'].mean(), df['conflict'].mean(), marker = 'o', markerfacecolor='yellow')


print("\n")

print("The median for total expenditure in a year is {}".format(df['expenditure'].median()))

print("The median for total conflicts in a year is {}".format(df['conflict'].median()))

#plt.plot(df['expenditure'].median(), df['conflict'].mean(), marker = 'o', markerfacecolor = 'green')


# k means clustering to find what is deemed as low, medium and high levels of expenditure
# or i could just do percentiles

print(df.describe())


#sns.pairplot(df[['years','expenditure','conflict']])
#plt.savefig("pairplot.png") #saved
#plt.show()

kmeans = cluster.KMeans(n_clusters=3, init='k-means++')
kmeans = kmeans.fit(df[['expenditure', 'conflict']])

#print("K-means cluster centres = {}".format(kmeans.cluster_centers_))


#add clusters to original data

#automatically assigns to relevant clustern
df['clusters'] = kmeans.labels_

print(df['clusters'].value_counts())



#export data with clusters
#df.to_csv('milex-conflict-clusters.csv', index=False)

sns.scatterplot(x='expenditure', y='conflict', hue='clusters', data = df)
plt.savefig('milex-conflict-clusters.png')
plt.show()

# adjusting the dataframe to account for 'war prep'


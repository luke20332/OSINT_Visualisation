import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

# conflicts from 1946-2018
# expenditure from 1946-2018
# Read the data
conflict = pd.read_csv('OSINT_Visualisation\conflicts\\prio_df.csv', header=0)
expenditure = pd.read_csv('OSINT_Visualisation\conflicts\\data.csv', header=0)

print(conflict)
# find earliest year of expenditure
print(expenditure.columns[1])
print(expenditure.columns[-1])

# Drop the first row
conflict = conflict.drop(conflict.index[0])
expenditure = expenditure.drop(expenditure.index[0])

# first conflict was in 1946 so only include data from 1946 onwards
conflict = conflict[conflict['year'] >= 1946]

# last conflict was in 2018 so only include data from 2018 onwards
conflict = conflict[conflict['year'] <= 2018]



# total military expenditure for per country
total_mil_exp = expenditure.sum(axis=1)
total_mil_exp = pd.DataFrame(total_mil_exp)
total_mil_exp['Country'] = expenditure['Country']
total_mil_exp.rename(columns={0: 'Total Military Expenditure'}, inplace=True)

# It is quite difficult to merge the two dataframes in terms of country names
# In the conflict dataframe, the country names are in the form of 'Country (ISO3)'
# In the expenditure dataframe, the country names are in the form of 'Country (ISO2)'
# Therefore, we need to extract the ISO2 code from the conflict dataframe
# and then merge the two dataframes based on the ISO2 code
conflict['ISO2'] = conflict['side_a'].str.extract(r'\((\w+)\)')
conflict = conflict.drop(['side_a'], axis=1)
conflict = conflict.rename(columns={'ISO2': 'Country'})
# print(conflict.head())

# Number of conflicts per country
num_conflicts = conflict.groupby('Country')['conflict_id'].count()
num_conflicts = pd.DataFrame(num_conflicts)
num_conflicts = num_conflicts.rename(columns={'conflict_id': 'Number of Conflicts'})


# number of conflicts per location
num_conflicts_location = conflict.groupby('location')['conflict_id'].count()
num_conflicts_location = pd.DataFrame(num_conflicts_location)
num_conflicts_location = num_conflicts_location.rename(columns={'conflict_id': 'Number of Conflicts'})

num_conflicts_location = num_conflicts_location.sort_values(by='Number of Conflicts')


# When location has multiple countries, countries must be separated and added to the dataframe
for index, row in num_conflicts_location.iterrows():
    if ',' in index:
        countries = index.split(',')
        for country in countries:
            country = country.strip()
            if country in num_conflicts_location.index:
                num_conflicts_location.loc[country] = num_conflicts_location.loc[country] + row
            else:
                num_conflicts_location.loc[country] = row
    else:
        if index in num_conflicts_location.index:
            num_conflicts_location.loc[index] = num_conflicts_location.loc[index] + row
        else:
            num_conflicts_location.loc[index] = row

# now i can remove the rows that have multiple countries 
for location in num_conflicts_location.index:
    if ',' in location:
        num_conflicts_location = num_conflicts_location.drop(location)

# sort in ascending order
num_conflicts_location = num_conflicts_location.sort_values(by='Number of Conflicts')

print(num_conflicts_location.sort_values(by='Number of Conflicts', ascending=False).head(10))

# checking if mil_exp and num_conflicts have the same countries
print(len(num_conflicts_location.index))
print(len(total_mil_exp['Country']))


# adding another feature to the dataframe
# total military expenditure per country
total_mil_exp = total_mil_exp.set_index('Country')
num_conflicts_location = num_conflicts_location.join(total_mil_exp)
num_conflicts_location = num_conflicts_location.dropna()
num_conflicts_location['Total Military Expenditure'] = num_conflicts_location['Total Military Expenditure'].astype(float)
num_conflicts_location['Total Military Expenditure'] = num_conflicts_location['Total Military Expenditure'].astype(int)

merged = num_conflicts_location

# first instance of a country having a conflict
first_conflict = conflict.groupby('Country')['year'].min()
first_conflict = pd.DataFrame(first_conflict)
first_conflict = first_conflict.rename(columns={'year': 'First Conflict'})

# arrange the dataframe in descending order of number of conflicts
merged = merged.sort_values(by='Number of Conflicts', ascending=False)


# Despite myanmar having the most conflicts, it is missing from merged dataframe

# is myanmar/burma in the conflict dataframe?
print('Myanmar' in conflict['Country'].values)
print('Burma' in conflict['Country'].values)

# is myanmar/burma in the expenditure dataframe?
print('Myanmar' in total_mil_exp.index.values)
print('Burma' in total_mil_exp.index.values)

# find myanmar in expenditure dataframe and its total military expenditure
for country in total_mil_exp.index.values:
    if 'Myanmar' in country:
        print(country)
        print(total_mil_exp.loc[country])

# Myanmar (Burma) has a total military expenditure of 1.5 billion

# myanmar/burma are in both datasets under different names, could not be formatted
# to the same name. Therefore it was lost in the merging process

# since myanmar has the most conflicts, we will add it manually
# from previous dataframes we know that myanmar has 573 conflicts/involvements in total

# Myanmar total expenditure = 55991.463495
# Myanmar total conflicts = 555

# add myanmar to the dataframe
merged.loc['Myanmar'] = [555, 55991.463495]

# sort in descending order of number of conflicts
merged = merged.sort_values(by='Number of Conflicts', ascending=False)

# I can now perform some analysis on the data
# I will be using the merged dataframe

# Scatter plot of number of conflicts vs total military expenditure

plt.scatter(np.log(merged['Total Military Expenditure']), merged['Number of Conflicts'])
plt.xlabel('Total Military Expenditure')
plt.ylabel('Number of Conflicts')
plt.title('Number of Conflicts vs Total Military Expenditure')
plt.show()

# Machine Learning
# I will be using the merged dataframe to predict the number of conflicts
# based on the total military expenditure

# Linear Regression
# import libraries

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# split the data into training and testing data
X = merged['Total Military Expenditure'].values.reshape(-1, 1)
y = merged['Number of Conflicts'].values.reshape(-1, 1)

# normalise the data
X = X / X.max()
y = y / y.max()


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# train the model
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# make predictions
y_pred = regressor.predict(X_test)

# plot the predictions
plt.scatter(X_test, y_test, color='red')
plt.plot(X_test, y_pred, color='blue')
plt.title('Number of Conflicts vs Total Military Expenditure')
plt.xlabel('Total Military Expenditure')
plt.ylabel('Number of Conflicts')
plt.show()

# The linear regression model is not very accurate
# The model is not able to predict the number of conflicts accurately
# This gives us an indication that the number of conflicts is not dependent on the total military expenditure

# checkin the accuracy of the model
from sklearn import metrics
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

# However, the model is able to predict the number of conflicts accurately
# when the total military expenditure is less than 10000
# This gives us an indication that the number of conflicts is dependent on the total military expenditure
# but only when the total military expenditure is less than 10000
# But this is not a very useful model as it is not able to predict the number of conflicts accurately
# when the total military expenditure is greater than 10000

# Is there a correlation between the number of conflicts and the total military expenditure?
# I will be using the merged dataframe to find out

# import libraries
import seaborn as sns

# plot the data using normalised values for better visualisation
sns.regplot(x=merged['Total Military Expenditure'] / merged['Total Military Expenditure'].max(), y=merged['Number of Conflicts'] / merged['Number of Conflicts'].max())
plt.title('Number of Conflicts vs Total Military Expenditure')
plt.xlabel('Total Military Expenditure')
plt.ylabel('Number of Conflicts')
plt.show()

# log plot of the data
sns.regplot(x=np.log(merged['Total Military Expenditure']), y=merged['Number of Conflicts'])
plt.title('Number of Conflicts vs Total Military Expenditure')
plt.xlabel('Total Military Expenditure')
plt.ylabel('Number of Conflicts')
plt.show()

# The data is not linearly correlated
# The data is not correlated at all


# K means clustering - With Elbow Method
# import libraries
from sklearn.cluster import KMeans
k = range(1, 10)


distortions = []

for k in k:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(merged[['Total Military Expenditure', 'Number of Conflicts']])
    distortions.append(kmeans.inertia_)

print(distortions)
print(k)
k_values = range(1, 10)

# plot the elbow graph
plt.plot(k_values, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()

# Based on the elbow graph, the optimal k is 2 or 3

# For further evidence, I will be using the silhouette score

# import libraries
from sklearn.metrics import silhouette_score

# silhouette score for all values of k stored in a list
sil_score = []

for k in range(2, 10):
    print(k)
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(merged[['Total Military Expenditure', 'Number of Conflicts']])
    sil_score.append(silhouette_score(merged[['Total Military Expenditure', 'Number of Conflicts']], kmeans.labels_))

print(sil_score)

# Silhouette score suggests that the optimal k is 2

# There may be more features that can be used to predict the number of conflicts

# Kmeans clustering with k = 2
kmeans = KMeans(n_clusters=2)
kmeans.fit(merged[['Total Military Expenditure', 'Number of Conflicts']])
labels = kmeans.labels_

# plot the clusters
plt.scatter(np.log(merged['Total Military Expenditure']), merged['Number of Conflicts'], c=labels)
plt.xlabel('Total Military Expenditure')
plt.ylabel('Number of Conflicts')
plt.title('Number of Conflicts vs Total Military Expenditure')
plt.show()

# Even with the optimal k, the clusters are not very distinct and the model does not reveal any useful information
# The model is not able to predict the number of conflicts accurately
# This gives us an indication that the number of conflicts may not be dependent on the total military expenditure
# 
# Can I merge the data with other datasets to get more features? 

# export the data to a csv file
# merged.to_csv('merged.csv')

# This has just been a basic analysis of the data on only two features
# I have now added more features to the dataset and will be performing more analysis on it
# Will try to merge the data with other datasets to get more features

# Spent too long trying to find a 
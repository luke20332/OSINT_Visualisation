import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the data
conflict = pd.read_csv('OSINT_Visualisation\conflicts\\prio_df.csv', header=0)
expenditure = pd.read_csv('OSINT_Visualisation\conflicts\\data.csv', header=0)


# Drop the first row
conflict = conflict.drop(conflict.index[0])
expenditure = expenditure.drop(expenditure.index[0])
# print(expenditure.head())
# print(conflict.head())


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
# print(num_conflicts.head())


# number of conflicts per location
num_conflicts_location = conflict.groupby('location')['conflict_id'].count()
num_conflicts_location = pd.DataFrame(num_conflicts_location)
num_conflicts_location = num_conflicts_location.rename(columns={'conflict_id': 'Number of Conflicts'})

num_conflicts_location = num_conflicts_location.sort_values(by='Number of Conflicts')

# print(num_conflicts_location.index)
# print(num_conflicts_location.loc['Cyprus'])

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

# print(num_conflicts_location.head())

# Plot the number of conflicts per location
# plt.figure(figsize=(20, 10))
# plt.title('Number of Conflicts per Location')
# plt.xlabel('Location')
# plt.ylabel('Number of Conflicts')
# plt.xticks(rotation=90)
# plt.bar(num_conflicts_location.index, num_conflicts_location['Number of Conflicts'])
# plt.show()

# Kmeans clustering
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
# drop the country column
df_kmean = num_conflicts_location.reset_index()
df_kmean = df_kmean.drop(['location'], axis=1)

X = np.array(df_kmean['Number of Conflicts'])
# standardise the data
scaler = StandardScaler()
num_conflicts_location_scaled = scaler.fit_transform(X.reshape(-1, 1))

# fit the data to the kmeans model
kmeans = KMeans(n_clusters=3)
kmeans.fit(num_conflicts_location_scaled)

# add the cluster labels to the dataframe
num_conflicts_location['Cluster'] = kmeans.labels_

print(num_conflicts_location.head())

# plot the clusters with seaborn
# plt.figure(figsize=(20, 10))
# plt.title('Number of Conflicts per Location')
# plt.xlabel('Location')
# plt.ylabel('Number of Conflicts')
# plt.xticks(rotation=90)
# sns.barplot(x=num_conflicts_location.index, y=num_conflicts_location['Number of Conflicts'], hue=num_conflicts_location['Cluster'])
# plt.show()

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
print(num_conflicts_location.loc['United States of America'])











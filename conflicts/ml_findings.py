import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the data
conflict = pd.read_csv('OSINT_Visualisation\conflicts\\prio_df.csv', header=0)
expenditure = pd.read_csv('OSINT_Visualisation\conflicts\\data.csv', header=0)


# Drop the first row
conflict = conflict.drop(conflict.index[0])
expenditure = expenditure.drop(expenditure.index[0])
print(expenditure.head())
print(conflict.head())


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
print(conflict.head())

# Number of conflicts per country
num_conflicts = conflict.groupby('Country')['conflict_id'].count()
num_conflicts = pd.DataFrame(num_conflicts)
num_conflicts = num_conflicts.rename(columns={'conflict_id': 'Number of Conflicts'})
print(num_conflicts.head())

# Check the overlap of countries in the two dataframes
print(set(conflict['Country']).intersection(set(expenditure['Country'])))

# number of conflicts per location
num_conflicts_location = conflict.groupby('location')['conflict_id'].count()
num_conflicts_location = pd.DataFrame(num_conflicts_location)
num_conflicts_location = num_conflicts_location.rename(columns={'conflict_id': 'Number of Conflicts'})
print(num_conflicts_location.head())










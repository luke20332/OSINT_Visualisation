import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import polars as pl
from pathlib import Path

# Read the data
data = pd.read_excel('OSINT_Visualisation\conflicts\SIPRI-Milex-data-1949-2022.xlsx', sheet_name='Constant (2021) US$', index_col=0, header=5)
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
prio_df = pd.read_csv('OSINT_Visualisation\conflicts\\ucdp-prio-acd-221.csv', header=0)

# Filtering UCDP data
print(data.head())
print(prio_df.head())
# remove unnecessary columns
remove_columns = ['incompatibility', 'territory_name', 'cumulative_intensity', 'type_of_conflict','start_date', 
        'start_prec', 'start_date2', 'start_prec2', 'ep_end',
       'ep_end_date', 'ep_end_prec', 'gwno_a', 'gwno_a_2nd', 'gwno_b',
       'gwno_b_2nd', 'gwno_loc', 'region', 'version']

prio_df = prio_df.drop(remove_columns, axis=1)


# total military expenditure for each country
total_mil_exp = data.sum(axis=1)
total_mil_exp = total_mil_exp.sort_values(ascending=False)

# Plotting the data
plt.figure(figsize=(20,10))
sns.barplot(x=total_mil_exp.index, y=total_mil_exp.values)
plt.title('Total Military Expenditure by Country')
plt.xlabel('Country')
plt.ylabel('Total Military Expenditure')
plt.xticks(rotation=90)
plt.show()

# total military expenditure for each year
total_mil_exp_year = data.sum(axis=0)
total_mil_exp_year = total_mil_exp_year.sort_values(ascending=False)

# Plotting the data
plt.figure(figsize=(20,10))
sns.barplot(x=total_mil_exp_year.index, y=total_mil_exp_year.values)
plt.title('Total Military Expenditure by Year')
plt.xlabel('Year')
plt.ylabel('Total Military Expenditure')
plt.xticks(rotation=90)
plt.show()

# ucdp average intensity per country
ucdp_avg_intensity = prio_df.groupby('side_a')['intensity_level'].mean()
print(ucdp_avg_intensity.head())
ucdp_avg_intensity = ucdp_avg_intensity.sort_values(ascending=False)

# Plotting the data
plt.figure(figsize=(20,10))
sns.barplot(x=ucdp_avg_intensity.index, y=ucdp_avg_intensity.values)
plt.title('Average Intensity Level by Country')
plt.xlabel('Country')
plt.ylabel('Average Intensity Level')
plt.xticks(rotation=90)
plt.show()

# UCDP number of conflicts per country
ucdp_num_conflicts = prio_df.groupby('side_a')['conflict_id'].count()
ucdp_num_conflicts = ucdp_num_conflicts.sort_values(ascending=False)

# Plotting the data
plt.figure(figsize=(20,10))
sns.barplot(x=ucdp_num_conflicts.index, y=ucdp_num_conflicts.values)
plt.title('Number of Conflicts by Country')
plt.xlabel('Country')
plt.ylabel('Number of Conflicts')
plt.xticks(rotation=90)
plt.show()



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
print(ucdp_num_conflicts_year.values[4:]) # yearly number of conflicts from 1950 onwards

df["conflict"] = ucdp_num_conflicts_year.values[3:]

print(df.head)

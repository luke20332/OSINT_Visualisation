#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import polars as pl
from pathlib import Path

# Read the data
data = pd.read_excel('SIPRI-Milex-data-1949-2022.xlsx', sheet_name='Constant (2021) US$', index_col=0, header=5)
data = data.drop(['Unnamed: 1', 'Notes'], axis=1)

# Unused index names:
extra_index = ['Africa', 'North Africa','sub-Saharan Africa','Americas','Central America and the Caribbean',
'North America', 'South America','Asia & Oceania', 'Oceania','South Asia', 'East Asia','South East Asia','Central Asia',
'Europe','Eastern Europe','Western Europe','Middle East']

data = data.drop(extra_index, axis=0)
data = data.drop(data.iloc[0])

data = data.fillna(-1)
print(data)
#%%
# Read the data
prio_df = pd.read_csv('ucdp-prio-acd-221.csv', index_col=0)
print(prio_df.head())
# %%


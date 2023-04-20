# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 17:53:36 2023

@author: pablo

"""

import networkx as nx
import numpy as np
import itertools
import pandas as pd
from sklearn.model_selection import ParameterGrid
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms import community
import matplotlib.pyplot as plt

cv=pd.read_csv("WeaponsData.txt",delimiter=";")

source=[]

pr=cv.iloc[:,1]
source = []
target=[]
for i in range(0,len(cv)):
    source_list = cv.iloc[i, 1].split(',')
    target_list = cv.iloc[i, 2].split(',')
    source_str = ','.join(source_list)
    target_str= ','.join(target_list)  
    source.append(source_str)
    target.append(target_str) 

result = cv[(cv['Seller'] == 'United States') & (cv['Buyer'] == 'Saudi Arabia')]
    

linkData = pd.DataFrame({'source': source, 'target': target, "weight":cv.iloc[:,-2]})
                  #'weight' : [cv.iloc[:,-2]]})


G = nx.from_pandas_edgelist(linkData, 'source', 'target', True, nx.MultiDiGraph())

#calculating graph parameters
density=nx.density(G)
degree=G.degree()
degree_list=[]

for (n,d) in degree:
    degree_list.append(d)

avrg_degree=sum(degree_list)/len(degree_list)







#GRID SEARCH
param_grid = {
    'weight': [0.5,1,2, 3, 4, 5,6,7],#The name of an edge attribute that holds the numerical value used as a weight
    'resolution': [0.1, 0.5, 1.0, 2.0,3.0,4.0],#if res<1 modularity favours bigger communities
    #'cu': [1, 1.5, 2.0,2.5,3], #minimum number of communities below which the merging process stops
    #'bn': [3,5,10,100],# A maximum number of communities above which the merging process will not stop
    
}

# Generate all combinations of hyperparameters
params = list(ParameterGrid(param_grid))

# Define graph G
G = nx.from_pandas_edgelist(linkData, 'source', 'target', True, nx.MultiDiGraph())

# Define empty lists to store results
modularities = []
num_communities = []

# Loop over all combinations of hyperparameters
for p in params:
    # Get communities using greedy_modularity_communities
    communities = list(nx.algorithms.community.greedy_modularity_communities(G, p['weight'], p['resolution']))
    num_communities.append(len(communities))
    # Calculate modularity of communities
    modularities.append(community.modularity(G, communities))

best_idx = np.argmax(modularities)
best_params = params[best_idx]
best_modularity = modularities[best_idx]
best_num_communities = num_communities[best_idx]

print('Best hyperparameters:', best_params)
print('Best modularity:', best_modularity)
    
communities1 = list(greedy_modularity_communities(G,1,0.5))#res can be changed to vary the size of the communities
for i, comm in enumerate(communities1):
    print(f"Community {i}: {', '.join([str(node) for node in comm])}")
    
# Compute the modularity score
# Modularity is the quality of community structure
modularity_score = nx.algorithms.community.modularity(G, communities1)

print(f"Modularity score: {modularity_score}")



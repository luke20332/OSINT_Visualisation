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
from networkx.algorithms.community.centrality import girvan_newman
from networkx.algorithms import community
import matplotlib.pyplot as plt
import infomap
from networkx.algorithms.community import modularity
from cdlib import algorithms
# import wurlitzer
# from cdlib import NodeClustering

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
    
weight=cv.iloc[:,-2]


    

result = cv[(cv['Seller'] == 'United States') & (cv['Buyer'] == 'Saudi Arabia')]
    
linkData = pd.DataFrame({'source': source, 'target': target, "weight":weight})

                  #'weight' : [cv.iloc[:,-2]]})
                  
G = nx.from_pandas_edgelist(linkData, 'source', 'target', True, nx.MultiDiGraph())

G = G.to_undirected()



#calculating graph parameters
density=nx.density(G)
degree=G.degree()
degree_list=[]

for (n,d) in degree:
    degree_list.append(d)

avrg_degree=sum(degree_list)/len(degree_list)


# #GRID SEARCH
# param_grid = {
#     'weight': ["weight"],
#     #'weight': [0.5,1,2, 3, 4, 5,6,7],#The name of an edge attribute that holds the numerical value used as a weight
#     'resolution': [0.1, 0.5, 1.0, 2.0,3.0,4.0],#if res<1 modularity favours bigger communities
#     #'cu': [1, 1.5, 2.0,2.5,3], #minimum number of communities below which the merging process stops
#     #'bn': [3,5,10,100],# A maximum number of communities above which the merging process will not stop
    
# }

# # Generate all combinations of hyperparameters
# params = list(ParameterGrid(param_grid))

# # Define graph G
# G = nx.from_pandas_edgelist(linkData, 'source', 'target', True, nx.MultiDiGraph())

# # Define empty lists to store results
# modularities = []
# num_communities = []

# # Loop over all combinations of hyperparameters
# for p in params:
#     # Get communities using greedy_modularity_communities
#     communities = list(nx.algorithms.community.greedy_modularity_communities(G, p['weight'], p['resolution']))
#     num_communities.append(len(communities))
#     # Calculate modularity of communities
#     modularities.append(community.modularity(G, communities))

# best_idx = np.argmax(modularities)
# best_params = params[best_idx]
# best_modularity = modularities[best_idx]
# best_num_communities = num_communities[best_idx]

# print('Best hyperparameters:', best_params)
# print('Best modularity:', best_modularity)



# find the nodes forming the communities

        
        


communities1 = list(nx.algorithms.community.greedy_modularity_communities(G,weight="weight",resolution=1))#res can be changed to vary the size of the communities
for i, comm in enumerate(communities1):
    size= len(comm)
    print(f"Community {i+1} (size {size}): {', '.join([str(node) for node in comm])}")
    

num_sellers_per_community = []
total_weight_by_country = {}
num_sellers_list=[]

# Loop over every community and calculate total weight and number of sellers
for community in communities1:
    # Reset the total weight by country for this community
    total_weight_by_country_community = {}

    # Reset the number of sellers for this community
    num_sellers = 0

    for node in community:
        is_seller = linkData['source'] == node

        if is_seller.any():
            num_sellers += 1
            total_weight = linkData[is_seller]['weight'].sum()

            total_weight_by_country_community[node] = total_weight
            
    for country, total_weight in total_weight_by_country_community.items():
        if country in total_weight_by_country:
            total_weight_by_country[country] += total_weight
        else:
            total_weight_by_country[country] = total_weight

    if num_sellers > 0:
        average_weight_per_seller = sum(total_weight_by_country_community.values()) / num_sellers
        num_sellers_list.append(average_weight_per_seller)
        print(f"Average number of sold weapons per seller in community {communities1.index(community) + 1}: {average_weight_per_seller}")


x = range(1, len(num_sellers_list) + 1)  
y = num_sellers_list 

fig, ax = plt.subplots()
ax.bar(x, y)

ax.set_xlabel('Community')
ax.set_ylabel('Average value of total sold weapons per country')

plt.show()
modularity_score = nx.algorithms.community.modularity(G, communities1)



print(f"Modularity score: {modularity_score}")

xyt=[0.2,0.2,20]
xy=xyt[:2]
t0=0
t1 = xyt[-1]
prms=[1,0.2,0.1]





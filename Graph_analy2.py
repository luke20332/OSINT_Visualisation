# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 13:08:44 2023

@author: pablo
"""

import networkx as nx
import numpy as np
import community
import itertools
import pandas as pd
from sklearn.model_selection import ParameterGrid
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms import community
from networkx.algorithms.community.quality import modularity
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

selected_edges = {}

nodes=list(G.nodes())


G = G.to_undirected()      

_adj = nx.to_numpy_array(G, weight='weight')

#Creating a new graph with only the Highest value edge between each node

H = nx.Graph()
for node in G.nodes():
    H.add_node(node)
for edge in G.edges(data=True):
    node1, node2, weight = edge
    if H.has_edge(node1, node2):
        current_weight = H[node1][node2]['weight']
        if weight['weight'] > current_weight:
            H[node1][node2]['weight'] = weight['weight']
    else:
        H.add_edge(node1, node2, weight=weight['weight'])
        
        
        

#Running the Louvain algorithm for n times
best_mod_1=-1
for i in range(5000):  # run Louvain algorithm n times
    partition = nx.community.louvain_communities(H,weight="weight")
    modularity_value = nx.algorithms.community.modularity(H,partition)
    if modularity_value > best_mod_1:
        best_partition_1 = partition
        best_mod_1 = modularity_value
        print(best_mod_1)
        
    
communities1 = list(nx.algorithms.community.greedy_modularity_communities(H,weight="weight",resolution=1))#res can be changed to vary the size of the communities
for i, comm in enumerate(communities1):
    print(f"Community {i}: {', '.join([str(node) for node in comm])}")
    
modularity_score = nx.algorithms.community.modularity(G, communities1)



print(f"Modularity score: {modularity_score}")
        
total_weight_by_country = {}

    
num_sellers_per_community = []
total_weight_by_country = {}
num_sellers_list=[]

# Loop over every community and calculate total weight and number of sellers
for community in best_partition_1:
    
    total_weight_by_country_community = {}
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
        print(f"Average number of sold weapons per seller in community {best_partition_1.index(community) + 1}: {average_weight_per_seller}")
        
x = range(1, len(num_sellers_list) + 1)  
y = num_sellers_list 

fig, ax = plt.subplots()
ax.bar(x, y)

ax.set_xlabel('Community')
ax.set_ylabel('Average value of total sold weapons per country')

plt.show()

comms = list(best_partition_1)
for i, comm in enumerate(comms):
   print(f"Community {i+1}: {', '.join([str(node) for node in comm])}")


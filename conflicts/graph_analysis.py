# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 17:53:36 2023

@author: pablo

"""

import networkx as nx
import pandas as pd
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms import community
import matplotlib.pyplot as plt

cv=pd.read_csv("OSINT_Visualisation\\conflicts\\WeaponsData.txt",delimiter=";")

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
    

#print(source)

#for i in range(0,len(cv)):
    #source=[source;cv(i,1)]


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


F=G.degree("Belgium")
# communities1=list(greedy_modularity_communities(G))
# communities2 = list(community.girvan_newman(G))
# communities3 = list(community.label_propagation_communities(G))


#for i, comm in enumerate(communities):
    #print(f"Community {i}: {', '.join([str(node) for node in comm])}")
#nx.draw(G,with_labels=True)

#nx.set_node_attributes(G, nodeData.set_index('name').to_dict('index'))
#################################################################################################################
# Drawing the graph for sanity check
# nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_color='grey', width=0.5, alpha=0.8)
# plt.show()

# Calculating centrality measures
deg_centrality = nx.degree_centrality(G)
close_centrality = nx.closeness_centrality(G)
betw_centrality = nx.betweenness_centrality(G)
# Eigenvector centrality is a measure of the influence of a node in a network.
# Not available for directed graphs...
# eigen_centrality = nx.eigenvector_centrality(G)

# Picking out the top 10 nodes for each centrality measure
top_deg = sorted(deg_centrality.items(), key=lambda x:x[1], reverse=True)[0:10]
top_close = sorted(close_centrality.items(), key=lambda x:x[1], reverse=True)[0:10]
top_betw = sorted(betw_centrality.items(), key=lambda x:x[1], reverse=True)[0:10]


# Bottom 10:
bottom_deg = sorted(deg_centrality.items(), key=lambda x:x[1], reverse=False)[0:10]
bottom_close = sorted(close_centrality.items(), key=lambda x:x[1], reverse=False)[0:10]
bottom_betw = sorted(betw_centrality.items(), key=lambda x:x[1], reverse=False)[0:10]

# Plotting results 
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.bar([x[0] for x in top_deg], [x[1] for x in top_deg], color='skyblue')
plt.title('Top 10 nodes by degree centrality')
plt.xticks(rotation=90)
plt.subplot(1, 3, 2)
plt.bar([x[0] for x in top_close], [x[1] for x in top_close], color='skyblue')
plt.title('Top 10 nodes by closeness centrality')
plt.xticks(rotation=90)
plt.subplot(1, 3, 3)
plt.bar([x[0] for x in top_betw], [x[1] for x in top_betw], color='skyblue')
plt.title('Top 10 nodes by betweenness centrality')
plt.xticks(rotation=90)
plt.show()

plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.bar([x[0] for x in bottom_deg], [x[1] for x in bottom_deg], color='skyblue')
plt.title('Bottom 10 nodes by degree centrality')
plt.xticks(rotation=90)
plt.subplot(1, 3, 2)
plt.bar([x[0] for x in bottom_close], [x[1] for x in bottom_close], color='skyblue')
plt.title('Bottom 10 nodes by closeness centrality')
plt.xticks(rotation=90)
plt.subplot(1, 3, 3)
plt.bar([x[0] for x in bottom_betw], [x[1] for x in bottom_betw], color='skyblue')
plt.title('Bottom 10 nodes by betweenness centrality')
plt.xticks(rotation=90)
plt.show()


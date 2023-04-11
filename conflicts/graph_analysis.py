# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 17:53:36 2023

@author: pablo

"""

import networkx as nx
import pandas as pd
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms import community

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
communities1=list(greedy_modularity_communities(G))
#communities2 = list(community.girvan_newman(G))
communities3 = list(community.label_propagation_communities(G))


#for i, comm in enumerate(communities):
    #print(f"Community {i}: {', '.join([str(node) for node in comm])}")
#nx.draw(G,with_labels=True)

#nx.set_node_attributes(G, nodeData.set_index('name').to_dict('index'))



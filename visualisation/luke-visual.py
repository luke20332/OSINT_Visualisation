# some attempts at visualisation of the data

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import csv
import seaborn as sb


from scipy.stats import multivariate_normal    

import imageio.v3 as iio

buyers = {}
sellers = {}
counter = 0



with open("numerical_data\joined_data_numeric.csv", newline = '') as transferFile:
    fileReader = csv.reader(transferFile, delimiter = ' ', quotechar= '|')
    headers = next(fileReader)
    for row in fileReader:

        x = ",".join(row) # converts the list into a string
        x = x.split(',')
        
        if x[2] not in buyers:  # x[2] is the buyer
            buyers[x[2]] = int(x[8])
        if x[2] in buyers:
            buyers[x[2]] = buyers[x[2]] + int(x[8])
        
        if x[1] not in sellers:
            sellers[x[1]] = int(x[8])
        if x[1] in sellers:
            sellers[x[1]] = sellers[x[1]] + int(x[8])


        #else:
        #    break

topBuyers = sorted(buyers, key=buyers.get, reverse=True)[:10]

#topBuyers.replace("United-States", "USA")
#topBuyers.replace("Saudi-Arabia", "S.Arabia")
#topBuyers.replace("East-Germany-(GDR)", "E.Germany")
print(topBuyers)

buyerQuantity = []

for i,x in enumerate(topBuyers):
    buyerQuantity.append(buyers[x])


topBuyers = list(map(lambda x: x.replace('United-Kingdom', 'UK'), topBuyers))
topBuyers = list(map(lambda x: x.replace('United-States', 'USA'), topBuyers))
topBuyers = list(map(lambda x: x.replace('Saudi-Arabia', 'S.Arabia'), topBuyers))
topBuyers = list(map(lambda x: x.replace('East-Germany-(GDR)', 'E.Germany'), topBuyers))

fig = plt.figure(figsize=(20,10))
sb.barplot(x=topBuyers, y=buyerQuantity)
plt.title("Top 10 Buyers")
plt.xlabel("Buyers")
plt.ylabel("Total items purchased")
plt.xticks(rotation=90)
plt.show()
#Biggest Buyers


topSellers = sorted(sellers, key=sellers.get, reverse=True)[:10]
print(topSellers)
sellerQuantity = []

for i,x in enumerate(topSellers):
    sellerQuantity.append(sellers[x])
topSellers = list(map(lambda x: x.replace('United-Kingdom', 'UK'), topSellers))
topSellers = list(map(lambda x: x.replace('United-States', 'USA'), topSellers))
topSellers = list(map(lambda x: x.replace('Soviet-Union', 'USSR'), topSellers))


fig = plt.figure(figsize=(20,10))
sb.barplot(x=topSellers, y=sellerQuantity)
plt.title("Top 10 Sellers")
plt.xlabel("Sellers")
plt.ylabel("Total items sold (Million)")
plt.xticks(rotation=90)
plt.show()


# may have to check if country is a double barrel name (united  x, soviet union, north x)

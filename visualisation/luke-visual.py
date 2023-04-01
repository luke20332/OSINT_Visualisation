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
        x = x.split(',')   # x is a list representing the entries in the row
       
        if x[2] not in buyers:  # x[2] is the buyer
            buyers[x[2]] = int(x[8])
            
        elif x[2] in buyers:
            buyers[x[2]] = buyers[x[2]] + int(x[8])
        
        
        if x[1] not in sellers:
            sellers[x[1]] = int(x[8])
        elif x[1] in sellers:
            sellers[x[1]] = sellers[x[1]] + int(x[8])
        
        
        #else:
        #    break


topBuyers = sorted(buyers, key=buyers.get, reverse=True)[:10]

#print(topBuyers)

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
plt.savefig("visualisation/Top-10-buyers.jpg")
#plt.show()

#Biggest Buyers


topSellers = sorted(sellers, key=sellers.get, reverse=True)[:10]
#print(topSellers)
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
plt.savefig("visualisation/Top-10-Sellers.jpg")
#plt.show()


# top buyers and sellers for each decade
"""
before make a list of dictionaries with a loop
in the csv reader loop

convert year to appropriate decade
make a buyers dictionary for each decade and add the country and amount sold
- Kinda hard


Simpler approach - very time and resource intensive
for loop for all decades
convert year to its decade
read csv file
make a dictionary of the top buyers of that decade
return the most common or top 3 of each decade
make a tuple of country and decade
"""

buyersDecades = []
sellersDecades = []

for i in range(5,13):
    decadeDict = {}
    with open("numerical_data\joined_data_numeric.csv", newline = '') as transferFile:
        fileReader = csv.reader(transferFile, delimiter = ' ', quotechar= '|')
        headers = next(fileReader)
        for row in fileReader:

            x = ",".join(row) # converts the list into a string
            x = x.split(',')

            if x[10][2] == str(i)[-1]: #year correlation
                if x[1] not in decadeDict:
                    decadeDict[x[1]] = int(x[8])
                else:
                    decadeDict[x[1]] += int(x[8])
        
        sellersDecades.append(decadeDict)


# 0th index is 50s 5th is noughties

"""
topBuyersOfDecades = []

for i,x in enumerate(buyersDecades):
    topBuyersOfDecades.append(sorted(buyersDecades[i], key=buyersDecades[i].get, reverse=True)[:1])

topBuyersOfDecades = [''.join(ele) for ele in topBuyersOfDecades]
print(topBuyersOfDecades)

file_object = open("visualisation/stats.txt", "a")
file_object.write("top buyers by decade")

for i,x in enumerate(topBuyersOfDecades):
    file_object.write("\n")
    file_object.write(x)

file_object.close()

"""

topSellersOfDecades = []

for i,x in enumerate(sellersDecades):
    topSellersOfDecades.append(sorted(sellersDecades[i], key=sellersDecades[i].get, reverse=True)[:1])

topSellersOfDecades = [''.join(ele) for ele in topSellersOfDecades]
print(topSellersOfDecades)

file_object = open("visualisation/stats.txt", "a")
file_object.write("top sellers by decade")

for i,x in enumerate(topSellersOfDecades):
    file_object.write("\n")
    file_object.write(x)

file_object.close()

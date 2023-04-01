import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import sklearn
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.svm import SVC
from sklearn.datasets import make_moons

import h5py
import imageio
from PIL import Image 
#from utils import *

milexcel_uk = 'visualisation/milex-uk.xlsx'
milexcel_uk_pound = 'visualisation/milex-uk-pound.xlsx'
milexcel = 'visualisation/milex.xlsx'

milexcel_df = pd.read_excel(milexcel)

df = pd.read_excel(milexcel_uk_pound)
df = df.dropna(axis = 0) # remove empty rows
print(df)

new_dict = df.to_dict(orient='list') # preliminary form of dictionary


# records may be the best
# or maybe list

cleaned_dict = {}

#clean the dictionary
for x in new_dict.values():
    if x[0] == 'Country' or x[0] == 'Currency' or x[0] == 'Notes' or x[1] == '...':
        continue
    else:
       cleaned_dict[int(x[0])] = int(x[1])

# plot the points - expenditure as a function of time

fig, ax = plt.subplots(figsize=(6,4))
#fig = plt.figure(figsize=(20,10))
ax.scatter(cleaned_dict.keys(), cleaned_dict.values())
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()


# time for some linear regression baby - doesnt work

"""
x_bias = np.concatenate((np.ones(len(cleaned_dict)).reshape(-1,1), cleaned_dict.keys()), axis=1)

w_fit = np.linalg.lstsq(x_bias, cleaned_dict.values(), rcond=None)[0]

y_pred = np.dot(x_bias, w_fit)

print("w_1 = {:.2f}".format(w_fit[1].item()))
print("b = {:.2f}".format(w_fit[0].item()))

fig, ax = plt.subplots(figsize=(6,4))
ax.scatter(cleaned_dict.keys(), cleaned_dict.values())
ax.plot(x, y_pred, '-r')
ax.set_xlabel('x')
ax.set_ylabel('y')
"""

# polynomial regression

poly = PolynomialFeatures(degree=2)
x_poly = poly.fit


print(cleaned_dict)


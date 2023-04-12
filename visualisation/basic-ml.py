import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import sklearn
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neural_network import MLPClassifier
#from sklearn.metrics import plot_confusion_matrix
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

milex21 = cleaned_dict.popitem()[1]
milex20 = cleaned_dict.popitem()[1]
 
keys = cleaned_dict.keys()
values = cleaned_dict.values()

fig, ax = plt.subplots(figsize=(6,4))
#fig = plt.figure(figsize=(20,10))
ax.scatter(keys, values)
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()


# time for some linear regression baby 

x_bias = np.concatenate((np.ones(len(cleaned_dict)).reshape(-1,1), np.array(list(keys)).astype(float).reshape(-1,1)), axis=1)


w_fit = np.linalg.lstsq(x_bias, np.array(list(values)).astype(float), rcond=None)[0]

y_pred = np.dot(x_bias, w_fit)


print("w_1 = {:.2f}".format(w_fit[1].item()))
print("b = {:.2f}".format(w_fit[0].item()))

fig, ax = plt.subplots(figsize=(6,4))
ax.scatter(keys, values)
ax.plot(keys, y_pred, '-r')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()


# using sklearns built in linear regression function to determine the weights and biases of the regression line 

regr = LinearRegression()
regr.fit(np.array(list(keys)).astype(float).reshape(-1,1), np.array(list(values)).astype(float))
print('w_1 = {:.2f}'.format(regr.coef_.item()))
print('b = {:.2f}'.format(regr.intercept_.item()))

print("prediction for 2020 = {}".format(regr.predict(np.array([2020]).reshape(1,-1))))
print("actual value = {}".format(milex20))
print("error = {}%".format((abs(milex20 - regr.predict(np.array([2020]).reshape(1,-1)))/milex20)[0]*100))

print("prediction for 2021 = {}".format(regr.predict(np.array([2021]).reshape(1,-1))))
print("actual value = {}".format(milex21))
print("error = {}%".format((abs(milex21 - regr.predict(np.array([2021]).reshape(1,-1)))/milex21)[0]*100))


# polynomial regression

poly_underfit = PolynomialFeatures(degree=2)
x_poly = poly_underfit.fit_transform(np.array(list(keys)).astype(float).reshape(-1,1))
regr.fit(x_poly, np.array(list(values)))

#x_plot = np.linspace(0,10,72).reshape(-1,1)
y_pred = regr.predict(poly_underfit.transform(np.array(list(keys)).astype(float).reshape(-1,1)))

fig,ax = plt.subplots(figsize=(6,4))
ax.scatter(keys, values)
ax.plot(keys, y_pred, '-r')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()



poly_overfit = PolynomialFeatures(degree=6)
x_poly = poly_overfit.fit_transform(np.array(list(keys)).astype(float).reshape(-1,1))
regr.fit(x_poly, np.array(list(values)))

#x_plot = np.linspace(0,10,72).reshape(-1,1)
y_pred = regr.predict(poly_overfit.transform(np.array(list(keys)).astype(float).reshape(-1,1)))

fig,ax = plt.subplots(figsize=(6,4))
ax.scatter(keys, values)
ax.plot(keys, y_pred, '-r')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()

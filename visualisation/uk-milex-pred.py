import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import sklearn
from sklearn import *
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import PolynomialFeatures



milexcel_uk = 'visualisation/milex-uk.xlsx'
milexcel_uk_pound = 'visualisation/milex-uk-pound.xlsx'


df = pd.read_excel(milexcel_uk_pound)
df = df.dropna(axis = 0) # remove empty rows
print(df)

new_dict = df.to_dict(orient='list') # preliminary form of dictionary

cleaned_dict = {}

#clean the dictionary
for x in new_dict.values():
    if x[0] == 'Country' or x[0] == 'Currency' or x[0] == 'Notes' or x[1] == '...':
        continue
    else:
       cleaned_dict[int(x[0])] = int(x[1])

# plot the points - expenditure as a function of time

milex21 = cleaned_dict.popitem()[1] #remove data post turn of decade
milex20 = cleaned_dict.popitem()[1]


keys = cleaned_dict.keys()
values = cleaned_dict.values()

"""
fig, ax = plt.subplots(figsize=(6,4))
#fig = plt.figure(figsize=(20,10))
ax.scatter(keys, values)
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()
"""

# time for some linear regression baby 

x_bias = np.concatenate((np.ones(len(cleaned_dict)).reshape(-1,1), np.array(list(keys)).astype(float).reshape(-1,1)), axis=1)


w_fit = np.linalg.lstsq(x_bias, np.array(list(values)).astype(float), rcond=None)[0]

y_pred = np.dot(x_bias, w_fit)
"""
print("my prediction for weight and bias")
print("w_1 = {:.2f}".format(w_fit[1].item()))
print("b = {:.2f}".format(w_fit[0].item()))
print("\n")


fig, ax = plt.subplots(figsize=(6,4))
ax.scatter(keys, values)
ax.plot(keys, y_pred, '-r')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()
"""


"""
print("my prediction for 2020's expenditure:")
print((w_fit[1].item() * 2020) + w_fit[0].item())
print("actual value")
print(milex20)

print("error = ")
print(((abs((w_fit[1].item() * 2020) + w_fit[0].item() - milex20))/milex20)*100)
print("\n")

print("my prediction for 2021's expenditure")
print((w_fit[1].item() * 2021) + w_fit[0].item())
print("actual value")
print(milex21)

print("error")
print(((abs((w_fit[1].item() * 2021) + w_fit[0].item() - milex21))/milex21)*100)
print("\n")
"""

# predict the expenditure for 2020, 2021, comapre to actual
# predict average expenditure for 20's, include error rate



# using sklearns built in linear regression function to determine the weights and biases of the regression line 

regr = LinearRegression()
regr.fit(np.array(list(keys)).astype(float).reshape(-1,1), np.array(list(values)).astype(float))

"""
print("sklearn's prediction for weight and bias")
print('w_1 = {:.2f}'.format(regr.coef_.item()))
print('b = {:.2f}'.format(regr.intercept_.item()))

print("Sklearns lin-reg prediction for 2020 = {}".format(regr.predict(np.array([2020]).reshape(1,-1))))
print("actual value = {}".format(milex20))
print("error = {}%".format((abs(milex20 - regr.predict(np.array([2020]).reshape(1,-1)))/milex20)[0]*100))

print("sklearn's lin-reg prediction for 2021 = {}".format(regr.predict(np.array([2021]).reshape(1,-1))))
print("actual value = {}".format(milex21))
print("error = {}%".format((abs(milex21 - regr.predict(np.array([2021]).reshape(1,-1)))/milex21)[0]*100))
"""


poly = PolynomialFeatures(degree = 2, include_bias=False)

poly_features = poly.fit_transform(np.array(list(keys)).reshape(-1,1))

poly_reg_model = LinearRegression()
poly_reg_model.fit(poly_features, np.array(list(values)))

x_vals = np.linspace(1950, 2020, 71).reshape(-1, 1)
y_predicted = poly_reg_model.predict(poly.transform(x_vals))

plt.figure()
plt.scatter(np.array(list(keys)), np.array(list(values)))
#plt.plot(np.array(list(keys)), y_predicted, c = "red")
plt.plot(x_vals, y_predicted, c = "red")
plt.show()

#print(poly_reg_model.predict([poly.transform(np.array(2020).reshape(-1,1))]))
pred20 = poly_reg_model.predict(poly.transform([[2020]]))[0]
print("predicted value of 2020 expenditure = {}".format(pred20))
print("actual expenditure = {}".format(milex20))
print("error = {}%".format((abs(milex20 - pred20)/milex20)*100))    
  
pred21 = poly_reg_model.predict(poly.transform([[2021]]))[0]
print("predicted value of 2021 expenditure = {}".format(pred21))
print("actual expenditure = {}".format(milex21))
print("error = {}%".format((abs(milex21 - pred21)/milex21)*100))

#milex_forecast = [pred20, pred21]
years_forecast = list(keys) + [2020, 2021]

forecast_dict = cleaned_dict

#reconstruct original dataset
forecast_dict[2020] = milex20
forecast_dict[2021] = milex21
print(len(years_forecast))
print(len(forecast_dict))


for i in range(1,9):
    years_forecast.append(2021+i)
    #milex_forecast.append(poly_reg_model.predict(poly.transform([[2021+i]]))[0])
    forecast_dict[2021+i] = poly_reg_model.predict(poly.transform([[2021+i]]))[0]




#appended_values = list(cleaned_dict.values()) + milex_forecast



poly_forecast = PolynomialFeatures(degree = 2, include_bias=False)

poly_forecast_features = poly_forecast.fit_transform(np.array(years_forecast).reshape(-1,1))

poly_forecast_reg_model = LinearRegression()
poly_forecast_reg_model.fit(poly_forecast_features, np.array(list(forecast_dict.values())))

x_forecast_vals = np.linspace(1950, 2029, 71).reshape(-1, 1)
y_forecast_predicted = poly_forecast_reg_model.predict(poly_forecast.transform(x_forecast_vals))


plt.figure()
plt.scatter(years_forecast, list(forecast_dict.values()))
#plt.plot(np.array(list(keys)), y_predicted, c = "red")
plt.plot(x_forecast_vals, y_forecast_predicted, c = "red")
plt.show()
#markov model?
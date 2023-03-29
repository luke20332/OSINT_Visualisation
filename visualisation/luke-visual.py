# some attempts at visualisation of the data

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import csv


from scipy.stats import multivariate_normal    

import imageio.v3 as iio

buyers = {}
counter = 0



with open("numerical_data\joined_data_numeric.csv", newline = '') as transferFile:
    fileReader = csv.reader(transferFile, delimiter = ' ', quotechar= '|')
    headers = next(fileReader)
    for row in fileReader:

        x = ",".join(row) # converts the list into a string
        x = x.split(',')
        
        if x[2] not in buyers:  # x[2] is the buyer
            buyers[x[2]] = int(x[8])
        else:
            buyers[x[2]] = buyers[x[2]] + int(x[8])
        
        #else:
        #    break



# may have to check if country is a double barrel name (united  x, soviet union, north x)

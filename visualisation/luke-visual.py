# some attempts at visualisation of the data

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import csv


from scipy.stats import multivariate_normal    

import imageio.v3 as iio

with open("numerical_data\joined_data_numeric.csv", newline = '') as transferFile:
    fileReader = csv.reader(transferFile, delimiter = ' ', quotechar= '|')
    for row in fileReader:
        print(', '.join(row))
        

# encoding: utf-8

##################################################
# This script shows how to explore values from a single variable using matplotlib and seaborn
# Multiple tutorials inspired the current design but they mostly came from:
# https://towardsdatascience.com/animations-with-matplotlib-d96375c5442c
# References for histograms using matplotlib https://matplotlib.org/stable/gallery/statistics/hist.html
# References for histograms using Seaborn https://seaborn.pydata.org/generated/seaborn.histplot.html
# Data uses the Open Data Barcelona API and especially the dataset
#
# Note: the project keeps updating every course almost yearly
##################################################
#
##################################################
# Author: Diego Pajarito
# Credits: [Institute for Advanced Architecture of Catalonia - IAAC, Advanced Architecture group]
# License:  Apache License Version 2.0
# Version: 0.7.0
# Maintainer: Diego Pajarito
# Email: diego.pajarito@iaac.net
# Status: development
##################################################

# We need to import numpy and matplotlib library

import pandas as pd

data_sample = pd.read_csv('../data/energy/sample.csv')
data_sample.columns = ['year', 'month', 'day', 'h24', 'price', 'price1', 'none']
data_sample = data_sample[data_sample['year'] != '*']
data_sample['dt_value'] = data_sample.apply(lambda row: row['year'] + '/' + str(int(row['month'])) + '/' +
                                                        str(int(row['day'])) + ' ' + str(int(row['h24'] - 1)) + ':00:00',
                                            axis=1)
data_sample['dt'] = pd.to_datetime(data_sample['dt_value'], format='%Y/%m/%d %H:%M:%S')


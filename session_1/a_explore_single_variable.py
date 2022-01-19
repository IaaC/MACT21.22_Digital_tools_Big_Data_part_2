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

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
plt.style.use('seaborn-pastel')

# default histogram
open_sense_measures = pd.read_csv('../data/barcelona/opensensemap_org-barcelona.csv')
sns.histplot(data=open_sense_measures, x="value")
plt.show()

# custome bin width and density
sns.histplot(data=open_sense_measures, x="value", bins=20, kde=True)
plt.show()

# Task
# Customise plots based on seaborn documentation

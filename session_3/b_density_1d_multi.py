# encoding: utf-8

##################################################
# This script shows how to visualise distribution from a single variable using matplotlib and seaborn
# Multiple tutorials inspired the current design but they mostly came from:
# https://seaborn.pydata.org/tutorial/distributions.html
# References for facet grids in seaborn https://matplotlib.org/stable/gallery/statistics/hist.html
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
meteocat_2021 = pd.read_csv('../data/barcelona/2021_MeteoCat_Detall_Estacions.csv')
temperature = meteocat_2021[meteocat_2021['ACRÒNIM'].isin(['TM', 'TX', 'TN'])]
# challenge: to integrate historical data

# filters for a single station
temp_station_1 = temperature[temperature['CODI_ESTACIO'] == 'D5']
sns.displot(data=temp_station_1, x="VALOR", hue="ACRÒNIM", kind="kde")
plt.show()

# Using facet grids to visualise multiple stations
grid = sns.FacetGrid(temperature, col="CODI_ESTACIO")
grid.map_dataframe(sns.histplot, x="VALOR", hue="ACRÒNIM", element='poly', bins=50)
plt.show()

# Build new variables for facets and densities


# encoding: utf-8

##################################################
# This script shows how to visualise distribution from two variables using and seaborn
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

# Using data from 2021
meteocat_2020 = pd.read_csv('../data/barcelona/2020_MeteoCat_Detall_Estacions.csv')

# Updating date formats and extracting months
meteocat_2020['DATE'] = pd.to_datetime(meteocat_2020['DATA_LECTURA'], format='%Y-%m-%d', errors='ignore')
meteocat_2020['MONTH'] = pd.DatetimeIndex(meteocat_2020['DATE']).month

# Selecting values for radiation and plotting 2d density
radiation = meteocat_2020[meteocat_2020['ACRÒNIM'].isin(['RS24h'])]
sns.displot(data=radiation, x="VALOR", y="MONTH")
plt.show()

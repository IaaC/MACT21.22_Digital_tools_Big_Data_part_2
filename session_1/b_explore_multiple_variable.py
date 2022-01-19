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
import urllib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import pandas as pd
import matplotlib
plt.style.use('seaborn-pastel')




# Data BCN API: Mesurements of the meteorological stations of the city of Barcelona
# Source: https://opendata-ajuntament.barcelona.cat/data/en/dataset/mesures-estacions-meteorologiques
url = 'https://opendata-ajuntament.barcelona.cat/data/dataset/cf1de5ca-9d1c-424c-9543-8ab23e7f478e/resource/0b96a191-463e-43ce-bb3a-67e61a96f466/download'
bcn_stations = pd.read_csv(url)

# Filtering to get the values for a single variable
bcn_mean_temperature = bcn_stations[bcn_stations['ACRÒNIM'] == 'TM']

# Default histogram for single variable
sns.histplot(data=bcn_mean_temperature, x="VALOR", kde=True)
plt.show()

# Preparing data for the second variable
bcn_mean_temperature['DATE'] = pd.to_datetime(bcn_mean_temperature['DATA_LECTURA'], format='%Y-%m-%d', errors='ignore')

# Scatter plot
sns.scatterplot(data=bcn_mean_temperature, x="DATE", y="VALOR")
# Task
# Customise plots based on seaborn documentation
# https://seaborn.pydata.org/generated/seaborn.scatterplot.html
# Add extra values and comparte with additional variables
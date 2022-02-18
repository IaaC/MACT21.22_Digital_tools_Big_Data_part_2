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

# Filtering values for relative humidity and precipitation
hum_precip = meteocat_2020[meteocat_2020['ACRÒNIM'].isin(['HRM', 'PM'])]

# Grouping data by date of measure (aggregates data from all stations)
hum_precip_group = hum_precip.groupby(['DATA_LECTURA', 'ACRÒNIM'])

hum_precip_group_calculated = hum_precip.groupby(['DATA_LECTURA', 'ACRÒNIM']).mean()

# Once grouped, we calculate the mean and use a pivot function to transpose values into columns
hum_precip_day = hum_precip_group.mean().reset_index().pivot(index="DATA_LECTURA", columns='ACRÒNIM', values='VALOR').reset_index()
# Note, pivot functions has considerations with indexed colum names
# Check the issue here https://stackoverflow.com/questions/42099024/pandas-pivot-table-rename-columns
hum_precip_day.columns = list(map("_".join, hum_precip_day.columns))

# Using distribution plot we provide to dimensions to creat the visualisation
sns.displot(data=hum_precip_day, x="VALOR_HRM", y="VALOR_PM")
plt.show()

print('end')
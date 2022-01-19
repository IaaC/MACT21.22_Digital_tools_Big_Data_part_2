# encoding: utf-8

##################################################
# This script shows uses the pandas library to visualise geospatial data sets
##################################################
#
##################################################
# Author: Diego Pajarito
# Credits: [Institute for Advanced Architecture of Catalonia - IAAC, Advanced Architecture group]
# License:  Apache License Version 2.0
# Version: 1.0.0
# Maintainer: Diego Pajarito
# Email: diego.pajarito@iaac.net
# Status: development
##################################################

# We need to import pandas library as well as the plot libraries matplotlib and seaborn
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

# We read the file from Open Data Barcelona
# https://opendata-ajuntament.barcelona.cat/data/en/dataset/20170706-districtes-barris/resource/cd800462-f326-429f-a67a-c69b7fc4c50a
url = 'https://opendata-ajuntament.barcelona.cat/data/dataset/82dc847a-661d-4701-a582-b0c1aba89b2a/resource/feafec8a-b389-42b5-a85d-cf16f3976440/download'
bcn_stations = pd.read_csv(url)

# Setting up the geospatial features
crs={'init':'epsg:4326'}
geometry = [Point(xy) for xy in zip(bcn_stations["LONGITUD"], bcn_stations["LATITUD"])]
bcn_stations_geo = geopandas.GeoDataFrame(bcn_stations, crs=crs, geometry=geometry)

bcn_stations_geo.plot()
plt.show()

# Task
# Add points from the second dataset (SenseBox)
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
# https://opendata-ajuntament.barcelona.cat/data/en/dataset/metadades-estacions-meteorologiques/resource/feafec8a-b389-42b5-a85d-cf16f3976440
url = 'https://opendata-ajuntament.barcelona.cat/data/dataset/82dc847a-661d-4701-a582-b0c1aba89b2a/resource/feafec8a-b389-42b5-a85d-cf16f3976440/download'
bcn_stations = pd.read_csv(url)

# We read the file from Open Sense Map
open_sense_measures = pd.read_csv('../data/barcelona/opensensemap_org-barcelona.csv')

# Setting up the geospatial features
crs = {'init': 'epsg:4326'}
geometry = [Point(xy) for xy in zip(bcn_stations["LONGITUD"], bcn_stations["LATITUD"])]
bcn_stations_geo = geopandas.GeoDataFrame(bcn_stations, crs=crs, geometry=geometry)
geometry = [Point(xy) for xy in zip(open_sense_measures["lon"], open_sense_measures["lat"])]
open_sense_geo = geopandas.GeoDataFrame(open_sense_measures, crs=crs, geometry=geometry)

# To plot multiple layers we need to use subplots
f, ax = plt.subplots()
bcn_stations_geo.plot(ax=ax, marker='o', color='blue', markersize=20)
open_sense_geo.plot(ax=ax, marker='*', color='green', markersize=15)
plt.show()


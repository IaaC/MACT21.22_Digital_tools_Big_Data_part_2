# encoding: utf-8

##################################################
# This script shows uses the geopandas library to calculate distances between geometries
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

# We read the file from Open Data Barcelona and select stations measure temperature
# https://opendata-ajuntament.barcelona.cat/data/en/dataset/metadades-estacions-meteorologiques/resource/feafec8a-b389-42b5-a85d-cf16f3976440
# url = 'https://opendata-ajuntament.barcelona.cat/data/dataset/82dc847a-661d-4701-a582-b0c1aba89b2a/resource/feafec8a-b389-42b5-a85d-cf16f3976440/download'
# bcn_stations = pd.read_csv(url)
bcn_stations = pd.read_csv('../data/barcelona/2020_MeteoCat_Estacions.csv')
bcn_stations = bcn_stations[bcn_stations['ACRÒNIM'] == 'TM']

# We read the file from Open Sense Map and calculate the average value by sensor
open_sense_measures = pd.read_csv('../data/barcelona/opensensemap_org-barcelona.csv')
open_sense_measures = open_sense_measures.groupby(['lat','lon', 'boxName', 'unit'])['value'].mean().reset_index()

# Setting up the geodataframes
crs = {'init': 'epsg:4326'}
geometry = [Point(xy) for xy in zip(bcn_stations["LONGITUD"], bcn_stations["LATITUD"])]
bcn_stations_geo = geopandas.GeoDataFrame(bcn_stations, crs=crs, geometry=geometry)
geometry = [Point(xy) for xy in zip(open_sense_measures["lon"], open_sense_measures["lat"])]
open_sense_geo = geopandas.GeoDataFrame(open_sense_measures, crs=crs, geometry=geometry)

# we can calculate the distrance between a dataframe and a reference point
reference = Point(2.05, 41.38)
distance = open_sense_geo.distance(reference)

# task: change the points and get to the distance
p1 = open_sense_geo.iloc[[0]]
distance_1 = p1.distance(reference)
print(distance_1)
p2 = open_sense_geo.iloc[[1]]
distance_2 = p2.distance(Point(2.05, 41.38))
print(distance_2)

# Task: Calculate distance between all points in the two dataframes


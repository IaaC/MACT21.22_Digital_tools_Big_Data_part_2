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
crs_bcn = {'init': 'epsg:32631'}
geometry = [Point(xy) for xy in zip(bcn_stations["LONGITUD"], bcn_stations["LATITUD"])]
bcn_stations_geo = geopandas.GeoDataFrame(bcn_stations, crs=crs, geometry=geometry)
bcn_stations_geo = bcn_stations_geo.to_crs(crs_bcn)
geometry = [Point(xy) for xy in zip(open_sense_measures["lon"], open_sense_measures["lat"])]
open_sense_geo = geopandas.GeoDataFrame(open_sense_measures, crs=crs, geometry=geometry)
open_sense_geo = open_sense_geo.to_crs(crs_bcn)


# Task: We can see the distance in projection units (metres)
open_sense_geo.geometry.apply(lambda g: bcn_stations_geo.distance(g))
print(open_sense_geo)
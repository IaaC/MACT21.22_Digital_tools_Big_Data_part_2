# encoding: utf-8

##################################################
# This script shows uses the geopandas library to create lines from two points geometries
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
from shapely.geometry import Point, Polygon, LineString

# We read the file from Open Data Barcelona and select stations measure temperature
# https://opendata-ajuntament.barcelona.cat/data/en/dataset/metadades-estacions-meteorologiques/resource/feafec8a-b389-42b5-a85d-cf16f3976440
# url = 'https://opendata-ajuntament.barcelona.cat/data/dataset/82dc847a-661d-4701-a582-b0c1aba89b2a/resource/feafec8a-b389-42b5-a85d-cf16f3976440/download'
#bcn_stations = pd.read_csv(url)
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

# we create an array with the two points and create a line
# This approach serve to extend it to multiline
# Example: https://stdworkflow.com/135/how-to-convert-points-to-lines-in-geopandas
lines = []
start_points = []
end_points = []
# to make it across the two data sets we use for loops based on the dataframe indexes
for e1 in open_sense_geo.index.to_list():
    node1 = [open_sense_geo.loc[e1, 'lon'], open_sense_geo.loc[e1, 'lat']]
    start = open_sense_geo.loc[e1, 'boxName']
    for e2 in bcn_stations_geo.index.to_list():
        node2 = [bcn_stations_geo.loc[e2, 'LONGITUD'], bcn_stations_geo.loc[e2, 'LATITUD']]
        line = LineString([node1, node2])
        end = bcn_stations_geo.loc[e2, 'NOM_ESTACIO']
        lines.append(line)
        start_points.append(start)
        end_points.append(end)
#data = [start_points, end_points] # to be reviewed for addting attributes

# with the list of geometries, we can create a geodataframe
lines_geo = geopandas.GeoDataFrame(geometry=lines)

# we use subplots to overlay multiple layers
f, ax = plt.subplots()
bcn_stations_geo.plot(ax=ax, marker='o', color='blue', markersize=20)
open_sense_geo.plot(ax=ax, marker='*', color='green', markersize=15)
lines_geo.plot(ax=ax)
plt.show()

print('end')
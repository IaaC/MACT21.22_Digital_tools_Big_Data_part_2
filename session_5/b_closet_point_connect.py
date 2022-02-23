# encoding: utf-8

##################################################
# This script shows how to find the closest point from a geodataframe
# The pricess was drafted by checking official docs and proposal from developers
# https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
# https://github.com/shapely/shapely/blob/main/docs/manual.rst#nearest-points
# https://gis.stackexchange.com/questions/222315/finding-nearest-point-in-other-geodataframe-using-geopandas

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

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Libraries needed for the closest point calculation
from shapely.ops import nearest_points
from shapely.geometry import LineString



# Predefined area of interest
aoi_path = "../data/footfall/aoi_glories.geojson"
aoi = gpd.read_file(aoi_path)
minx, miny, maxx, maxy = aoi.geometry.total_bounds

# Geospatial point reference data (originally served as EPSG:25831)
bus_stops_path = f'../data/barcelona/ESTACIONS_BUS.csv'
stops = pd.read_csv(bus_stops_path)
stops = gpd.GeoDataFrame(stops, geometry=gpd.points_from_xy(stops.ETRS89_COORD_X, stops.ETRS89_COORD_Y),
                         crs='epsg:25831')
stops_aoi = gpd.clip(stops, aoi)


# Footfall data to process
footfall_path = "../data/footfall/footfall_aoi.geojson"
footfall = gpd.read_file(footfall_path)


# empty geodataframe for the lines
shortest_lines = gpd.GeoDataFrame(columns=["id", 'geometry'], crs="EPSG:25831", geometry="geometry")
shortest_lines_path = "../data/footfall/shortest_lines.geojson"

stops_aggregated = stops_aoi.geometry.unary_union
# find the nearest point and return the corresponding Place value

for index, point in footfall.iterrows():
    nearest = nearest_points(point.geometry, stops_aggregated)[1]
    line = LineString([point.geometry, nearest])
    row = gpd.GeoDataFrame(geometry=[line])
    row['id'] = index
    shortest_lines = gpd.GeoDataFrame(pd.concat([shortest_lines, row], ignore_index=True), crs=shortest_lines.crs)

# Saving the concatenated lines to geojson
shortest_lines.to_file(shortest_lines_path, driver="GeoJSON")
print('Points extracted: ' + str(len(shortest_lines)))

f, ax = plt.subplots()
aoi.plot(ax=ax, facecolor="none", edgecolor='grey', lw=0.3)
footfall.plot(ax=ax, marker='o', color='red', markersize=0.5, alpha=0.3)
shortest_lines.plot(ax=ax, lw=0.1)
ax.set_xlim(minx - .1, maxx + .1)  # Using the previously calculated boundaries
ax.set_ylim(miny - .1, maxy + .1)
ax.xaxis.set_major_locator(ticker.NullLocator())
ax.yaxis.set_major_locator(ticker.NullLocator())
plt.show()
print('end')



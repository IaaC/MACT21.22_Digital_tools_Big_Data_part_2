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
import seaborn as sns

# Libraries needed for the closest point calculation
from shapely.ops import nearest_points



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


# We need to build a generic near function that uses "nearest point"
def near(point, gdf2, id_col):
    # we need to treat the reference points as an aggregation
    points = gdf2.geometry.unary_union
    # find the nearest point and return the corresponding Place value
    nearest = gdf2.geometry == nearest_points(point, points)[1]
    return gdf2[nearest].loc[:, id_col].values


footfall['Nearest_stop'] = footfall.apply(lambda row: near(row.geometry, stops_aoi, 'EQUIPAMENT'), axis=1)

sns.histplot(data=footfall, x="Nearest_stop")
plt.show()



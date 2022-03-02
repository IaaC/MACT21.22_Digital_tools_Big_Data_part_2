# encoding: utf-8

##################################################
# This uses the MOVINGPANDAS tutorial to explore the use of this library in pyCharm
# The source code presented is directly adapted from the official gitHub Repo
# https://github.com/anitagraser/movingpandas

#
# Note: for the use in anaconda it is recommended to create a separated environment
# Use the following commands
# $  conda create -n mvp python=3.9
# $  conda install -n mvp -c conda-forge movingpandas
##################################################
#
##################################################
# Author: Diego Pajarito
# Credits: [Institute for Advanced Architecture of Catalonia - IAAC, Advanced Architecture group]
# License:  Apache License Version 2.0
# Version: 0.5.0
# Maintainer: Diego Pajarito
# Email: diego.pajarito@iaac.net
# Status: development
##################################################

# This script corresponds to the "Getting Started" Notebook
# See the original here https://github.com/anitagraser/movingpandas/blob/master/tutorials/1-getting-started.ipynb

import urllib
import os
import pandas as pd
#from fiona.crs import from_epsg
import geopandas as gpd
from geopandas import GeoDataFrame, read_file
from shapely.geometry import Point, LineString, Polygon
from datetime import datetime, timedelta
from matplotlib import pyplot as plt

import sys
import movingpandas as mpd
mpd.show_versions()


## Creating a trajectory from the existing FOOTFALL layer
# df = gpd.read_file("../data/footfall/footfall_aoi.shp")
df = pd.read_csv("../data/footfall/footfall_aoi.csv")
df['t'] = pd.to_datetime(df['TIMESTAMP'], unit='s')
df['geometry'] = df.apply(lambda row: Point(row.LONGITUDE, row.LATITUDE), axis=1)
df = df.set_index('t')
geo_df = GeoDataFrame(df, crs=4326)
geo_df = geo_df.to_crs("EPSG:25831")

# Creating trajectory collection based on "DEVICE_AID"
traj_collection = mpd.TrajectoryCollection(geo_df, 'DEVICE_AID', t='t')
print(traj_collection)

# Trajectories can be plot
traj_collection.to_line_gdf().plot(column='DEVICE_AID', legend=False)

# Trajectories can be saved and therefore analysed in a GIS tool
# Likely to fail in MacOS
#traj_collection.to_line_gdf().to_file("../data/footfall/footfall_aoi_traj.geojson", layer='trajectories', driver="GeoJSON")


# Splitting Trajectories
split = mpd.ObservationGapSplitter(traj_collection).split(gap=timedelta(minutes=5))

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 4))
traj_collection.to_line_gdf().plot(ax=axes[0], column='DEVICE_AID')
axes[0].set_title('Original Trajectories')
split.to_line_gdf().plot(ax=axes[1], column='DEVICE_AID')
axes[1].set_title('Split Trajectories')
plt.show()


# Split trajectories can be saved and therefore analysed in a GIS tool
# Likely to fail in MacOS
# split.to_line_gdf().to_file("../data/footfall/footfall_aoi_traj.geojson", layer='trajectories', driver="GeoJSON")


# Smoothing Trajectories
# It can fail in PyCharm depending on the moving pandas framework used
smooth = mpd.trajectory_smoother.KalmanSmootherCV(split).smooth(process_noise_std=0.1, measurement_noise_std=10)
print(smooth)
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
import geopandas as gpd
from geopandas import GeoDataFrame, read_file
from shapely.geometry import Point, LineString, Polygon
# from fiona.crs import from_epsg
from datetime import datetime, timedelta
from matplotlib import pyplot as plt

import sys
sys.path.append("..")
import movingpandas as mpd
mpd.show_versions()


## Creating a trajectory from the existing FOOTFALL layer
# df = gpd.read_file("../data/footfall/footfall_aoi.shp")
df = pd.read_csv("../data/footfall/footfall_aoi_single.csv")
df['t'] = pd.to_datetime(df['TIMESTAMP'], unit='s')
df['geometry'] = df.apply(lambda row: Point(row.LONGITUDE, row.LATITUDE), axis=1)
df = df.set_index('t')
geo_df = GeoDataFrame(df, crs=4326)
geo_df = geo_df.to_crs("EPSG:25831")
toy_traj = mpd.Trajectory(geo_df, 1)

# trajectory as dataframe
toy_traj.df


# trajectory as a line geodataframe
toy_traj.to_line_gdf()

# Print Trajectory as a dataframe and WKT
print(toy_traj.to_traj_gdf(wkt=True))

# Print raw trajectory
print(toy_traj)

# Print trajectory as linestring
print(toy_traj.to_linestring())

# Add Speed to trajectory and plot
toy_traj.add_speed(overwrite=True)
toy_traj.df.plot()

# Plot using speed values
toy_traj.to_line_gdf().plot(column="speed", linewidth=5, capstyle='round', legend=True)

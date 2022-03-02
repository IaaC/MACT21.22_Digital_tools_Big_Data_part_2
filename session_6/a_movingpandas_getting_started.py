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


## Creating a trajectory from Scratchb

df = pd.DataFrame([
  {'geometry':Point(0,0), 't':datetime(2018,1,1,12,0,0)},
  {'geometry':Point(6,0), 't':datetime(2018,1,1,12,6,0)},
  {'geometry':Point(6,6), 't':datetime(2018,1,1,12,10,0)},
  {'geometry':Point(9,9), 't':datetime(2018,1,1,12,15,0)}
]).set_index('t')
geo_df = GeoDataFrame(df, crs=31256)
toy_traj = mpd.Trajectory(geo_df, 1)
toy_traj.df


# trajectory as a dataframe
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


## Trajectory analysis
# Extract location at a given time
print('Location at')
print(toy_traj.get_position_at(datetime(2018, 1, 1, 12, 10, 40), method="nearest"))

# Extract location at a given time, different methods
print('Location at (different methods)')
print(toy_traj.get_position_at(datetime(2018, 1, 1, 12, 10, 40), method="nearest"))
print(toy_traj.get_position_at(datetime(2018, 1, 1, 12, 10, 40), method="interpolated"))
print(toy_traj.get_position_at(datetime(2018, 1, 1, 12, 10, 40), method="ffill"))
print(toy_traj.get_position_at(datetime(2018, 1, 1, 12, 10, 40), method="bfill"))

# Extract segment from a time interval, different methods
segment = toy_traj.get_segment_between(datetime(2018, 1, 1, 12, 2, 0), datetime(2018, 1, 1, 12, 13, 0))
print(segment)
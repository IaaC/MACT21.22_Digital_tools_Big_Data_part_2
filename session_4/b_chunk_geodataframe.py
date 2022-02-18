# encoding: utf-8

##################################################
# This script shows how to read large files using pandas
# With files exceeding sizes of GB, the chunk alternative is most of the times needed
# https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html


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
import matplotlib as plt

# Output file path and param
day_num = 1
input_csv_filepath = f'../data/footfall/footfall_20210217/day{day_num}Bcntrakingotherdays.csv'

# Setting a loop for chunks is compatible with geopandas
chunksize = 10 ** 5
for df_chunk in pd.read_csv(input_csv_filepath, delimiter='|', low_memory=False, on_bad_lines='skip',
                            chunksize=chunksize):
    gdf_chunk = gpd.GeoDataFrame(df_chunk, geometry=gpd.points_from_xy(df_chunk.LONGITUDE, df_chunk.LATITUDE),
                                 crs='epsg:4326')
    print('Chunk size in rows: ' + str(len(gdf_chunk)))


print('end')
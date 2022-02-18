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
import matplotlib.pyplot as plt

# Geospatial reference data (originally served as EPSG:25831)
ud_admin_path = "../data/barcelona/0301100100_UNITATS_ADM_POLIGONS.json"
ud_admin = gpd.read_file(ud_admin_path)
barris = ud_admin[ud_admin['CONJ_DESCR'] == 'Barris']
minx, miny, maxx, maxy = barris.geometry.total_bounds       # To control the visual representation of the plot



# Output file path and param
day_num = 1
input_csv_filepath = f'../data/studio/footfall/footfall_20210217/day{day_num}Bcntrakingotherdays.csv'

# Setting a loop for chunks is compatible with geopandas
chunksize = 10 ** 5
for df_chunk in pd.read_csv(input_csv_filepath, delimiter='|', low_memory=False, on_bad_lines='skip',
                            chunksize=chunksize):
    gdf_chunk = gpd.GeoDataFrame(df_chunk, geometry=gpd.points_from_xy(df_chunk.LONGITUDE, df_chunk.LATITUDE),
                                 crs='epsg:4326')
    gdf_chunk = gdf_chunk.to_crs("EPSG:25831")      # Projection needed to ensure visual and geographic processing
    f, ax = plt.subplots()
    barris.plot(ax=ax, facecolor="none", edgecolor='grey', lw=0.3)
    gdf_chunk.plot(ax=ax, marker='o', color='red', markersize=0.5)
    ax.set_xlim(minx - .1, maxx + .1)  # Using the previously calculated boudaries
    ax.set_ylim(miny - .1, maxy + .1)
    plt.show()

print('end')
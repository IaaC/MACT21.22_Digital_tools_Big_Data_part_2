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
import matplotlib.ticker as ticker


# Path to concatenated file
footfall_aoi_path = "../data/footfall/footfall_aoi.geojson"

# Geospatial clip area of interest
aoi_path = "../data/footfall/aoi_glories.geojson"
aoi = gpd.read_file(aoi_path)
minx, miny, maxx, maxy = aoi.geometry.total_bounds       # To control the visual representation of the plot


# Empty geodataframe with the structure of footfall data
footfall_aoi = gpd.GeoDataFrame(columns=["SSCCG_SSCCCODOF", "MUNG_MUNCODOF", "PROVG_PROVCODOF", "CCAAG_CCAACODOF",
                                         "TIMESTAMP", "DEVICE_AID", "DEVICE_AID_TYPE", "LATITUDE", "LONGITUDE",
                                         "HORIZONTAL_ACCURACY", "ALTITUDE", "ALTITUDE_ACCURACY", "LOCATION_METHOD",
                                         "IP", "USER_AGENT", "OS", "OS_VERSION", "MANUFACTURER", "MODEL", "CARRIER",
                                         "FECHA_DATOS", "THE_GEOM", "ID_SSCC", "ID_CP", "ID_MUN", "ID_PROV",
                                         "ID_CCAA", 'geometry'],
                                crs="EPSG:25831", geometry="geometry")

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
    clip_chunk = gpd.clip(gdf_chunk, aoi)
    # footfall_aoi = footfall_aoi.append(clip_chunk)    # To-be deprecated method
    footfall_aoi = gpd.GeoDataFrame(pd.concat([footfall_aoi, clip_chunk], ignore_index=True), crs=footfall_aoi.crs)

# Saving the concatenated file to geojson
footfall_aoi.to_file(footfall_aoi_path, driver="GeoJSON")
print('Points extracted: ' + str(len(footfall_aoi)))

f, ax = plt.subplots()
aoi.plot(ax=ax, facecolor="none", edgecolor='grey', lw=0.3)
footfall_aoi.plot(ax=ax, marker='o', color='red', markersize=0.5, alpha=0.3)
ax.set_xlim(minx - .1, maxx + .1)  # Using the previously calculated boundaries
ax.set_ylim(miny - .1, maxy + .1)
ax.xaxis.set_major_locator(ticker.NullLocator())
ax.yaxis.set_major_locator(ticker.NullLocator())
plt.show()
print('end')
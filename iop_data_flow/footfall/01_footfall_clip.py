import os

import pandas as pd
import geopandas as gpd

## Config

# Number of rows to read
nrows = 10
#nrows = 1000000
#nrows = None

# Output file path
day_num = 1
input_csv_filepath = f'../../data/studio/footfall/footfall_20210217/day{day_num}Bcntrakingotherdays.csv'

# Clip mask file path
clip_mask_filepath = '../../data/studio/clip_area/clip_darea.shp'

# Output file path
output_file = f'ff-day{day_num}-clipped.shp'
output_folder = '../../data/studio/footfall/01_clipped/'

## Run

# Load csv all spain footfall
print(f"Load csv footfall : {input_csv_filepath}")
df = pd.read_csv(input_csv_filepath,
                 delimiter='|',
                 nrows=nrows)

# Convert it to geopandas
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.LONGITUDE, df.LATITUDE), crs='epsg:4326')
print(f"Footfall all: {len(gdf)} points")

# Load clip mask
mask_gdf = gpd.read_file(clip_mask_filepath)
mask_gdf = mask_gdf[mask_gdf['geometry'].notnull()]

# Clip it to district
gdf = gpd.clip(gdf, mask_gdf)
print(f"Footfall clipped district: {len(gdf)} points")

# Create output directory if it doesn't exist
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
output_fullpath = os.path.join(output_folder, output_file)

# Save clipped points
gdf.to_file(output_fullpath)
print(f"Saved shp footfall district: {output_fullpath}")
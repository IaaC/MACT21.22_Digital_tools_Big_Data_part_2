import os
import pandas as pd
import geopandas as gpd

## Config

# Output file path
output_file = f'ff-all-clipped_concat.shp'
output_folder = '../../data/studio/footfall/02_clipped_concat/'

## Run

# Read all points
gdf1 = gpd.read_file('../../data/studio/footfall/01_clipped/ff-day1-clipped.shp')
print(f"gdf1: {len(gdf1)} points")
gdf2 = gpd.read_file('../../data/studio/footfall/01_clipped/ff-day2-clipped.shp')
print(f"gdf2: {len(gdf2)} points")

# Concatenate them
concat_gdf = pd.concat([gdf1, gdf2]).pipe(gpd.GeoDataFrame)
print(f"concat_gdf: {len(concat_gdf)} points")

# Create output directory if it doesn't exist
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
output_fullpath = os.path.join(output_folder, output_file)

# Save the concatenation
concat_gdf.to_file(output_fullpath)

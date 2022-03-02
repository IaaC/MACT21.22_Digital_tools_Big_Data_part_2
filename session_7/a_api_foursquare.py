# encoding: utf-8

##################################################
# This script provides an example for using a public API to gather information from TripAdvisor
# it creates an output file with information coming from their platform
# To get credentials for the API visit https://developer.foursquare.com/docs/api/venues/search
##################################################
#
##################################################
# Author: Iacopo Testi
# Copyright: Copyright 2020, IAAC
# Credits: [Institute for Advanced Architecture of Catalonia - IAAC, Advanced Architecture group]
# License:  Apache License Version 2.0
# Version: 1.3.0
# Maintainer: Diego Pajarito
# Email: diego.pajarito@iaac.net
# Status: development
##################################################

# import all libraries
import json
import pandas as pd
import requests

# open csv file with containing the limits fo a grid cell array
df_grid = pd.read_csv('../data/api/grid.csv')
# Get only the
df_grid = df_grid[['left', 'top']]

# Due to limitation of calls per day, you should use up to 500 elements for testing
df_grid = df_grid.iloc[0:500]

# create an empty list to store the dictionaries containing data retrived in the loop
list_of_dictionaries = []
# set new lists to set a dataframe later on
venues_id = []
names = []
latitudes = []
longitudes = []
category = []

# url taken by the Foursquare API developers page -> Places API -> Venues -> Search for venues
url = 'https://api.foursquare.com/v2/venues/search'
# make a for loop to iterate through the points of the grid created in QGIS to extract all lot and lat
for i in df_grid.index:
    # this is to extract the lon and lat of each point
    lon = df_grid['left'][i]
    lat = df_grid['top'][i]
    # concatenate lon and lat values. Be aware of the need to cast from number to string.
    lat_lon = str(lat) + ',' + str(lon)

    # parameters taken from the API developers page 'search for venues' (same as above)
    params = dict(
        client_id='replace_with_your_id',
        client_secret='replace_with_your_secret',
        v='20180323',
        ll=lat_lon,  # each time it is replaced with new coordinates
        intent='browse',
        radius=30,
        limit=100
    )

    # use the request.get method to ask for the parameters
    resp = requests.get(url=url, params=params)
    # Print the raw response
    print(resp)

    # json.loads method transforms the response into a dictionary
    data = json.loads(resp.text)

    # append to the new dictionary created
    list_of_dictionaries.append(data)
    # end of loop

# this for loop iterates through the list of dictionaries to extract them one by one
for det_venues in list_of_dictionaries:
    # this second loop retrieves the parameters inside the json format
    for i in det_venues['response']['venues']:

        # add all the ids to the venues_id list
        venues_id.append(i['id'])
        # add all the names to the names list
        names.append(i['name'])
        # add all the latitudes to the latitudes list
        latitudes.append(i['location']['lat'])
        # add all the latitudes to the latitudes list
        longitudes.append(i['location']['lng'])

        # this for loop retrieve all the categories
        for cat in i['categories']:
            # add all the categories to the category list
            category.append(cat['name'])

print('--------------------------- Underneath printed all the lists to check them ---------------------------------')
print('venues id:', venues_id)
print('names:', names)
print('latitudes:', latitudes)
print('longitudes:', longitudes)
print('category:', category)

# create dataframe from lists names, latitudes, longitudes
df_venues = pd.DataFrame(list(zip(venues_id, names, latitudes, longitudes, category)),
                         columns=['Venues_id', 'Name', 'lat', 'lon', 'category'])

# drop rows with same values in column Venues_id
df_venues_search = df_venues.drop_duplicates(subset=['Venues_id'], keep='last')

# reset the row id values
df_venues_search.reset_index(drop=True, inplace=True)

# export data frame df_venues in csv
df_venues_search.to_csv('./venues_output.csv')

print('Successfully exported %i items from Foursquare' % len(df_venues_search))
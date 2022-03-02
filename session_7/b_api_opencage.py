# encoding: utf-8

##################################################
# This script uses the opencage geocoding service to get the coordinates corresponding to an address
# it creates an output file with structured information combining the input address and the API response
# To get credentials for the API visit https://opencagedata.com/api#quickstart
##################################################
#
##################################################
# Author: Diego Pajarito
# Copyright: Copyright 2020, IAAC
# Credits: [Institute for Advanced Architecture of Catalonia - IAAC, Advanced Architecture group]
# License:  Apache License Version 2.0
# Version: 1.3.0
# Maintainer: Diego Pajarito
# Email: diego.pajarito@iaac.net
# Status: development
##################################################

# import all libraries
import pandas as pd
import requests

# url taken from the API developers page
url = 'https://api.opencagedata.com/geocode/v1/json'

# This is an example to geocode IAAC's address
address_1 = 'Carrer de pujades, 102'

# This object contains the parameters needed for
params = dict(
    q=address_1,
    key='replace_with_your_key'
)
resp = requests.get(url=url, params=params)
# Print the raw response
print(resp)

output = resp.json()
first_result = output['results'][0]

geocoded_result = {'address_input': [address_1],
                   'address_formatted': [first_result['formatted']],
                   'lat': [first_result['geometry']['lat']],
                   'lon': [first_result['geometry']['lng']]
                   }

geocoded_output = pd.DataFrame(data=geocoded_result)
geocoded_output.to_csv('geocoding_outuput.csv')
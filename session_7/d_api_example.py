# Example for

import requests
import pandas as pd

# To get access to the API we need to check 'https://www.ree.es/es/apidatos'
# for instructions.
# It is usually needed a URL and a set of parameters
hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
url_balance = 'https://apidatos.ree.es/es/datos/balance/balance-electrico'
url_demand = 'https://apidatos.ree.es/en/datos/demanda/ire-general?'
url_generation = 'https://apidatos.ree.es/es/datos/generacion/estructura-generacion'

params = {'start_date': '2020-01-01T00:00', 'end_date': '2021-12-31T23:59', 'time_trunc': 'month',
          'geo_trunc': 'electric_system', 'geo_limit': 'peninsular', 'geo_ids': '8741'}
resp = requests.get(url_demand, params=params, headers=hdr)
json = resp.json()

# Based on the response and the documentation, usual response from REE.ES
# usually provides a list of indicators
# General index [0]
# Corrected General index [1]
# Monthly variation [2]
# Corrected Monthly variation [3]
# Using pandas they can become Dataframes. It is important to follow the response JSON data structure+

df_cgi = pd.DataFrame.from_dict(json['included'][1])
df_cmv = pd.DataFrame.from_dict(json['included'][3])

pd.DataFrame.from_dict(json['included'][0])
pd.DataFrame.from_dict()

print('End')

#https://www.omie.es/es/file-access-list?parents%5B0%5D=/&parents%5B1%5D=Mercado%20Diario&parents%5B2%5D=1.%20Precios&dir=Precios%20horarios%20del%20mercado%20diario%20en%20España&realdir=marginalpdbc

#https://www.ree.es/es/apidatos
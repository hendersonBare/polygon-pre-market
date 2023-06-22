# a seperate file used to manually verify API calls and the information that they put out

import config, json, requests, datetime, pandas

response = requests.get('https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/minute' +
                        '/1686888000000/1686922200000?adjusted=true&sort=asc&limit=5000&apiKey=' + config.API_KEY)

data = response.json() # converts the HTTP response into a JSON object

results = data['results'] # creates a list of the 'results' in this JSON object to ignore unneeded info

"""for x in results:
    print(datetime.datetime.fromtimestamp(x['t'] / 1000))"""

print('\n')
print(datetime.datetime.fromtimestamp(1627632000000 / 1000))

print(datetime.datetime.fromtimestamp(1627651800000 / 1000))

"""for x in results:
    print (x['h'])"""
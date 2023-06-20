import config, json, requests, datetime, pandas

def isValidTicker(ticker):
    response = requests.get('https://api.polygon.io/v2/aggs/ticker/' + ticker + '/range/1/minute' +
                        '/1686888000000/1686922200000?adjusted=true&sort=asc&limit=5000&apiKey=' + config.API_KEY)
    data = response.json()
    #need error handling for when the ticker yeilds no data or response
    try:
        if data['resultsCount'] <= 0:
            return
    except:
        print("an error occured")
    aggregates = data['results']
    open = aggregates[000]['o']
    threshold = open * 1.2
    for r in aggregates:
        if r['h'] > threshold:
            print(ticker)
            return ticker

"""response = requests.get('https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/minute' +
                        '/1686888000000/1686922200000?adjusted=true&sort=asc&limit=5000&apiKey=' + config.API_KEY)

data = response.json() # converts the HTTP response into a JSON object

results = data['results'] # creates a list of the 'results' in this JSON object to ignore unneeded info

for x in results:
    print(datetime.datetime.fromtimestamp(x['t'] / 1000))

print('\n')
print(datetime.datetime.fromtimestamp(1686888000000 / 1000))

print(datetime.datetime.fromtimestamp(1686907800000 / 1000))

for x in results:
    print (x['h']) """

isValidTicker("BRK.AWKND") ##test case for more "obscure" tickers

for y in range(0, len(config.tickers)):
    isValidTicker(config.tickers[y])


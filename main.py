#NOTE: Polygon API calls only return data for stocks listed on US stock exchanges.

import config, json, requests, datetime, pandas

def isValidTicker(ticker):
    openResponse = requests.get('https://api.polygon.io/v1/open-close/' + ticker + '/2021-07-30?adjusted=true&apiKey=' + config.API_KEY)

    openResponseJSON = openResponse.json()
    """TODO: Error handling. Possible error cases:
       1.) Stock is listed on an exchange outside of the US
       2.) The stock ticker has changed """
    try:
        open = openResponseJSON['open']
    except:
        print("an error occured trying to find the open price")
    #API call that returns all premarket data in the form of one minute candles for a certain ticker
    response = requests.get('https://api.polygon.io/v2/aggs/ticker/' + ticker + '/range/1/minute' +
                        '/1686888000000/1686922200000?adjusted=true&sort=asc&limit=5000&apiKey=' + config.API_KEY) 
    data = response.json()
    #TODO: need error handling for when the ticker yeilds no data or response
    try:
        if data['resultsCount'] <= 0: #'resultsCount' corresponds to the number of candles returned
            return
    except:
        print("an error occured trying to get premarket candles")
    aggregates = data['results'] #the list of candles 
    #open = aggregates[000]['o'] 
    threshold = open * 1.2
    for r in aggregates:
        if r['h'] > threshold:
            print(ticker)
            return ticker

#isValidTicker("BRK.AWKND") ##test case for more "obscure" tickers

for y in range(0, len(config.ConfirmationList)):
    isValidTicker(config.ConfirmationList[y])


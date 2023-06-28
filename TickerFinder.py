#file containing the methods whose main purpose is to find the tickers that perform well in the 
#premarket compared to previous close and other parameters

#NOTE: Polygon API calls only return data for stocks listed on US stock exchanges.

import requests, config, TimeConversion, datetime

def isValidTicker(ticker):
    date = "2021-08-02"
    PreMarketTimes = TimeConversion.DateToMilliseconds(date)

    URL = ('https://api.polygon.io/v1/open-close/' + ticker + '/' + date + 
                                '?adjusted=true&apiKey=' + config.API_KEY) #URL of the API request
    
    openResponse = requests.get(URL)

    openResponseJSON = openResponse.json()
    """TODO: Error handling. Possible error cases:
       2.) !! The stock ticker has changed """
    try:
        open = openResponseJSON['open']
    except:
        print("an error occured trying to find the open price")
    #API call that returns all premarket data in the form of one minute candles for a certain ticker
    response = requests.get('https://api.polygon.io/v2/aggs/ticker/' + ticker + '/range/1/minute' +
                        '/' + str(PreMarketTimes[0])+ '/' + str(PreMarketTimes[1]) +'?adjusted=true&sort=asc&limit=5000&apiKey=' + config.API_KEY) 
    data = response.json()
    #TODO: need error handling for when the ticker yeilds no data or response
    try:
        if data['resultsCount'] <= 0: #'resultsCount' corresponds to the number of candles returned
            return
    except:
        print("an error occured trying to get premarket candles")
    aggregates = data['results'] #the list of candles 
    threshold = ((open * 100 * 12) / 1000) #multiplies the open price by 1.2, prevents floating point errors
    for r in aggregates:
        if r['h'] > threshold:
            print(ticker)
            return ticker
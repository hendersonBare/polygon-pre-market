#file containing the methods whose main purpose is to find the tickers that perform well in the 
#premarket compared to previous close and other parameters

#NOTE: Polygon API calls only return data for stocks listed on US stock exchanges.

import requests, config, TimeConversion, datetime, logging

logging.basicConfig(level=logging.WARNING)

def isValidTicker(ticker, date):
    PreMarketTimes = TimeConversion.DateToMilliseconds(date)

    URL = ('https://api.polygon.io/v1/open-close/' + ticker + '/' + date + 
                                '?adjusted=true&apiKey=' + config.API_KEY) #URL of the git API request
    
    closeResponse = requests.get(URL)

    closeResponseJSON = closeResponse.json()
    """TODO: Error handling. Possible error cases:
       2.) !! The stock ticker has changed """
    try:
        close = closeResponseJSON['close']
    except:
        logging.info("an error occured trying to find the close price")
        return
    #API call that returns all premarket data in the form of one minute candles for a certain ticker
    response = requests.get('https://api.polygon.io/v2/aggs/ticker/' + ticker + '/range/1/minute' +
                        '/' + str(PreMarketTimes[0])+ '/' + str(PreMarketTimes[1]) +'?adjusted=true&sort=asc&limit=5000&apiKey=' + config.API_KEY) 
    data = response.json()
    #TODO: need error handling for when the ticker yeilds no data or response
    try:
        if data['resultsCount'] <= 0: #'resultsCount' corresponds to the number of candles returned
            return
    except:
        logging.info("an error occured trying to get premarket candles")
    aggregates = data['results'] #the list of candles 
    try:
        threshold = ((close * 100 * 12) / 1000) #multiplies the open price by 1.2, prevents floating point errors
    except UnboundLocalError:
        logging.info("UnboundLocalError occurred, issue finding close price")
        return
    for r in aggregates:
        if r['h'] > threshold:
            print(ticker)
            return ticker
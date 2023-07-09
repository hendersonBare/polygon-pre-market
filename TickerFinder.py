#file containing the methods whose main purpose is to find the tickers that perform well in the 
#premarket compared to previous close and other parameters

#NOTE: Polygon API calls only return data for stocks listed on US stock exchanges.

"""OPTIMIZE: The 2 approaches I could come up with for adding data to the database are as follows:
1.) Go ahead and create a table for every single ticker and its values, if not a single datapoint is above the threshold
then delete the table
    Problems: overhead cost of creating a table paid for every single ticker
    Have to add data to a database that will most likely not be used
2.) If the threshold is met, create the table, add the ticker to the databse of tickers for that day,
then reiterate over the results of the API call and add them to the databse
    Problems: redundant iterations

NOTE: for now, using #2
"""

import requests, config, TimeConversion, datetime, logging, pyodbc

logging.basicConfig(level=logging.WARNING)

def isValidTicker(ticker, date, cursor):
    createTickerTable(date, cursor)
    close = getClosePrice(date, ticker)
    if (close == -1): return

    aggregates = getAggregates(date, ticker)

    try:
        threshold = ((close * 100 * 12) / 1000) #multiplies the previous close price by 1.2, prevents floating point errors
    except UnboundLocalError:
        logging.info("UnboundLocalError occurred, issue finding close price")
        return
    for r in aggregates:
        if r['h'] > threshold:
            print(ticker)
            addTickerToDateTable(date, cursor, ticker)
            createTickerAggregateTable(date, cursor, ticker, aggregates)
            return ticker

        
def getClosePrice(date, ticker):
    previousDay = TimeConversion.decreaseDayByOne(date)
    openCloseURL = ('https://api.polygon.io/v1/open-close/' + ticker + '/' + previousDay + 
                                '?adjusted=true&apiKey=' + config.API_KEY) #URL of the git API request
    
    closeResponse = requests.get(openCloseURL)

    closeResponseJSON = closeResponse.json()
    """TODO: Error handling. Possible error cases:
       2.) !! The stock ticker has changed """
    try:
        close = closeResponseJSON['close']
    except:
        logging.info("an error occured trying to find the close price")
        return -1
    return close



def getAggregates(date, ticker):
    PreMarketTimes = TimeConversion.DateToMilliseconds(date)

    aggregatesURL = ('https://api.polygon.io/v2/aggs/ticker/' + ticker + '/range/1/minute' +
                        '/' + str(PreMarketTimes[0])+ '/' + str(PreMarketTimes[1]) +'?adjusted=true&sort=asc&limit=5000&apiKey=' + config.API_KEY)
    #API call that returns all premarket data in the form of one minute candles for a certain ticker
    response = requests.get(aggregatesURL) 

    data = response.json()
    #TODO: need error handling for when the ticker yeilds no data or response
    try:
        if data['resultsCount'] <= 0: #'resultsCount' corresponds to the number of candles returned
            return [] #returns empty list
    except:
        logging.info("an error occured trying to get premarket candles")
    return data['results'] #the list of candles 

def createTickerTable(date, cursor):
    dateString = date.replace("-", "")
    createTableCommand = ("IF OBJECT_ID(N'dbo.Table_" + dateString + "', N'U') IS NULL" + 
                          '\n' + "BEGIN" + '\n' + '\t' + 'CREATE TABLE Table_' + dateString + '(' + '\n'
                          + '\t' + 'TickerName varchar(50));' + '\n' + 'END'
                          )
    cursor.execute(createTableCommand)
    cursor.commit()

def addTickerToDateTable(date, cursor, ticker):
    dateString = date.replace("-", "")
    addTickerCommand = ("INSERT INTO Table_" + dateString + " (TickerName)" + '\n' +
                     "VALUES ('" + ticker + "');")
    cursor.execute(addTickerCommand)
    cursor.commit()

def createTickerAggregateTable(date, cursor, ticker, aggregates):
    dateString = date.replace("-", "")
    createTableCommand = ("IF OBJECT_ID(N'dbo.Table_" + ticker + "_" + dateString +"', N'U') IS NULL" + 
                          '\n' + "BEGIN" + '\n' + '\t' + 'CREATE TABLE Table_' + ticker +"_"+ dateString + '(' + 
                          '[open] FLOAT,'  + '\n' + 
                          '\t' + '[close] FLOAT,' + '\n' +
                          '\t' + '[high] FLOAT,' + '\n' +
                          '\t' + '[low] FLOAT,' + '\n' +
                          '\t' + '[volumeWeighted] FLOAT,' + '\n' +
                          '\t' + '[numberOfTransactions] int,' + '\n' +
                          '\t' + '[timestamp] int' +
                          ');' + '\n' + 'END'
                          )
    cursor.execute(createTableCommand)
    cursor.commit()
    insertDataCommand = ""
    for result in aggregates:
        insertDataCommand = ("INSERT INTO Table_" + ticker +"_"+ dateString + 
                             " ([open], [close], [high], [low], [volumeWeighted], [NumberOfTransactions], [timestamp]) \n" 
                             + "( {}, {}, {}, {}, {}, {}, {} )".format(result['o'], result['c'], result['h'], result['l'],
                                                                       result['vw'], result['n'], result['t']) )
        cursor.execute(insertDataCommand)
        cursor.commit()
    return
"""a class used to experiment with the logic used to calculate RSI values"""

import TickerFinder, config, datetime

#date = "2023-08-17"
#ticker = 'AAPL'

#resultArray = TickerFinder.getAggregates(date, ticker)

def buildRSI(date, ticker):
    resultArray = TickerFinder.getRSI(date, ticker)
    resultArray.reverse()
    gains = [0] * 14 #list for average gains between data points
    losses = [0] * 14 #list for average losses between data points
    i = 0
    while (i < 14):
        try:
            diff = resultArray[i+1]['c'] - resultArray[i]['c'] #how much the price changed 
        except:
            return
        percentChange = (diff / resultArray[i]['c']) * 100 #the percentage of change from i
        if percentChange > 0:
            gains[i] = percentChange #greater than zero is a gain
        else:
            losses[i] = abs(percentChange) #less than zero is a loss (zero gets added anyways)
        i +=1

    avgPercentageGain = (gains[0] + gains[1] + gains[2] + gains[3] + gains[4] + gains[5] + gains[6] + gains[7] + gains[8] + gains[9] + gains[10] + gains[11] + gains[12] + gains[13]) / 14
    avgPercentageLoss = (losses[0] + losses[1] + losses[2] + losses[3] + losses[4] + losses[5] + losses[6] + losses[7] + losses[8] + losses[9] + losses[10] + losses[11] + losses[12] + losses[13]) / 14

    relativeStrength = avgPercentageGain / avgPercentageLoss

    relativeStrengthIndex = 100 - (100 / (1 + relativeStrength))
    return relativeStrengthIndex, gains, losses, float(resultArray[14]['c'])

# A function used to calculate the RSI for each trade of a stock

def CalculateRSI(date, ticker, resultArray):
    listOfRSIs = [] # list to be returned
    buildRSIResults = buildRSI(date, ticker) # obtains data from previous data points
    gains = buildRSIResults[1]
    losses = buildRSIResults[2]
    j, i = 0, 0
    percentChange = 0
    prevResult = buildRSIResults[3] # the last close price
    listBarrier = len(resultArray) - 1 # cap of indexing value
    while i < 14:
        diff = resultArray[j]['c'] - prevResult # subtracts current close price from previous close price to find difference
        percentChange = (diff / prevResult) * 100
        if percentChange > 0:
            gains[i] = percentChange #greater than zero is a gain
        else:
            losses[i] = abs(percentChange) #less than zero is a loss (zero gets added anyways)
        avgPercentageGain = (gains[0] + gains[1] + gains[2] + gains[3] + gains[4] + gains[5] + gains[6] + gains[7] + gains[8] + gains[9] + gains[10] + gains[11] + gains[12] + gains[13]) / 14
        avgPercentageLoss = (losses[0] + losses[1] + losses[2] + losses[3] + losses[4] + losses[5] + losses[6] + losses[7] + losses[8] + losses[9] + losses[10] + losses[11] + losses[12] + losses[13]) / 14
        if (avgPercentageGain == 0 | avgPercentageLoss == 0):
            relativeStrength = 0
        else:
            relativeStrength = avgPercentageGain / avgPercentageLoss
        relativeStrengthIndex = 100 - (100 / (1 + relativeStrength))
        listOfRSIs.append(relativeStrengthIndex)
        prevResult = resultArray[j]['c']
        if j < listBarrier:
            if i == 13:
                i = 0 # resets i back to 0 since we are using a circular array
            else:
                i += 1
            j+=1
        else:
            break

    return listOfRSIs

#RSI = CalculateRSI(date, ticker, TickerFinder.getAggregates(date, ticker))
#print('done Running!')
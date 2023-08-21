import TickerFinder, config, datetime

def buildMACD(date, ticker, aggregates):
    MACDList = []
    results = TickerFinder.getMACD(date, ticker)
    EMA12day = (results[0] + results[1] + results[2] + results[3] + results[4] + results[5] + results[6] + 
                results[7] + results[8] + results[9] + results[10] + results[11]) / 12
    
    EMA26day = (results[0] + results[1] + results[2] + results[3] + results[4] + results[5] + results[6] + 
                results[7] + results[8] + results[9] + results[10] + results[11] + 
                results[12] + results[13] + results[14] + results[15] + results[16] + results[17] + results[18] + 
                results[19] + results[20] + results[21] + results[22] + results[23] + results[24] + results[25]) / 26
    
    
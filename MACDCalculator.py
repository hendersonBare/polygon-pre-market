import TickerFinder

def buildMACD(date, ticker, aggregates):
    MACDList = []
    results = TickerFinder.getMACD(date, ticker)
    MACD = 0
    EMA12day = (results[0]['c'] + results[1]['c'] + results[2]['c'] + results[3]['c'] + results[4]['c'] + results[5]['c'] + results[6]['c'] + 
                results[7]['c'] + results[8]['c'] + results[9]['c'] + results[10]['c'] + results[11]['c']) / 12
    
    EMA26day = (results[0]['c'] + results[1]['c'] + results[2]['c'] + results[3]['c'] + results[4]['c'] + results[5]['c'] + results[6]['c'] + 
                results[7]['c'] + results[8]['c'] + results[9]['c'] + results[10]['c'] + results[11]['c'] + 
                results[12]['c'] + results[13]['c'] + results[14]['c'] + results[15]['c'] + results[16]['c'] + results[17]['c'] + results[18]['c'] + 
                results[19]['c'] + results[20]['c'] + results[21]['c'] + results[22]['c'] + results[23]['c'] + results[24]['c'] + results[25]['c']) / 26
    
    for result in aggregates:
        EMA12day = (result['c'] * (2/(13))) + (EMA12day * (1-(2/(13))))
        EMA26day = (result['c'] * (2/(27))) + (EMA12day * (1-(2/(27))))
        MACD = EMA12day - EMA26day
        MACDList.append(MACD)
    return MACDList
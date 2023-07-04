import TickerFinder, config, datetime
file = open('NASDAQ_screener_tickers.txt', "r")

lines = file.readlines()

NASDAQ_Tickers = [line.strip() for line in lines]

file.close()

#rough iteration through dates

date = datetime.datetime.strptime("2023-06-30", "%Y-%m-%d")
date = date - datetime.timedelta(days=1)
dateString = date.strftime("%Y-%m-%d")

for x in range(0, 3):
    date = date - datetime.timedelta(days=1)
    dateString = date.strftime("%Y-%m-%d")
    for y in range(0, len(NASDAQ_Tickers)):
        TickerFinder.isValidTicker(NASDAQ_Tickers[y], dateString)


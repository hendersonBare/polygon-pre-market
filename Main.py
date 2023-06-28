import TickerFinder, config
file = open('NASDAQ_screener_tickers.txt', "r")

lines = file.readlines()

NASDAQ_Tickers = [line.strip() for line in lines]

file.close()

for y in range(0, len(NASDAQ_Tickers)):
    TickerFinder.isValidTicker(NASDAQ_Tickers[y])


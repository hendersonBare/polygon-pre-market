import TickerFinder, config, Webscrape

NASDAQ_Tickers = Webscrape.main()

for y in range(0, len(NASDAQ_Tickers)):
    TickerFinder.isValidTicker(NASDAQ_Tickers[y])


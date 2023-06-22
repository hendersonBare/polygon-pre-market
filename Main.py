import TickerFinder, config

for y in range(0, len(config.ConfirmationList)):
    TickerFinder.isValidTicker(config.ConfirmationList[y])


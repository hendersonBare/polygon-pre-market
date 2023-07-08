import TickerFinder, config, datetime, pyodbc

connection_string = 'DRIVER={SQL Server};SERVER=' + config.server + ';DATABASE=' + config.database + ';Trusted_Connection=yes;'

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

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
        TickerFinder.isValidTicker(NASDAQ_Tickers[y], dateString, cursor)

connection.close()
cursor.close()
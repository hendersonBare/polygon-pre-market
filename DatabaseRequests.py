import config, pyodbc

connection_string = 'DRIVER={SQL Server};SERVER=' + config.server + ';DATABASE=' + config.database + ';Trusted_Connection=yes;'

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()



def requestDate(dateValue):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    dateValue = dateValue.replace("-", "")
    dateTableRequest = "SELECT TickerName FROM Table_" + dateValue
    cursor.execute(dateTableRequest)
    tickers = cursor.fetchall()
    returnValue = []
    for row in tickers:
        returnValue.append(row[0])

    cursor.close()
    connection.close()

    return returnValue
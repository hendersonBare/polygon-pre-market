import config, pyodbc

connection_string = 'DRIVER={SQL Server};SERVER=' + config.server + ';DATABASE=' + config.database + ';Trusted_Connection=yes;'

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()



def requestDate(dateValue):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor() ##why is this here, redundant

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

def requestTable(tableName):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor() ##why is this here, redundant

    tableName = tableName.replace("-", "")
    tableDataRequest = 'SELECT [open], [close], [high], [low], [volumeWeighted], [numberOfTransactions], [timestamp] FROM ' + tableName
    cursor.execute(tableDataRequest)
    data = cursor.fetchall()
    listOfLists = []
    for cursorDescription in data:  
        newList = []
        for item in cursorDescription:
            newList.append(item)
        listOfLists.append(newList)

    return listOfLists

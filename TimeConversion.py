# A simple file with a method that converts a specified date time to time in milliseconds

import datetime
import re

#Since the only uses of dates are for premarket data (milliseconds) or the date of
#the previous close, we will be converting the date to milliseconds with the times
#of premarket trading appended to the date

#given a date in a human readable format, we want the millisecond timestamps for 
#2am and 7:30am the next day
def DateToMilliseconds(humanReadableDate):

    openTimeObj = datetime.datetime.strptime(humanReadableDate + " 2:00:00", '%Y-%m-%d %H:%M:%S')
    openTimeMillisec = int(openTimeObj.timestamp() * 1000)

    closeTimeObj = datetime.datetime.strptime(humanReadableDate + " 7:30:00", '%Y-%m-%d %H:%M:%S')
    closeTimeMillisec = int(closeTimeObj.timestamp() * 1000)

    #return openTimeMillisec  + 86400000, closeTimeMillisec + 86400000, this line returns timestamps the day after
    return openTimeMillisec, closeTimeMillisec


#converts a string in yyyy-mm-dd format into a date object then decrements by one
def decreaseDayByOne(date):
    dateObj = datetime.datetime.strptime(date, "%Y-%m-%d")
    dateObj = dateObj - datetime.timedelta(days=1)
    DateString = dateObj.strftime("%Y-%m-%d")
    return DateString
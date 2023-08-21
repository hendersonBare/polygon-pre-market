# A simple file with a method that converts a specified date time to time in milliseconds

import datetime
import re

#Since the only uses of dates are for premarket data (milliseconds) or the date of
#the previous close, we will be converting the date to milliseconds with the times
#of premarket trading appended to the date

#given a date in a human readable format, we want the millisecond timestamps for 
#2am and 4pm the next day
def DateToMilliseconds(humanReadableDate):

    openTimeObj = datetime.datetime.strptime(humanReadableDate + " 5:00:00", '%Y-%m-%d %H:%M:%S')
    openTimeMillisec = int(openTimeObj.timestamp() * 1000)

    closeTimeObj = datetime.datetime.strptime(humanReadableDate + " 14:00:00", '%Y-%m-%d %H:%M:%S')
    closeTimeMillisec = int(closeTimeObj.timestamp() * 1000)

    openTimePrevious = datetime.datetime.strptime(humanReadableDate + " 5:00:00", '%Y-%m-%d %H:%M:%S')
    openTimePrevious = openTimePrevious - datetime.timedelta(days=1)
    openTimePreviousMillisec = int(openTimePrevious.timestamp() * 1000)

    closeTimePrevious = datetime.datetime.strptime(humanReadableDate + " 4:00:00", '%Y-%m-%d %H:%M:%S')
    closeTimePreviousMillisec = int(closeTimePrevious.timestamp() * 1000)

    #return openTimeMillisec  + 86400000, closeTimeMillisec + 86400000, this line returns timestamps the day after
    return openTimeMillisec, closeTimeMillisec, openTimePreviousMillisec, closeTimePreviousMillisec


#converts a string in yyyy-mm-dd format into a date object then decrements by one
def decreaseDayByOne(date):
    dateObj = datetime.datetime.strptime(date, "%Y-%m-%d")
    dateObj = dateObj - datetime.timedelta(days=1)
    DateString = dateObj.strftime("%Y-%m-%d")
    return DateString

#used when less than 14 trades are made in the previous day when checking for historical
#data to calculate RSI
#reason for this computation is to hopefully expand the window to return enough results to calculate the RSI
def decreaeDayMillisecond(timeStamp):
    input_datetime = datetime.fromtimestamp(timeStamp / 1000.0)

    # Subtract one day
    result_datetime = input_datetime - datetime.timedelta(days=2)

# Convert datetime back to millisecond timestamp
    result_timestamp_ms = int(result_datetime.timestamp() * 1000)
    return result_timestamp_ms
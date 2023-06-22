# A simple file with a method that converts a specified date time to time in milliseconds

from datetime import datetime
import re

#Since the only uses of dates are for premarket data (milliseconds) or the date of
#the previous close, we will be converting the date to milliseconds with the times
#of premarket trading appended to the date

#given a date in a human readable format, we want the millisecond timestamps for 
#2am and 7:30am the next day
def DateToMilliseconds(humanReadableDate):

    openTimeObj = datetime.strptime(humanReadableDate + " 2:00:00", '%Y-%m-%d %H:%M:%S')
    openTimeMillisec = int(openTimeObj.timestamp() * 1000)

    closeTimeObj = datetime.strptime(humanReadableDate + " 7:30:00", '%Y-%m-%d %H:%M:%S')
    closeTimeMillisec = int(closeTimeObj.timestamp() * 1000)

    return openTimeMillisec, closeTimeMillisec

print(DateToMilliseconds("2021-7-30")[0])
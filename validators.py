################################

#Author: Andreas Gölz

#This document is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License, version 3, 
#as published by the Free Software Foundation. 

############################### 

import re
import datetime

def validatemail(email): #Eine Email, nach der Email kann in das Textfeld beliebiger Text geschrieben werden.

    if(len(email)<1):
        return True
    
    regex = re.compile(r'(([A-Za-z0-9]+[.\-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+){1}.*')
    
    if re.fullmatch(regex, email):
        return True
    
    return False

def validatetime(time):
    
    if(len(time)<1):
        return False
    
    regex = re.compile("([0-9][0-9]):([0-9][0-9])")
    
    if re.fullmatch(regex, time):
        return True
    
    return False

def validatedatum(d):
    match = re.search("([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])", d)

    res = False
    
    if match != None:
        res = True

    else:
        return False

    year = d.split("-")[0]
    month = d.split("-")[1]
    day = d.split("-")[2]

    if len(year) < 4:
        res = False 

    if len(month) != 2 or int(month) > 12 or month == "00":
        res = False
    
    if len(day) != 2 or day == "00":
        res = False

    _31er = ["01", "03", "05", "07", "08", "10", "12"] 

    _30er = ["04", "06", "09", "11"]

    ly = isLeapYear(year)
    
    if ly and month == "02" and int(day) > 29:
        res = False   
    
    elif not ly and month == "02" and int(day) > 28:
        res = False  
 
 
    if month in _31er:
        if int(day) > 31:
            res = False 
 
    elif month in _30er:
        if int(day) > 30:
            res = False 
 
    return res


def isLeapYear(y):
    year = int(y)
    
    res = False
    
    if (year % 400 == 0) and (year % 100 == 0):
        res = True
    
    elif (year % 4 ==0) and (year % 100 != 0):
        res = True

    else:
        res = False

def isDateBetween(start, input, end):
    if len(start) < 1 or len(input) < 1 or len(end) < 1:
        return False
    
    startdate = start.split(" ")[0]
    
    startyear = startdate.split("-")[0]
    startmonth = startdate.split("-")[1]
    startday = startdate.split("-")[2]
    
    starttime = start.split(" ")[1]
    
    starthour = starttime.split(":")[0]
    startminute = starttime.split(":")[1]
    
    inputdate = input.split(" ")[0]
    
    inputyear = inputdate.split("-")[0]
    inputmonth = inputdate.split("-")[1]
    inputday = inputdate.split("-")[2]
    
    inputtime = input.split(" ")[1]
    
    inputhour = inputtime.split(":")[0]
    inputminute = inputtime.split(":")[1]
    

    enddate = end.split(" ")[0]
    
    endyear = enddate.split("-")[0]
    endmonth = enddate.split("-")[1]
    endday = enddate.split("-")[2]
    
    endtime = end.split(" ")[1]
    
    endhour = endtime.split(":")[0]
    endminute = endtime.split(":")[1]
    
    
    d1 = datetime.datetime(int(startyear), int(startmonth), int(startday), int(starthour), int(startminute))
    d2 = datetime.datetime(int(inputyear), int(inputmonth), int(inputday), int(inputhour), int(inputminute))
    d3 = datetime.datetime(int(endyear), int(endmonth), int(endday), int(endhour), int(endminute))

    res = d1 <= d2 <= d3
    return res
 
def validategebtag(gebtag): #YYYY-MM-DD
    
    if(len(gebtag)<1):
        return True
    
    match = re.search("([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])", gebtag)
    
    if match != None:
        return True
    
    return False
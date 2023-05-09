from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from json import dumps
from datetime import datetime
import pytz

TimeZoneCities = {
    "America/New_York":"New York",
    "Asia/Seoul":"Seoul",
    "America/Panama":"Texas",
    "America/Montreal":"Montreal",
    "Europe/Zurich":"Zurich",
    "Asia/Singapore":"Singapore",
    "Asia/Taipei":"Taipei",
    "Asia/Shanghai":"Shanghai",
    "Australia/Sydney":"Sydney",
    "Australia/Brisbane":"Brisbane",
    "Pacific/Honolulu":"Honolulu",
    "America/Los_Angeles":"Los Angeles",
    "America/Vancouver":"Vancouver",
    "America/Boise":"Boise",
    "America/Chicago":"Chicago",
    "Europe/London":"London",
    "Europe/Berlin":"Berlin",
    "Europe/Paris":"Paris",
    "Europe/Rome":"Rome",
}

# Create your views here.
def timeconvert(request):

    # get the standard UTC time
    #original = pytz.utc

    #ZoneSelections = pytz.all_timezones
    TimeZoneKeys = TimeZoneCities.keys() # Get the keys for pytz.timezone parameter

    LocalTimesDict = {}
    for TimeZoneKey in TimeZoneKeys:
        dateTimeObj = datetime.now(pytz.timezone(TimeZoneKey))
#        LocalTimesDict[timeZone] = dateTimeObj.strftime('%Y%m%d %H%M%S %Z %z')
        # Get 'city name' Value to pass as Key to the dictionary of LocalTimesDict to display
        LocalTimesDict[TimeZoneCities[TimeZoneKey]] = dateTimeObj.strftime('%I:%M %p, %A, %b %d, %Y')

    # it will get the time zone
    # of the specified location
    #for timeZone in pytz.all_timezones
    #    if 'Indian/' in timeZone
    #        dateTimeObj = datetime.now(pytz.timezone(timeZone))
    #        print(timeZone,"",dateTimeObj.strftime('%Y%m%d %H%M%S %Z %z'))

    return render(request, 'worldtime/timeconvert.html', {
        #"ZoneSelections": TimeZoneCities,
        "LocalTimes": LocalTimesDict,
    })

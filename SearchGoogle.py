# from /usr/lib/python2.6/site-packages import argparse


import imp


import httplib2
import os
import sys
sys.path.remove('/usr/lib/python2.6/site-packages')
# foo = imp.load_source('argparse.py', '/usr/lib/python2.6/site-packages/')
import argparse
from datetime import datetime
#import tzlocal
#import pytz 

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools


CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/calendar.readonly',
    ],
    message=tools.message_if_missing(CLIENT_SECRETS))


def googleSearch(userId, startTimeParam, startDate, endTime, endDate):
  
  #used from the google reference code
  storage = file.Storage('sample.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    ##print credentials
    credentials = tools.run_flow(FLOW, storage, flags)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  # Construct the service object for the interacting with the Calendar API.
  service = discovery.build('calendar', 'v3', http=http)

  try:
    #put the tz as 0000 so it searches the calendar with no timezone change, will handle this after
    tz = "-0000"
    page_token = None
    #put the start time string togetheradd 01 for the seconds or else it wont get the item starting at that exact time, whcih I want
    myStartTime = startDate + "T" + startTimeParam + ":01" + tz 
    #end time  string put together  add :00 for the seconds or else it fails
    myEndTime = endDate + "T" + endTime + ":00" + tz
    
    while True:
		#get the calendar id is always the onid plus this email or else it wont work
      #calendarID = userId + "@onid.oregonstate.edu"
      calendarID = "cs419.team4@gmail.com"
      
      startTime = "startTime"
      
	  #we run into an issue if the calendar iddoesnt exist
      try:
		#when we get the events
		#order by the start time, have it all as single events, min and max time are our parameters we put in 
		#also we are having it return in the time zone of the local machine, not useful for full day events but very helpful for datetime events
        events = service.events().list(calendarId=calendarID, pageToken=page_token, orderBy=startTime, singleEvents=True, timeMin=myStartTime, timeMax=myEndTime).execute()
      except:
	    #when we get an error from the events return, normally meaning a bad onid id
        events = "NoID"
	
      if not page_token:
        break
      
      
  except client.AccessTokenRefreshError:
    pass
    #print ("The credentials have been revoked or expired, please re-run the application to re-authorize")

  return events


if __name__ == '__main__':
  main(sys.argv)

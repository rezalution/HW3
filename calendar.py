#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import httplib2
import os
import sys
import datetime
 
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run
 
# Calendar id for reading.
CALENDAR_ID = 'cs419.team4@gmail.com'
 
# Path to the credential files.
BASE_DIR = lambda x: os.path.join(os.path.dirname(__file__), x)
 
CLIENT_SECRETS_PATH = BASE_DIR('client_secrets.json')
STORAGE_PATH = BASE_DIR('read_calendar.dat')
 
# Set up a Flow object to be used for authentication.
FLOW = flow_from_clientsecrets(CLIENT_SECRETS_PATH, scope=[
    'https://www.googleapis.com/auth/calendar.readonly',
])
 
 
def get_calendar_service():
    storage = Storage(STORAGE_PATH)
    credentials = storage.get()
 
    if credentials is None or credentials.invalid:
        credentials = run(FLOW, storage)
 
    http = httplib2.Http()
    http = credentials.authorize(http)
 
    service = build('calendar', 'v3', http=http)
    return service
 
 
class OneDayEvent(object):
    def __init__(self, start_time, end_time, summary, creator):
        if start_time is None:
            assert(end_time is None)
        self.start_time = start_time
        self.end_time = end_time
        self.summary = summary
        self.creator = creator
 
    def __lt__(self, that):
        if self.start_time is None and that.start_time is None:
            return self.summary < that.summary
        if self.start_time is None or that.start_time is None:
            return self.start_time is None
        return (self.start_time, self.end_time, self.summary, self.creator) < (
            that.start_time, that.end_time, that.summary, that.creator)
 
    def __str__(self):
        if self.start_time is None:
            tm = u'終日'
        else:
            f = lambda x: datetime.datetime.strftime(x, '%H:%M')
            tm = '%s-%s' % (f(self.start_time), f(self.end_time))
        return u'[%s] %s (%s)' % (tm, self.summary, self.creator)
 
 
def read_events(date):
    """Returns sorted list of OneDayEvent objects."""
 
    def format(x):
        return datetime.datetime.strftime(x, '%Y-%m-%dT%H:%M:%SZ')
 
    time_min = datetime.datetime.combine(date, datetime.time())
    time_max = time_min + datetime.date.resolution
 
    time_min, time_max = map(format, (time_min, time_max))
 
    service = get_calendar_service()
    events = service.events().list(
        calendarId=CALENDAR_ID, timeMin=time_min, timeMax=time_max).execute()
 
    def f(x):
        y = x.get('dateTime')
        if y:
            z = datetime.datetime.strptime(y[:-6], '%Y-%m-%dT%H:%M:%S')
            return datetime.datetime.combine(date, z.time())
 
    ret = [OneDayEvent(
        f(event['start']), f(event['end']), event['summary'],
        event['creator']['displayName']) for event in events['items']]
    ret.sort()
    return ret
 
 
def main(argv):
    offset = int(argv[1]) if len(argv) >= 2 else 0
 
    for event in read_events(
            datetime.date.today() + datetime.date.resolution * offset):
        print(unicode(event))
 
if __name__ == '__main__':
    main(sys.argv)
#! /usr/bin/env python

from api_app import main

class CalAp():
    
    def __init__(self):
        self.service = main()

    # Returns a list of calendars formatted as calendar objects.
    def list_calendars(self):
        page_token = None
        results = []
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                results.append(calendar_list_entry['summary'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return results

    # Returns a list of events formatted as strings.
    def list_events(self, calendarId):
        page_token = None
        results = []
        while True:
            events = self.service.events().list(calendarId=calendarId, pageToken=page_token).execute()
            for event in events['items']:
                results.append(event['summary'])
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return results
    
    # Returns a dictionary of events formatted as Event objects.
    def get_events(self, calendarId):
        page_token = None
        results = []
        while True:
            events = self.service.events().list(calendarId=calendarId, pageToken=page_token).execute()
            for event in events['items']:
                results.append(Event(event))
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return results
        
    # Returns an Event object representing the given event ID.
    def get_event(self, calendarId, eventId)
        event = self.service.events().get(calendarId=calendarId, eventId=eventId).execute()
        return Event(event)

    # Adds an event to the calendar.
    def add_event(self, calendarId, event):
        created_event = self.service.events().insert(calendarId=calendarId, body=event).execute()
        return created_event['id']

    def remove_event(self, calendarId, event):
        try:
            self.service.events().delete(calendarId=calendarId, eventId=event.id).execute()
            return 1
        except:
            return 0


# Provides utilities for Event objects through the CalAp.get_events function.
class Event:

    def __init__(self, event):
        self.id = event['id']
        self.summary = event['summary']
        try:
            self.description = event['description']
        except:
            self.description = None
        try:
            _start = event['start']['dateTime']
            _end = event['end']['dateTime']
            self.startDate = _start.split("T")[0]
            self.startTime = _start.split("T")[1].split("-")[0]
            self.endDate = _end.split("T")[0]
            self.endTime = _end.split("T")[1].split("-")[0]
            self.allday = False
        except:
            _start = event['start']['date']
            _end = event['end']['date']
            self.startDate = _start
            self.startTime = None
            self.endDate = _end
            self.endTime = None
            self.allday = True


    def __repr__(self):
        return '%s(%s)' % (self.__class__, self.summary)

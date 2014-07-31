#! /usr/bin/env python

from calap import CalAp
from datetime import datetime

calap = CalAp()

print '\n'
print '*******'
print 'TESTING'
print '*******'

print '\nlist_calendars'
print '**************'
cals = calap.list_calendars()
for cal in cals:
    print cal

print '\nlist_events'
print '***********'
cal = calap.list_calendars()[0]
events = calap.list_events(cal)
for event in events:
    print event

print '\nget_events'
print '**********'
cal = calap.list_calendars()[0]
events = calap.get_events(cal)
for event in events:
    print 'Event Object     ', event
    print 'Event ID         ', event.id
    print 'Event Name       ', event.summary
    print 'Event Description', event.description
    print 'Event All Day?   ', event.allday
    print 'Event Start Date ', event.startDate
    print 'Event Start Time ', event.startTime
    print 'Event End Date   ', event.endDate
    print 'Event End Time   ', event.endTime
    print '\n'
    
print '\nget_event'
print '*********'
cal = calap.get_event(cal, eventId)[0]
eventId = calap.get_events(cal)[0].id
event = calap.get_event(cal, eventId)
print 'Event Object     ', event
print 'Event ID         ', event.id
print 'Event Name       ', event.summary
print 'Event Description', event.description
print 'Event All Day?   ', event.allday
print 'Event Start Date ', event.startDate
print 'Event Start Time ', event.startTime
print 'Event End Date   ', event.endDate
print 'Event End Time   ', event.endTime
print '\n'

print '\nadd_event'
print '*********'
event = {
    'summary': 'Appointment',
    'location': 'Somewhere',
    'start': {
             'dateTime': '2013-01-12T10:00:00.000-07:00'
             },
    'end': {
           'dateTime': '2011-06-12T10:25:00.000-07:00'
           }
    }
cal = calap.list_calendars()[0]
newEventId = calap.add_event(cal, event)
print 'New event ID', newEventId

print '\nremove_event'
print '************'
cal = calap.list_calendars()[0]
event = calap.get_event(cal, newEventId)
print 'Event deletion (1/0)', calap.remove_event(cal, event)

print '\n'

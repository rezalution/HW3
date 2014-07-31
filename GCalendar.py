from oauth2client import file
from oauth2client import client
from oauth2client import tools
from apiclient import discovery
import os
import argparse
import httplib2
import dateutil.parser
from dateutil import tz
from datetime import datetime
from datetime import timedelta

__author__ = 'Patrick'


# manages a google calendar account, has a list of calendars with a list of events
class GCalendar:
    def authorize(self, credentials):
        http = httplib2.Http()
        http = credentials.authorize(http)
        self._service = discovery.build('calendar', 'v3', http=http)

    def __init__(self, secrets_filename, args, credentials_filename='calendar.dat'):
        self._parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[tools.argparser]
        )
        self._secrets_filename = os.path.join(os.path.dirname(__file__), secrets_filename)
        self._flow = client.flow_from_clientsecrets(
            self._secrets_filename,
            scope=['https://www.googleapis.com/auth/calendar.readonly'],
            message=tools.message_if_missing(self._secrets_filename)
        )
        self._service = None

        flags = self._parser.parse_args(args[1:])
        storage = file.Storage(credentials_filename)
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            credentials = tools.run_flow(self._flow, storage, flags)

        self.authorize(credentials)

    # @brief    retrieves the list of calendars from google
    # @return   a list of CalendarData representing all of the current user's calendars
    def get_calendar_list(self):
        ret = list()
        page_token = None
        while True:
            calendar_list = self._service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                ret.append(CalendarData(calendar_list_entry, self._service))
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return ret


# converts a datetime to RFC 3339 format (for google)
def time_to_rfc3339(time):
    return time.strftime('%Y-%m-%dT%H:%M:%S-00:00')


class CalendarData:
    def __init__(self, calendar_entry, service):
        self.id = calendar_entry['id']
        self.selected = calendar_entry['selected']
        self.summary = calendar_entry['summary']
        self._service = service
        self.events = list()

        self.refresh_events()

    def refresh_events(self):
        page_token = None
        self.events = list()
        today = datetime.utcnow()
        tomorrow = today + timedelta(days=1)

        while True:
            events = self._service.events().list(
                calendarId=self.id,
                pageToken=page_token,
                orderBy='startTime',
                singleEvents=True,
                timeMin=time_to_rfc3339(today),
                timeMax=time_to_rfc3339(tomorrow)
            ).execute()
            for event in events['items']:
                self.events.append(CalendarEvent(event))
            page_token = events.get('nextPageToken')
            if not page_token:
                break


# defines a calendar event
class CalendarEvent:
    def __init__(self, event_entry):
        my_zone = tz.tzlocal()
        self.summary = event_entry.get('summary', '')
        self.description = event_entry.get('description', '')
        start_entry = event_entry['start']
        if start_entry.get('date'):
            self.start = dateutil.parser.parse(start_entry['date'])
        elif start_entry.get('dateTime'):
            self.start = dateutil.parser.parse(start_entry['dateTime']).astimezone(my_zone)

        end_entry = event_entry['end']
        if end_entry.get('date'):
            self.end = dateutil.parser.parse(end_entry['date'])
        elif end_entry.get('dateTime'):
            self.end = dateutil.parser.parse(end_entry['dateTime']).astimezone(my_zone)

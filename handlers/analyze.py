from calendar import timegm
from collections import defaultdict
from collections import OrderedDict
from datetime import datetime
from datetime import timedelta
import json
import logging
from pprint import pformat

from google.appengine.api import users
from google.appengine.ext import webapp
from oauth2client.client import AccessTokenRefreshError

from handlers.env import decorator
from handlers.env import service
from handlers.env import template_engine
from utils.calendar import num_working_days
from utils.calendar import str_to_datetime
from utils.gae import get_all_items
from utils.gae import get_cal_name

DEFAULT_WEEKS = 4
"""Default number of weeks to look back"""

WORK_DAY_START = 9
"""Start of the work day"""

WORK_DAY_END = 19
"""End of the work day"""

WEEKDAY_TO_STR = OrderedDict([
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    ])
"""Lookup of weekday num -> day"""

DEFAULT_CAL_ID = 'primary'
"""Default calendar id to analyze"""


def _get_events(cal_id, time_min, time_max):
    """
    Retrieve events from the Google API

    @param cal_id: str, calendar id
    @param time_min: datetime, from time
    @param time_max: datetime, to time
    @return: list(events)
    """
    params = dict(
        calendarId=cal_id,
        singleEvents=True,
        timeMin=time_min.isoformat('T') + 'Z',
        timeMax=time_max.isoformat('T') + 'Z',
        )

    return get_all_items(service.events(), params, decorator.http())


def _generate_stats(time_min, time_max, events):
    """
    Generate stats from a list of events.

    @param events: list(events), events to analyze
    @param time_min: datetime, from time
    @param time_max: datetime, to time
    @return: dict(), stats object
    """

    num_events = 0
    event_days = defaultdict(lambda: 0)
    attendees = 0
    total_duration_in_secs = 0
    event_series = defaultdict(lambda: 0)
    for event in events:
        try:
            _ac = event['_ac'] = {}
            if 'dateTime' not in event['start']:
                # All-day events
                continue

            # TODO: Sort out declined and tentative events, if not
            # event.organizer.self, find self in event.attendees
            # list(dict)), 'email' = self and 'responseStatus' =
            # 'accepted'
            start = str_to_datetime(event['start']['dateTime'])
            end = str_to_datetime(event['end']['dateTime'])

            _ac['duration'] = end - start

            if event.get('summary', '') == 'Lunch':
                # Don't count lunches as events
                continue
            if end.hour < WORK_DAY_START or start.hour > WORK_DAY_END:
                # TODO: will miss multi-day events
                continue
            if start.weekday() > 4 or end.weekday() > 4:
                # TODO: will exclude events ending or starting in
                # weekends, but stretching into the week
                continue

            _ac['included'] = True
            total_duration_in_secs += _ac['duration'].total_seconds()
            event_series[start.date()] += 1
            event_days[start.weekday()] += 1
            num_events += 1
            # if list not present, Default to 1 attendant (self)
            attendees += len(event.get('attendees', ['1']))
        except Exception:
            logging.exception('Could not process: {0}'.format(event))
            raise

    # Calculate stats
    stats = {}
    stats['events'] = num_events
    stats['event_days'] = OrderedDict((v, event_days[k]) for (k, v) in WEEKDAY_TO_STR.iteritems())
    stats['event_series'] = OrderedDict((timegm(k.timetuple()) * 1000, v) for (k, v) in sorted(event_series.iteritems()))
    stats['event_hours'] = total_duration_in_secs / 60 / 60
    stats['working_days'] = num_working_days(time_min, time_max)
    stats['working_hours'] = (WORK_DAY_END - WORK_DAY_START) * stats['working_days']
    stats['percent_events'] = (stats['event_hours'] / stats['working_hours']) * 100
    stats['avg_attendees'] = attendees / stats['events']
    stats['avg_events_day'] = stats['events'] / stats['working_days']
    stats['events_excluded'] = len(events) - stats['events']

    return stats


class AnalyzeHandler(webapp.RequestHandler):
    """
    Analyzes a calendar and shows the result to the user.
    """

    @decorator.oauth_required
    def get(self):
        logging.info('Analyzing for: %s', users.get_current_user().nickname())

        try:
            weeks = int(self.request.get('weeks'))
        except ValueError:
            weeks = DEFAULT_WEEKS

        time_min = datetime.utcnow() - timedelta(weeks=weeks)
        time_max = datetime.utcnow()

        cal_id = self.request.get('cal', default_value=DEFAULT_CAL_ID)
        # TODO: The get_events and get_cal_name calls should be concurrent
        try:
            events = _get_events(cal_id, time_min, time_max)
        except AccessTokenRefreshError:
            return self.redirect('/')
        cal_name = get_cal_name(cal_id, service, decorator.http())

        stats = _generate_stats(time_min, time_max, events)

        params = {
            'cal_id': cal_id,
            'time_min': time_min,
            'time_max': time_max,
            'weeks': weeks,
            'work_day_start': WORK_DAY_START,
            'work_day_end': WORK_DAY_END,
            }
        data = {
            'events': events,
            'params': params,
            'stats': stats,
            'stats_json': json.dumps(stats),
            'cal_name': cal_name,
            'pformat': pformat,
            'title': cal_name,
            'page': 'analyze',
            'js': 'analyze',
            'css': 'analyze',
            }
        template = template_engine.get_template('analyze.html')
        self.response.out.write(template.render(data))

#!/usr/bin/python

import sys
from GCalendar import *


def draw_with_calendar_list(screen, calendar_list):
    y = 0
    for calendar_data in calendar_list:
        screen.addstr(y, 0, calendar_data.summary)
        y += 1
        for event in calendar_data.events:
            screen.addstr(y, 1, event.summary)
    screen.refresh()


# @brief  run with --noauth_local_webserver on a remote machine!
if __name__ == '__main__':
    calendar = GCalendar('client_secrets.json', sys.argv)
    calendar_list = calendar.get_calendar_list()

    for calendar_data in calendar_list:
        print calendar_data.id, ',', calendar_data.summary
        for event in calendar_data.events:
            print '\tsummary:', event.summary, '; start:', event.start

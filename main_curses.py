#!/usr/bin/python

import sys
import curses
import locale
import time
import httplib

from GCalendar import *


sleepTime = 15.0
locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()
stdscr = curses.initscr()


def start_curses():
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)


def end_curses():
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()


def draw_with_calendar_list(screen, calendar_list):
    y = 0
    screen.addstr(y, 0, 'Your next 24 hours! (fetched ' + str(datetime.now()) + ')', curses.A_REVERSE)
    y += 1
    for calendar_data in calendar_list:
        y += 1
        screen.addstr(y, 0, calendar_data.summary, curses.A_BOLD)
        y += 1
        for event in calendar_data.events:
            screen.addstr(y, 0, ' ') # because we can overflow
            screen.addstr(y, 1, event.start.strftime('%a - %X'))
            screen.addstr(y, 19, event.summary.encode(code))
            y += 1
    return y


def render_screen():
    calendar_list = calendar.get_calendar_list()
    draw_with_calendar_list(stdscr, calendar_list)
    stdscr.refresh()


if __name__ == '__main__':
    # we're going to want to delay starting curses until after we auth!
    # move to after teh ctor for GCalendar
    start_curses()
    calendar = GCalendar('client_secrets.json', sys.argv)
    stdscr.nodelay(1)

    while 1:
        try:
            render_screen()
            time.sleep(sleepTime * 60)
        except httplib.BadStatusLine:
            continue

    end_curses()

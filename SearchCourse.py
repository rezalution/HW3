import time
from datetime import datetime
from datetime import timedelta
from datetime import time as datetimetime
from TimeClass import TimeClass
import sys
import sqlite3
import operator
import tzlocal
import pytz 


def searchCourse(userID, startTime = None, startDate = None, endTime = None, endDate = None):
  #search to see if there are any courses connected to the userid
    db = sqlite3.connect('catalogue.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = db.cursor()
    cursor.execute(''' SELECT count(course.rowid) FROM course, person WHERE course.person_id = person.rowid AND onid = ?''', (userID,))
    #get all of the items
    countCourses = cursor.fetchone()
    #get the course count to integer to count correctly
    try:
        intCountCourses = int(countCourses[0])
    except:
        intCountCourses = countCourses

    #the corse time zone is pacific coast time since this is for OSU and it is west coast
    courseTimeZone = pytz.timezone("America/Los_Angeles")
	
    #need to get the local timezone
    #this requires tzlocal to get the name, then we can get that into the pytz timezone for the timeZone
    zoneName = tzlocal.get_localzone()
    #then get the timezone from the local time using pytz
    #get the localized time, don't really care just want the time zone
    tz = zoneName.localize(datetime.now())
    #now get the time zone 
    tz = tz.strftime('%z')
		
    #initialize out list of timeclass for our courses
    courseTimeClassList = []

    #if there are less than  1 return the blank list
    if intCountCourses < 1:
        return courseTimeClassList
    #else return a list with each course event
    else:
        now = datetime.now()
        #if there is no start date set the first date to now
        if startDate == None:
            firstDate = now
        else:
            #try to get start date and time to a datetime
            #first try if they have date and time
            try:	

                firstDate = datetime.strptime(startDate + startTime, "%Y-%m-%d%H:%M")
            except:
                #if that doesnt work get the date and it will make the time midnight
                firstDate = datetime.strptime(startDate, "%Y-%m-%d")
      
        #if there is no end date set the last date to bext week
        if endDate == None:
            nextWeek = now + timedelta(days=7)
            lastDate = nextWeek
        else:
            #try to get end date and time to a datetime
            #first try if they have date and time
            try:
                lastDate = datetime.strptime(endDate + endTime, "%Y-%m-%d%H:%M")
            except:
                #if that doesnt work get the date and it will make the time midnight
                lastDate = datetime.strptime(endDate, "%Y-%m-%d")
                lastDate = lastDate + timedelta(hours=23, minutes=59, seconds=59)

        #put our search into a time class, just to make it easier 
        searchTimeClass = TimeClass(firstDate, lastDate)
       
        #get a list of the courses this person has
        cursor.execute('''SELECT mt.start_time, mt.end_time, cmt.start_date, cmt.end_date, mt.week_day FROM person, course, courseMeetingTimes AS cmt, meetingTimes AS mt where course.person_id = person.rowid AND cmt.course_id = course.rowid AND cmt.meeting_times_id = mt.rowid AND person.onid = ?''', (userID,))
        listCourses = cursor.fetchall()

        #get the course datetimes, need to combine the dates and times together
        for i in range(len(listCourses)):
            thisCourseStartTime = listCourses[i][0].time()
            thisCourseStartDateTime = datetime.combine(listCourses[i][2],thisCourseStartTime)
            thisCourseEndTime = listCourses[i][1].time()
            thisCourseEndDateTime = datetime.combine(listCourses[i][3],thisCourseEndTime)
	    #do the time zone change just in case someone isn't on the west coast (like the courses will be always)
            thisCourseStartDateTime = courseTimeZone.localize(thisCourseStartDateTime)
            thisCourseEndDateTime = courseTimeZone.localize(thisCourseEndDateTime)
	    #now shift the datetimes from pacific they were at to the local one
            thisCourseStartDateTime = zoneName.normalize(thisCourseStartDateTime.astimezone(zoneName))
            thisCourseEndDateTime = zoneName.normalize(thisCourseEndDateTime.astimezone(zoneName))
	    #remove the tzinfo cause we cant sort if we leave it
            thisCourseStartDateTime = thisCourseStartDateTime.replace(tzinfo=None)
            thisCourseEndDateTime = thisCourseEndDateTime.replace(tzinfo=None)
				
            #set the course day to an actual day
            if listCourses[i][4] == 'M':
                thisMeetDay = 0
            elif listCourses[i][4] == 'T':
                thisMeetDay = 1
            elif listCourses[i][4] == 'W':
                thisMeetDay = 2
            elif listCourses[i][4] == 'R':
                thisMeetDay = 3
            elif listCourses[i][4] == 'F':
                thisMeetDay = 4
            elif listCourses[i][4] == 'S':
                thisMeetDay = 5
            elif listCourses[i][4] == 'U':
                thisMeetDay = 6

            #check if those times even matter (could be too early orlate)
            if thisCourseStartDateTime > searchTimeClass.end:
                #this means the class starts too late do nothing
                continue
            elif thisCourseEndDateTime < searchTimeClass.start:
                #this means the class ends too early to matter
                continue
            else:
                #this is where the class will be that matters
                #get the latest start time class or search start
                if thisCourseStartDateTime < searchTimeClass.start:
                     relevantStart = searchTimeClass.start
                else:
                    relevantStart = thisCourseStartDateTime
                #get the latest end time like start
                if thisCourseEndDateTime < searchTimeClass.end:
                     relevantEnd = searchTimeClass.end
                else:
                    relevantEnd = thisCourseEndDateTime

                #find the first actual event of the class if its negative then add 7
                nextMeetDay = thisMeetDay - relevantStart.weekday()
                
                if nextMeetDay < 0:
                    nextMeetDay = nextMeetDay + 7
                #set the actual event of the class to a datetime
                eventStart = relevantStart + timedelta(days=nextMeetDay)
                
                #set the actual event to the time of the course
                eventStart = datetime.combine(eventStart, thisCourseStartDateTime.time())
                #set the endinf of the event to a datetime
                eventEnd = datetime.combine(eventStart, thisCourseEndDateTime.time())
				
                #if our course time made it so the timing was too early for our query add 7 days
                if eventEnd < searchTimeClass.start:
                    eventStart = eventStart + timedelta(days=7)
                    eventEnd = eventEnd + timedelta(days=7) 
                #until we hit the end of the search keep adding courses
                while eventStart < searchTimeClass.end:
                     #put course into a timeClassObject
                    thisTimeClass = TimeClass(eventStart, eventEnd)
                    #add it to the list
                    courseTimeClassList.append(thisTimeClass)
                    #increment to the next class time 7 days away 
                    eventStart = eventStart + timedelta(days=7)
                    eventEnd = eventEnd + timedelta(days=7)

        #this is how we will sort, probably do it once we go back to the search item 
		courseTimeClassList.sort(key=operator.attrgetter('start'))
        
		
        #then return the courseTimeListClass for the search algorithm to handle 
    return courseTimeClassList


if __name__ == '__main__':
    userID = sys.argv[1]

    try:
        startTime = sys.argv[2]
    except:
        startTime = None
    try:
        startDate = sys.argv[3]
    except:
        startDate = None
    try:
        endTime = sys.argv[4]
    except:
        endTime = None
    try:
        endDate = sys.argv[5]
    except:
        endDate = None

    searchCourse(userID, startTime, startDate, endTime, endDate)

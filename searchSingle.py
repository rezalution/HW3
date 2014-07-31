import time 
from datetime import datetime
from datetime import timedelta
from datetime import time as datetimetime
from TimeClass import TimeClass
import sys
from SearchGoogle import *
from SearchCourse import *
import operator 
import tzlocal
import pytz 
import json
import collections

flag = None

def searchSingle(userID, startTime = None, startDate = None, endTime = None, endDate = None):
	now = datetime.now()
	#used later to #print out if there is a onid error
	noIDList = []
	
	#if the start date is blank it is now, even if there is a start time, too bad put a date
	if startDate == None:
		startDate = (now.strftime("%Y-%m-%d"))
		startTime = (now.strftime("%H:%M"))
	
	#if the start time is blank put the time as now
	if startTime == None:
		startTime = (now.strftime("%H:%M")) 
		
	#if the end date is blank it is now + 7 days, even if there is an end time
	if endDate == None:
		nextWeek = now + timedelta(days=7)
		endDate = (nextWeek.strftime("%Y-%m-%d")) 
		endTime = (nextWeek.strftime("%H:%M"))
	
	#if the end time is blank put the time as now
	if endTime == None:
		endTime = (now.strftime("%H:%M"))

	listBusyTimes = []
	
	
	#search google calendar here and return the list 
	#have order by in the google search so shouldnt need to order this list for single searches!
	events = googleSearch(userID, startTime, startDate, endTime, endDate)

	#need to get the calendars timezone so we can localize the date returned
	try:
		calendarTimeZone = pytz.timezone(events['timeZone'])
	except:
	#going to force it to pacific coast time if it doesn't have it since this is for OSU and it is west coast
		calendarTimeZone = pytz.timezone("America/Los_Angeles")
	
	#need to get the local timezone
	#this requires tzlocal to get the name, then we can get that into the pytz timezone for the timeZone
	zoneName = tzlocal.get_localzone()
	#then get the timezone from the local time using pytz
	#get the localized time, don't really care just want the time zone
	tz = zoneName.localize(datetime.now())
	#now get the time zone 
	tz = tz.strftime('%z')


	
	#if the id doesn't exist it will return NoID
	if events == "NoID":
		noIDList.append(userID)
	else:
		#if we return to a list called events from the google search
		for event in events['items']:
			#get our times to go into a free time class
			try:
				#if the item is not an all day even it will have datetime 
				thisStart = event['start']['dateTime']
				thisEnd = event['end']['dateTime']
				#convert from unicode to datetime
				thisStart = datetime.strptime(thisStart[:19], '%Y-%m-%dT%H:%M:%S')
				thisEnd = datetime.strptime(thisEnd[:19], '%Y-%m-%dT%H:%M:%S')
				
			except:
				#i the item is an all day event it will justhave date so take up the whole date
				thisStart = event['start']['date']
				#get the unicode to a datetime for combine
				thisStart = datetime.strptime(thisStart, "%Y-%m-%d")
				thisEnd = event['end']['date']
				thisEnd = datetime.strptime(thisEnd, "%Y-%m-%d")
				#change the datetimes to have the relevant timezone
				thisStart = calendarTimeZone.localize(thisStart)
				thisEnd = calendarTimeZone.localize(thisEnd)
				#now shift the datetimes from whatever timezone they were at to the local one (if needed)
				thisStart = zoneName.normalize(thisStart.astimezone(zoneName))
				thisEnd = zoneName.normalize(thisEnd.astimezone(zoneName))
				
				thisStart = thisStart.replace(tzinfo=None)
				thisEnd = thisEnd.replace(tzinfo=None)
				
			#make a busy time from the even that just happened
			thisBusyTime = TimeClass(thisStart, thisEnd)

			#add the busy time to the list
			listBusyTimes.append(thisBusyTime)
		
	#return a list of course times
	listCourseTimes = searchCourse(userID, startTime, startDate, endTime, endDate)
	#add the coursetimes to the busy times
	listBusyTimes.extend(listCourseTimes)
	#sort the busy times list
	listBusyTimes.sort(key=operator.attrgetter('start'))
	#start our free time list
	freeTimeList = []
	
	#print len(listBusyTimes)
	#convert our arguments to actual dates
	startDateTime = datetime.strptime(startDate + startTime, "%Y-%m-%d%H:%M")
	endDateTime = datetime.strptime(endDate + endTime, "%Y-%m-%d%H:%M")
	#if there are no busy times then they are free the entire time
	if len(listBusyTimes) == 0:
		noBusyTime = TimeClass(startDateTime, endDateTime)
		freeTimeList.append(noBusyTime)

	else:			
		#keeping track if we hit the end of the line
		outOfTimeFlag = False
		#is used in for loop counters
		nextItem = 0

		#set the time as the beginning of our comparisons	
		if startDateTime < listBusyTimes[0].start:
			#if the start time is free set this as this free time
			thisFreeTime = TimeClass(startDateTime)
		else:
			#if the start time is busy set the first item as the busy time
			thisBusyTime = listBusyTimes[0]
			#loop through the rest of the items
			for busyCalendarNum in range(len(listBusyTimes)):
				nextItem = busyCalendarNum + 1
				#if the item ending time is after our current busy time
				if thisBusyTime.end < listBusyTimes[busyCalendarNum].end:
					thisBusyTime = listBusyTimes[busyCalendarNum]
					continue #to keep going and not fail
				#if the busy time ends after our ending time
				if thisBusyTime.end > endDateTime:
					#say we have no open times
					outOfTimeFlag = True
					break
				
				#if we get here we found the ending of our time
				thisFreeTime = TimeClass(thisBusyTime.end)
				break
				
		#now this loop for all items after the ones affecting the beginning
		for busyCalendarCount in range(len(listBusyTimes[nextItem:])):
			if outOfTimeFlag == True:
				break
			#check to see if the end of our busy time is after the next time
			if thisFreeTime.start > listBusyTimes[busyCalendarCount].start:
				#if it is after then go to the next one
				continue
			#mark the end of our free time 
			thisFreeTime.end = listBusyTimes[busyCalendarCount].start
			#add the free time to our list of free times
			freeTimeList.append(thisFreeTime)
			#create a new busy time object to compare
			thisBusyTime = listBusyTimes[busyCalendarCount]
			#loop through the rest of the items starting at the next one
			for busyCalendarCount2 in range(len(listBusyTimes[busyCalendarCount:])):
				#if the items ending time is after our current busy time
				if thisBusyTime.end < listBusyTimes[busyCalendarCount2].end:
					thisBusyTime = listBusyTimes[busyCalendarCount2]
					continue #to keep going and not fail
				#if the busy time ends after our ending time
				if thisBusyTime.end > endDateTime:
					#say we have no open times
					#somehow need to break out of ALL loops 
					outOfTimeFlag = True
					break
					
				#if we get here we found the ending of our time
				thisFreeTime = TimeClass(thisBusyTime.end)
				break #hopefully stay within the bog one
		
		#if we get to the end and have not hit the end of the line
		if outOfTimeFlag == False:
			thisFreeTime.end = endDateTime
			freeTimeList.append(thisFreeTime)
	'''		
		#print "Start Time Date End Time Date Day of the Week"
		for freeTimeItem in range(len(freeTimeList)):
			#print freeTimeItem
			#print freeTimeList[freeTimeItem].start.time() 
			#print freeTimeList[freeTimeItem].start.date()
			#print freeTimeList[freeTimeItem].end.time()
			#print freeTimeList[freeTimeItem].end.date()
	
	##print out the user ids that werent found in the onid
	for i in range(len(noIDList)):
		#print noIDList[i]
	'''
	if not flag:
# 		print "no flag"
		return freeTimeList, noIDList
	
	else:
# 		print "we have a flag"
		result = []
		for freeTimeItem in range(len(freeTimeList)):
			##print freeTimeItem
			d = collections.OrderedDict()
			d['onid'] = userID
			d['startAvailability'] = str(freeTimeList[freeTimeItem].start.time()) +" "+ str(freeTimeList[freeTimeItem].start.date())
			d['endAvailability'] = str(freeTimeList[freeTimeItem].end.time()) + " " + str(freeTimeList[freeTimeItem].end.date())

			result.append(d)
        print json.dumps(result)


def main():
	global flag
	
	userID = sys.argv[1]

	try:
		startTime = sys.argv[2]
	except:
		startTime = None
		#print "excet"

	try:
		startDate = sys.argv[3]
	except:
		startDate = None
		#print "excet"

	try:
		endTime = sys.argv[4]
	except:
		endTime = None
		#print "excet"

	try:
		endDate = sys.argv[5]
	except:
		endDate = None
		#print "excet"
		
	try:
		flag = sys.argv[6]
		
	except:
		flag = None
# 		print "excet"

	searchSingle(userID, startTime, startDate, endTime, endDate)
			
if __name__ == '__main__':
	main()

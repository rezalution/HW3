from bs4 import BeautifulSoup
import urllib2
import sqlite3
from fill_tables import *
import sys
import string
from datetime import date, datetime
import time
from teacherNamesScraper import refillPeopleDatabase
		
def deleteRelevantTables(db):
	#deletes the items we are going to fill
	try:
		cursor = db.cursor()
		#delete dept cause we will add this when we go (just in case new ones are added)
		cursor.execute('''DELETE FROM dept ''')
		#delete this cause this is what we are adding
		cursor.execute('''DELETE FROM course ''')
		#deleting this cause we ae adding these as well
		cursor.execute('''DELETE FROM courseMeetingTimes ''')
		#not deleting meetingTimes because those are going to be used quite a bit I think (though we could the logic is there to add them if we want 
	except:
		raise

	return
	
def insertReturnDepartment(db, departmentName):
	try:
		cursor = db.cursor()
		#see if the department exists yet
		cursor.execute('''SELECT rowid FROM dept WHERE name = ?''', (departmentName,))
		#get the department id
		deptID = cursor.fetchone()
		
		if deptID is None:
		#if it doesnt we will insert and save the dept
			deptID = deptFillRetID(db, departmentName)

	except:
		raise
		
	return deptID

def insertReturnCourse(db, courseName, deptID, section, instructor):
	try:
		cursor = db.cursor()
		#split the name to search
		indexComma = instructor.index(',')
		indexPeriod = instructor.index('.')

		#get the last name and the first letter since that is all courses have
		firstInit = instructor[indexComma + 1: indexPeriod].strip()
		lastName = instructor[:indexComma].strip()
		
		#get the person name
		cursor.execute('''SELECT rowid FROM person WHERE lastName = ? and firstName like ?''', (lastName, firstInit + '%',))
		personID = cursor.fetchone()

		#try to insert the course and return the id
		courseID = courseFillRetID(db, courseName, section, personID)
	except:
		raise
	
		
	return courseID

def insertReturnMeetTime(db, startTime, endTime, day):
	try:
		cursor = db.cursor()

		#convert the string of the times in form #### to a datetime
		#the date time will have a date of 1,1,1 cause it really doesnt matter, it just needs to exist 
		#we only care about the time, like how we only care about date in dates instance
		startTimeDateTime = datetime(year=1,month=1,day=1, hour=int(startTime[0:2]), minute=int(startTime[2:4]))
		endTimeDateTime = datetime(year=1,month=1,day=1, hour=int(endTime[0:2]), minute=int(endTime[2:4]))
		
		#see if the meeting time exists yet
		cursor.execute('''SELECT rowid FROM meetingTimes WHERE start_time = ? AND end_time = ? AND week_day = ?''', (startTimeDateTime, endTimeDateTime, day,))
		meetingTimeID = cursor.fetchone()
		
		if meetingTimeID is None:
			#if it doesnt we will insert and save the meeting time
			meetingTimeID = meetingTimesRetID(db, startTimeDateTime, endTimeDateTime, day)
	except:
		raise
		
	return meetingTimeID
	
	
def insertIntoDatabaseMultiple(db, department, courseName, instructor, section, startTime, endTime, startDate, endDate, day):
	try:
		cursor = db.cursor()

		#insert the department if it is new else get the id
		deptID = insertReturnDepartment(db, department)
		#insert the course	
		courseID = insertReturnCourse(db, courseName, deptID, section, instructor)
		#insert the meeting time if it doesnt exist else get the id
		meetingTimeID = insertReturnMeetTime(db, startTime, endTime, day)
		#convert the dates to actual dates for comparison
		startDateTime = startDate.date()
		endDateTime = endDate.date()
		
		#insert the course meeting time using the course and meeting time id
		courseMeetingTimesInsert(db, courseID, meetingTimeID, startDateTime, endDateTime)
	
	except:
		raise

	return

def refreshCourse():
	#call the people refresh first
	refillPeopleDatabase()
	#test is a file for test purposes
	test = open('file','w')
	try:
		#connect to database
		db = sqlite3.connect('catalogue.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		cursor = db.cursor()
		#delete the items from the tables we are going to fill
		deleteRelevantTables(db)
	except:
		raise
	
	#this is the url for the course catalog searching for EVERY class
	url = "http://catalog.oregonstate.edu/SOCSearcher.aspx?wks=&chr=abcder/"
	#do the html response and read
	response = urllib2.urlopen(url)
	
	page = response.read()
	#open the soup from the page
	soup = BeautifulSoup(page) 
	#go to the table we actually want of the courses
	tableTag = soup.find('table', id='ctl00_ContentPlaceHolder1_gvResults')

	##############################
	#use this part to single out a course for testings mostly
	'''
	td = tableTag.find('td')

	aTag = td.a
	aTag = tableTag.find('a', id='ctl00_ContentPlaceHolder1_gvResults_ctl4767_HyperLink1')
        print "the value is %s " % td.string
	print "the fref at this td is %s" % aTag['href']
	

	getCourseInfo("http://catalog.oregonstate.edu" + aTag['href'], test, db)

	print "asdfa"
	exit()
	'''
	###########################################

	#for each table row(which is each class)
	for trTag in tableTag.find_all('tr'):
		#should only be one td per tr and we'll go into it
		td = trTag.find('td')
		
		#finding the a tag in the td 
		aTag = td.a
		#get the href and go there, to get the info
		test.write("%s\n" % aTag['href'])
		#use the url string extension to the catalog url 
		urlString = "http://catalog.oregonstate.edu" + aTag['href']
		
		#go to the function to get the info
		getCourseInfo(urlString, test, db)
			
	return

def getCourseInfo(url, test, db):
	#open the page and read the info
	response = urllib2.urlopen(url)
	page = response.read()
	
	#do the soup business
	soup = BeautifulSoup(page)

	#get the dept here 
	#it is the a tag in the form tag that is aspnetForm
	formWithDepartment = soup.find('form', id='aspnetForm')
	department = formWithDepartment.find('a')

	#gets the course name
	course = soup.find('h3')
	course = course.text
	#only get the course til the period
	periodIndex = course.index('.')
	course = course[:periodIndex]
	course = course.strip()
	
	#get the table we want for the courses, seems to be the same id always
	tableTag = soup.find('table', id='ctl00_ContentPlaceHolder1_SOCListUC1_gvOfferings')

	#for all of the table rows except the first cause its the header
	for trTags in tableTag.find_all('tr'):
		if trTags.find('th'):
			continue
			#this allows us to skip the th tag which we dont want at all
		else:
			tdTags = trTags.find_all('td')
			#gets this courses day/time/date field 
			dayTimeDate = tdTags[6].text.split()
			#gets the instructor name
			instructor = tdTags[5].text
			
			#gets the course section
			section = tdTags[2].text
						
			#if there is a TBA then skip it as it wont be helpful
			#same with if the instructor is "Staff"
			if(dayTimeDate[0] == "TBA" or instructor == "Staff" or instructor == "" or instructor == None) or instructor == u'\xa0':
				continue
			else:
				#this loops through for each item in dayTimeDate list 
				#mostly used when they will have multiple strange meeting times for one class
				#else it will just go through once as normal
				
				for meetingCount in range(len(dayTimeDate) - 1):
					#when the meeting time is 0 the day is the first list item (all by itself)
					if meetingCount == 0:
						days = dayTimeDate[0]
					#else the day is the last of the one before(we'll store this at the end)	
					else:	
						days = nextDays

					#splits the time which is in the next item in the list
					timeList = dayTimeDate[meetingCount + 1].split('-')
					#for each char in the days they meet (because we will need to search through each day)
					for day in days:
						startTime = timeList[0]
						#get the end time (the first 4 chars)
						endTime = timeList[1][:4]
						
						#gets the start date after the end time
						date = timeList[1][4:]
						
						#the "normal" days would be here like MWF only courses at the same time
						try:
							#sometimes gets the end date(this is where the try will fail if it does)
							dateEnd = timeList[2]

							dateSplit = date.split('/')
							monthStart = dateSplit[0]
							dayStart = dateSplit[1]
							#only want the first 2 characters of the year
							yearStart = dateSplit[2][:2]
							
							
							test.write("START M %s d %s y %s Day %s time %s\n" % (monthStart, dayStart, yearStart, day, startTime))
							
							dateSplit = dateEnd.split('/')
							monthEnd = dateSplit[0]
							dayEnd = dateSplit[1]
							yearEnd = dateSplit[2][:2]
							test.write("END M %s d %s y %s Day %s time %s\n" % (monthEnd, dayEnd, yearEnd, day, endTime))

							#next day, if there is one
							nextDays = dateSplit[2][2:]

							#put the date in a datetime format
							startDateString = monthStart + '/' + dayStart + '/' + yearStart
							endDateString = monthEnd + "/" + dayEnd + "/" + yearEnd
							startDate = datetime.strptime(startDateString, "%m/%d/%y")
							endDate = datetime.strptime(endDateString, "%m/%d/%y")
							
							#now insert into the database the course information
							insertIntoDatabaseMultiple(db, department.text, course, instructor, section, startTime, endTime, startDate, endDate, day)
						
						#this is for specific day meeting courses like BEE 507 (meet 5 times over the quarter one day each)
						except:
							#this is really only important when they have only one date
							#splits the date up into blocks of '/' so we can get the correct D/M/Y
							dateSplit = date.split('/')
							monthStart = dateSplit[0]
							dayStart = dateSplit[1]
							#only want the first 2 characters for the year
							yearStart = dateSplit[2][:2]
								
							#next day, if there is one
							nextDays = dateSplit[2][2:]
							
							
							test.write("SINGLE M %s d %s y %s Day %s\n" % (monthStart, dayStart, yearStart, day))
							
							#put the date in a datetime format
							startDateString = monthStart + '/' + dayStart + '/' + yearStart
							endDateString = monthStart + "/" + dayStart + "/" + yearStart
							startDate = datetime.strptime(startDateString, "%m/%d/%y")
							endDate = datetime.strptime(endDateString, "%m/%d/%y")
							
							try:
							#now insert into the database the course information
								insertIntoDatabaseMultiple(db, department.text, course, instructor, section, startTime, endTime, startDate, endDate, day)
							except:
								continue
							

							
	return
	
if __name__ == '__main__':
	refreshCourse()

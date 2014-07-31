import time 
from datetime import datetime
from datetime import timedelta
from datetime import time as datetimetime
from TimeClass import TimeClass
from SearchCourse import *
from SearchGoogle import *
from searchAvailableTimes import searchAvailTimes
import operator 
import json
import collections
import pytz
import tzlocal
flag = None

def searchAvailUsers(userIDList, startTime = None, startDate = None, endTime = None, endDate = None, dayStartTime = None, dayEndTime = None):
	#split the userid list string (this is because the web site needs to pass it as a string, cant pass a list)
	#print startDate
	userIDList = userIDList.split(',')
	#strp all of the white space
	for i in range(len(userIDList)):
		userIDList[i] = userIDList[i].strip()
	
	now = datetime.now()
	#used later to #print out if there is a onid error
	noIDList = []
	
	#if the start date is blank it is now, even if there is a start time, too bad put a date
	if startDate == None:
		startDate = (now.strftime("%Y-%m-%d"))
		startTime = (now.strftime("%H:%M"))
		
	#if the end date is blank it is now + 7 days, even if there is an end time
	if endDate == None:
		nextWeek = now + timedelta(days=7)
		endDate = (nextWeek.strftime("%Y-%m-%d")) 
		endTime = (nextWeek.strftime("%H:%M"))
		
	#convert our arguments to actual dates
	startDateTime = datetime.strptime(startDate + startTime, "%Y-%m-%d%H:%M")
	endDateTime = datetime.strptime(endDate + endTime, "%Y-%m-%d%H:%M")
	#get the amount of days
	daysBetween = endDateTime - startDateTime
	
	#start our list of busy times
	listBusyTimes = []
	
	#setup the remove list
	userIDRemoveList = []
	
	#Going to have to do this for EVERY user id with the multi search
	for user in userIDList:
        #initialize the freetimelist for each user
		freeTimeList = []
		#do the search list
		freeTimeList, noIDList = searchAvailTimes(user, startTime, startDate, endTime, endDate, dayStartTime, dayEndTime)
				
		#if the start or end constraint dont exist do it like we did before
		if dayStartTime == None or dayEndTime == None:
			#if the free time list is not blank or full of just one time
			if len(freeTimeList) > 1:
				#remove the user
				userIDRemoveList.append(user)
		#else if there are constraints 
		else:
			#see if there are any days that we are leaving out, if we are they are busy the entire constraint
			if daysBetween.days > len(freeTimeList):
				userIDRemoveList.append(user)
			else:
			        #for all of the free times
				for time in freeTimeList:
				        #get our constraints to datetime values 
					dayStartDateTime = datetime.strptime(dayStartTime, '%H:%M')
					dayEndDateTime = datetime.strptime(dayEndTime, '%H:%M')
				
	
				        #if the start time is after our constraint start time 
					if time.start.time() > dayStartDateTime.time():
					        #first check if it is only later cause the search time was later
						if time.start.date() == startDateTime.date() and startDateTime.time() > dayStartDateTime.time():
							pass
						else:
						        #if it was later for any other reason then it means something is happening
							userIDRemoveList.append(user)
							break
						
				        #if the end time is before our constraint end time
					if time.end.time() < dayEndDateTime.time():
					        #first check if it is only before because the search was before
						if time.end.date() == endDateTime.date() and endDateTime.time() < dayEndDateTime.time():
							pass
						else:
						       #if it was earlier for any other treason then they are busy
							userIDRemoveList.append(user)
							break
	
		#clear the lists if they exist else delete them totally
		#this way we dont get false negatives for the next person
		try:
			del freeTimeList[:]
		except:
			del freeTimeList	
	

	for userNum in userIDRemoveList:
		#print "remove"
		#print userNum
		userIDList.remove(userNum)

 	#for userLeft in range(len(userIDList)):
 		#do a database search to get the users name? 
 		#userName = userIDList[userLeft]#nameSearch(userId)
 		#print "found"
 		#print userIDList[userLeft]
 		
 	##print out the user ids that werent found in the onid
 	#for i in range(len(noIDList)):
 		#print "not found"
 	#	print noIDList[i]
 		
 	#if no users
 	#if userIDList == 0:
 		#print "No users available during your time constraints"
 		#probably should add this to the userIDList instead that way it #prints out the error

	
	##print the header
	#print "UserID	Name"
	if not flag:
# 		print "no flag"
#		print userIDList
		return userIDList, noIDList
	
	else:
# 		print "we have a flag"
		result = []
		for user in noIDList:
			userIDList.remove(user)
		
		for freeTimeItem in range(len(userIDList)):
			##print freeTimeItem
			d = collections.OrderedDict()
			d['onid'] = userIDList[freeTimeItem]
			d['notFound'] = None
			result.append(d)
		
		##print out the user ids that werent found in the onid
		for i in range(len(noIDList)):
			#if we already have an index, edit. if not, append
			if i < len(result):
				d = result[i]
				d['notFound'] = noIDList[i]
				result[i]=d
			else:
				d = collections.OrderedDict()
				d['onid'] = None
				d['notFound'] = noIDList[i]
				result.append(d)
		
		
        print json.dumps(result)
        
        

	return userIDList, noIDList
		
def main():
	global flag
	userID = sys.argv[1]

	#print "userID"
	userIDList = userID 
	#print userIDList
	
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
	
	try:
		dayTimeStart = sys.argv[6]
	except:
		dayTimeStart = None
		
	try:
		dayTimeEnd = sys.argv[7]
	except:
		dayTimeEnd = None
		
	try:
		flag = sys.argv[8]
	except:
		flag = None
		
	

	searchAvailUsers(userIDList, startTime, startDate, endTime, endDate, dayTimeStart, dayTimeEnd)
			
if __name__ == '__main__':
	main()

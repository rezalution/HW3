#!/usr/bin/env python
import curses
from curses import wrapper 
from datetime import datetime
from searchSingle import *
from searchAvailableTimes import *
from searchAvailableUsers import *
import time
#make the initial array for the queries
queryArray = [None, None, None, None, None]

#show the results for people who are free the entire time
def placeUserResults(stdscr, freeUserList, noIDList):
	stdscr.clear()
	stdscr.border()
	#setup our large window and box it
	resultsScreen = stdscr.subwin(0,0)
	resultsScreen.box()
	#get the max x and y so we can do the center
	y, x = resultsScreen.getmaxyx() 
	resultsScreen.refresh()

	#get the width has to be a little smaller
	windowWidth = x - 2
	#get the window length if its too short make it the endtire screen
	windowLength = len(freeUserList) + (len(freeUserList) / 25) + 10
	if windowLength < y:
		windowLength = y - 1
	
	#make our result padding 
	resultPad = curses.newpad(windowLength, windowWidth)#windowLength, windowWidth,1,1)
	resultPad.scrollok(True)
	resultPad.idlok(True)

	#see if the values in the queries are blank or not, if so set the data to now or now plys 7 days
	if queryArray[1] == None:
		queryArray[1] = (datetime.now().strftime("%Y-%m-%d"))
		queryArray[2] = (datetime.now().strftime("%H:%M"))
	if queryArray[2] == None:
		queryArray[2] = (datetime.now().strftime("%H:%M"))
	if queryArray[3] == None:
		nextWeek = datetime.now() + timedelta(days=7)
		queryArray[3] = (nextWeek.strftime("%Y-%m-%d"))
		queryArray[4] = (nextWeek.strftime("%H:%M"))
	if queryArray[4] == None:
		queryArray[4] = (datetime.now.strftime("%H:%M"))

 
	#put the headline for the results pad
	resultsScreen.addstr(1,1, "Users available the entire time")
	resultsScreen.addstr(2,1, "From the time: " + queryArray[2] + " " + queryArray[1] + " to " + queryArray[4] + " " + queryArray[3])
					
	#put the heading for commands
	scrollString = "Scroll with up or down arrow"
	backString = "Press b or q to go back"
	resultsScreen.addstr(1, x - len(scrollString) - 2, scrollString)
	resultsScreen.addstr(2, x - len(backString) - 2, backString)
						
	if len(noIDList) > 0:
		#used for going over headings so we dont overlap
		extra = 0
		
		resultPad.addstr(1, 0, "The following ONIDs do not seem to exist")
		resultPad.addstr(2, 0, "This could lead to busy times showing as free, please check for correct ONIDs")
		for i in range(len(noIDList)):
			resultPad.addstr(i + extra +  3, 0, "Missing ONID: " + noIDList[i])
			#if the range has gone 25 lines print out the header again
			if i % 25 == 0 and i != 0:
				#increase the extra so we don't overlap
				extra = extra + 2
				resultPad.addstr(i + extra + 3, 0, "The following ONIDs do not seem to exist")
				resultPad.addstr(i + extra + 4, 0, "This could lead them showing as free, please check for correct ONIDs")
				
		
		#add the header for the times 
		noIDLength = len(noIDList)
		resultPad.addstr(noIDLength + 4, 0, "Users Available the entire time")

		#print the free times
		for i in range(len(freeUserList)):
			#number
			resultPad.addstr(i + noIDLength + extra + 5, 0, str(i + 1))
			#start date
			resultPad.addstr(i + noIDLength + extra  + 5, 5, freeUserList[i])
			#if the range has gone 25 lines print out the header again just cause it wont stay 
			if i % 25 == 0 and i != 0:
				resultPad.addstr(i + noIDLength + extra  + 5, 0, "Users Available the entire time")
				#increase the noIDLength so we don't miss items
				noIDLength = noIDLength + 2

	else:
		#add the header for the times 
		resultsScreen.addstr(3, 1, "Users Available the entire time")
		#have this extra lines for when we print out the extra headers
		extra = 0
		#print the free times
		for i in range(len(freeUserList)):
			#number
			resultPad.addstr(i + extra + 2, 0, str(i + 1))
			#start date
			resultPad.addstr(i + extra  + 2, 5, freeUserList[i])
			#if the range has gone 25 lines print out the header again
			if i % 25 == 0 and i != 0:
				#increase the extra so we don't overlap
				extra = extra + 1
				resultPad.addstr(i + extra + 2, 0, "Users Available the entire time")
				
				
	#refresh the pad toshow it
	resultsScreen.refresh()
	resultPad.refresh(0,0,4,2,y - 4, x - 3)
	#set our position to the end of the window
	pos = 0
	while True:
		char = resultPad.getch()
		if char == curses.KEY_DOWN or char == 66:
			#need to move it down, but need to have a limit on how low we can go
			if pos + y + 2 < windowLength:
				pos = pos + 1 
			resultPad.refresh(pos, 0, 4, 2, y - 2, x - 3) 
		elif char == curses.KEY_UP or char == 65:
			#need to move it up but need to have a limit
			if pos > 0: 
				pos = pos - 1
			resultPad.refresh(pos, 0, 4, 2, y - 2, x - 3) 
		elif char == ord('B') or char == ord('b') or char == ord('Q') or char == ord('q'):
			resultsScreen.clear()
			stdscr.border()
			return
			
	return

#shoul dwork for the multiple and single time searches
def placeTimeResults(stdscr, freeTimeList, noIDList):
	stdscr.clear()
	stdscr.border()
	#setup our large window and box it
	resultsScreen = stdscr.subwin(0,0)
	resultsScreen.box()
	#get the max x and y so we can do the center
	y, x = resultsScreen.getmaxyx() 
	resultsScreen.refresh()

	#get the width has to be a little smaller
	windowWidth = x - 2
	#get the window length if its too short make it the endtire screen
	windowLength = len(freeTimeList) + (len(freeTimeList) / 25) + 10
	
	resultsScreen.refresh()
	if windowLength < y:
		windowLength = y - 1
		
	#make our result padding 
	resultPad = curses.newpad(windowLength, windowWidth)#windowLength, windowWidth,1,1)
	resultPad.scrollok(True)
	resultPad.idlok(True)


	#see if the values in the queries are blank or not, if so set the data to now or now plys 7 days
	if queryArray[1] == None:
		queryArray[1] = (datetime.now().strftime("%Y-%m-%d"))
		queryArray[2] = (datetime.now().strftime("%H:%M"))
	if queryArray[2] == None:
		queryArray[2] = (datetime.now().strftime("%H:%M"))
	if queryArray[3] == None:
		nextWeek = datetime.now() + timedelta(days=7)
		queryArray[3] = (nextWeek.strftime("%Y-%m-%d"))
		queryArray[4] = (nextWeek.strftime("%H:%M"))
	if queryArray[4] == None:
		queryArray[4] = (datetime.now().strftime("%H:%M"))


	#put the headline for the results pad
	resultsScreen.addstr(1,1, "Times the user: " + queryArray[0] + " is available")
	resultsScreen.addstr(2,1, "From the time: " + queryArray[2] + " " + queryArray[1] + " to " + queryArray[4] + " " + queryArray[3])
		

	#put the heading for commands
	scrollString = "Scroll with up or down arrow"
	backString = "Press b or q to go back"
	resultsScreen.addstr(1, x - len(scrollString) - 2, scrollString)
	resultsScreen.addstr(2, x - len(backString) - 2, backString)

						
	if len(noIDList) > 0:
		#used for going over headings so we dont overlap
		extra = 0
		
		resultPad.addstr(1, 0, "The following ONIDs do not seem to exist")
		resultPad.addstr(2, 0, "This could lead to busy times showing as free, please check for correct ONIDs")
		for i in range(len(noIDList)):
			resultPad.addstr(i + extra +  3, 0, "Missing ONID : " + noIDList[i])
			#if the range has gone 25 lines print out the header again
			if i % 25 == 0 and i != 0:
				#increase the extra so we don't overlap
				extra = extra + 2
				resultPad.addstr(i + extra + 3, 0, "The following ONIDs do not seem to exist")
				resultPad.addstr(i + extra + 3, 0, "This could lead to busy times showing as free, please check for correct ONIDs")
				
		
		#add the header for the times 
		noIDLength = len(noIDList)
		resultPad.addstr(noIDLength + 4, 0, "Time  Start Date  Start Time  End Date  End Time")

		#print the free times
		for i in range(len(freeTimeList)):
			#number
			resultPad.addstr(i + noIDLength + 5, 0, str(i + 1))
			#start date
			resultPad.addstr(i + noIDLength + 5, 6, freeTimeList[i].start.strftime("%Y-%m-%d"))
			#start time
			resultPad.addstr(i + noIDLength + 5, 20, freeTimeList[i].start.strftime("%H:%M"))
			#end date
			resultPad.addstr(i + noIDLength + 5, 29, freeTimeList[i].end.strftime("%Y-%m-%d"))
			#end time
			resultPad.addstr(i + noIDLength + 5, 42, freeTimeList[i].end.strftime("%H:%M"))
			#if the range has gone 25 lines print out the header again just cause it wont stay 
			if i % 25 == 0 and i != 0:
				#increase the noIDLength so we don't miss items
				noIDLength = noIDLength + 1
				resultPad.addstr(i + noIDLength + extra  + 5, 0, "Time  Start Date  Start Time  End Date  End Time")
				

	else:
		#add the header for the times 
		resultsScreen.addstr(3, 2, "Time  Start Date  Start Time  End Date   End Time")
		
		#have this extra lines for when we print out the extra headers
		extra = 0
		#print the free times
		for i in range(len(freeTimeList)):
			#number
			resultPad.addstr(i + extra, 0, str(i + 1))
			#start date
			resultPad.addstr(i + extra, 6, freeTimeList[i].start.strftime("%Y-%m-%d"))
			#start time
			resultPad.addstr(i + extra, 20, freeTimeList[i].start.strftime("%H:%M"))
			#end date
			resultPad.addstr(i + extra, 29, freeTimeList[i].end.strftime("%Y-%m-%d"))
			#end time
			resultPad.addstr(i + extra, 42, freeTimeList[i].end.strftime("%H:%M"))
			#if the range has gone 25 lines print out the header again
			if i % 25 == 0 and i != 0:
				#increase the extra so we don't overlap
				extra = extra + 1
				resultPad.addstr(i + extra, 0, "Time  Start Date  Start Time  End Date   End Time")
	
					
	#refresh the pad toshow it
	resultsScreen.refresh()
	resultPad.refresh(0,0,4,2,y - 2, x - 3)
	#resultPad.getch()
	#resultPad.getch()
	#set our position to the end of the window
	pos = 0
	while True:
		char = resultPad.getch()
		if char == curses.KEY_DOWN or char == 66:
			#need to move it down, but need to have a limit on how low we can go
			if pos + y + 2 < windowLength:
				pos = pos + 1 
			resultPad.refresh(pos, 0, 4, 2, y - 2, x - 3) 
		elif char == curses.KEY_UP or char == 65:
			#need to move it up but need to have a limit
			if pos > 0: 
				pos = pos - 1
			resultPad.refresh(pos, 0, 4, 2, y - 2, x - 3) 
		elif char == ord('B') or char == ord('b') or char == ord('Q') or char == ord('q'):
			resultsScreen.clear()
			stdscr.border()
			break
			
	return

def center (window):
	#centers our text
	y, x = window.getmaxyx()
	
	centerY = (y / 2)
	centerX = (x / 2)

	return centerY,  centerX

def placeMenu(window, string, x, y, colorPair):
	#place it partway to the left so it is aligned
	thisX = x - 30 
	window.addstr(y, thisX, string[:1], curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(colorPair))
	window.addstr(y, thisX + 1, string[1:], curses.color_pair(colorPair))

	return
	
def placeUserInput(window, x, y, pos, singleOrMulti):
	#get the users input for this item
	curses.echo()
	#depending on the position change what to show
	if pos == 1 and singleOrMulti == "multi":
		#used for the multi onid searches
		if queryArray[pos - 1] == None:
			window.addstr(y, x, "Use comma to separate users  ", curses.A_UNDERLINE)
		else:
			window.addstr(y, x, queryArray[pos - 1])
		
		queryArray[pos - 1] = window.getstr(y, x)
	elif pos == 2 or pos == 4:
		#dates for dates
		if queryArray[pos - 1] == None:
			window.addstr(y, x, "YYYY-MM-DD", curses.A_UNDERLINE)
		else:
			window.addstr(y, x, queryArray[pos - 1])
			
		queryArray[pos - 1] = window.getstr(y, x, 10)
	elif pos == 3 or pos == 5:
		#used for the times
		if queryArray[pos - 1] == None:
			window.addstr(y, x, "HH:MM", curses.A_UNDERLINE)
		else:
			window.addstr(y, x, queryArray[pos - 1])
			
		queryArray[pos - 1] = window.getstr(y, x, 5)
	else:
		#just for one user search
		if queryArray[pos - 1] == None:
			window.addstr(y, x, "Please just insert one ONID   ", curses.A_UNDERLINE)
		else:
			window.addstr(y, x, queryArray[pos - 1])
			
		queryArray[pos - 1] = window.getstr(y, x)

	#jave it sothe user input doesnt show up
	curses.noecho()

	return 

def placeUserMenu(window, x, y, pos, stdscr):
	#setup the colors for the text
	curses.init_pair(1, curses.COLOR_BLUE , curses.COLOR_WHITE)
	curses.init_pair(2, curses.COLOR_GREEN , curses.COLOR_BLACK)

	blueOnWhite = 1
	greenOnBlack = 2
	
	#shows where we are based on arrows and position 
	if pos == - 1:
		#this is the search part
		placeMenu(window, "Execute Query", x, y - 1, blueOnWhite)
	else:
		placeMenu(window, "Execute Query", x, y - 1, greenOnBlack)
	if pos == 1:
		placeMenu(window, "1 - User ONID:", x, y + 1, blueOnWhite)
	else:
		placeMenu(window, "1 - User ONID:" , x, y + 1, greenOnBlack)
	if pos == 2:
		placeMenu(window, "2 - Beginning Date:", x, y + 2, blueOnWhite)
	else:
		placeMenu(window, "2 - Beginning Date:", x, y + 2, greenOnBlack)
	if pos == 3:
		placeMenu(window, "3 - Beginning Time:", x, y + 3, blueOnWhite)
	else:
		placeMenu(window, "3 - Beginning Time:", x, y + 3, greenOnBlack)
	if pos == 4:
		placeMenu(window, "4 - End Date:", x, y + 4, blueOnWhite)
	else:
		placeMenu(window, "4 - End Date:", x, y + 4, greenOnBlack)
	if pos == 5:
		placeMenu(window, "5 - End Time:", x, y + 5, blueOnWhite)
	else:
		placeMenu(window, "5 - End Time:", x, y + 5, greenOnBlack)
	if pos == 6:
		#special for back to have B go back as well
		string = "6 - Back to Home"
		placeMenu(window, string, x, y + 6, blueOnWhite)
		thisX = x - 30
		window.addstr(y + 6, thisX + 4, string[4:5], curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(blueOnWhite))
	else:
		string = "6 - Back to Home"
		placeMenu(window, string, x, y + 6, greenOnBlack)
		thisX = x - 30
		window.addstr(y + 6, thisX + 4, string[4:5], curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(greenOnBlack))

	return
	
	
def getInput(window, char, pos, stdscr, multiFlag, query):
	window.keypad(1)
	#get the ecenter of the screenfor 
	centerY, centerX = center(window)
	curses.init_pair(3, curses.COLOR_RED , curses.COLOR_BLACK)
	redOnBlack = 3
	
	#get the users input 
	if char == ord('1'):
		pos = 1
	elif char == ord('2'):
		pos = 2
	elif char == ord('3'):
		pos = 3
	elif char == ord('4'):
		pos = 4
	elif char == ord('5'):
		pos = 5
	elif char == ord('6'):
		pos = 6
	elif char == ord('e') or char == ('E'):
		pos = -1
	elif char == curses.KEY_DOWN or char == 66:
		#wrap around positions going down
		window.addstr(0,0, "down")
		if pos == -1:
			pos = 1
		elif pos < 6:
			pos += 1
		else: 
			pos = -1
	elif char == curses.KEY_UP or char == 65:
		#wrap around positions going up
		window.addstr(0,0, "up")
		if pos == -1:
			pos = 6
		elif pos > 1:
			pos -= 1
		else: 
			pos = -1
	elif char == ord('b') or char == ord('B'):
		pos = 'Back'
	#when the user hits enter
	elif char == ord('\n') or char == curses.KEY_ENTER:
		#remove the error just in case another pops up, don't want them overlapping and making no sense
		placeMenu(window, " " * 57, centerX, centerY - 3, redOnBlack)
		#depending on the position do the certain functions
		if pos == -1:
			window.addstr(0,0,"execute")
				
			#re-validate onid as that is the most important one and the others will all be None-ed out if they suck
			#onids
			#trim the onid line
			queryArray[0] = queryArray[0].strip()
			if queryArray[0] == "": 
				placeMenu(window, "Please insert an ONID to search." , centerX, centerY - 3, redOnBlack)
			else:
				#try to get all of the items(just for validation)
				if multiFlag == 'multi':
					try:
						#try to split the userIDList just make sure they did indeed do it correctly even though we wont use it
						userIDList = queryArray[0].split(',')
						
						if query == "time":
							#search on the multiple user onid to get multiple times
							freeTimeList, noIDList = searchAvailTimes(queryArray[0],queryArray[2],queryArray[1],queryArray[4],queryArray[3])

							#go to the results screen
							placeTimeResults(stdscr, freeTimeList, noIDList)
						elif "user":
							#search on the multiple user onid to see who is available
							freeTimeList, noIDList = searchAvailUsers(queryArray[0],queryArray[2],queryArray[1],queryArray[4],queryArray[3])
							
							#go to the results screen
							placeUserResults(stdscr, freeTimeList, noIDList)
							#delete to refresh, want to do it here and not after the else just in case it fails
							try:
								del freeTimeList[:]
							except:
								del freeTimeList
							try:
								del noIDList[:]
							except:
								del noIDList
					except:
						placeMenu(window, "Please insert ONIDs in a comma separated list." , centerX, centerY - 3, redOnBlack)
				else:
					#search the single user onid
					freeTimeList, noIDList = searchSingle(queryArray[0],queryArray[2],queryArray[1],queryArray[4],queryArray[3])
					#go to the results screen
					placeTimeResults(stdscr, freeTimeList, noIDList)
							
				        #should remove the freeTimeList, noIDList for next time to get a new one no matter what
					try:
						del freeTimeList[:]
					except:
						del freeTimeList
					try:
						del noIDList[:]
					except:
						del noIDList
		if pos == 1:
			placeUserInput(window, centerX, centerY + pos, pos, multiFlag)
			window.addstr(0,0, "user")
			#validate that there is an onid item existing
			#trim the onid line
			queryArray[pos - 1] = queryArray[pos - 1].strip()
			if queryArray[pos - 1] == "": 
				placeMenu(window, "Please insert an ONID to search." , centerX, centerY - 3, redOnBlack)
			else:
				#try to get all of the items(just for validation)
				if multiFlag == 'multi':
					#see if they have a user list
					try:
						#seeing if we get a comma seperated list for validation purposes
						userIDList = queryArray[pos - 1].split(',')
					except:
						#if they didn't insert any it will come here
						placeMenu(window, "Please insert ONIDs in a comma separated list." , centerX, centerY - 3, redOnBlack)
						queryArray[pos - 1] = None	
		if pos == 2:
			placeUserInput(window, centerX, centerY + pos, pos, multiFlag)
			window.addstr(0,0, "beg date")
			#validate the beginning date
			try:
				begDate = datetime.strptime(queryArray[pos - 1], '%Y-%m-%d')
			except:
				placeMenu(window, "Incorrect date format, please re-insert it as YYYY-MM-DD." , centerX, centerY - 3, redOnBlack)
				queryArray[pos - 1] = None
		if pos == 3:
			placeUserInput(window, centerX, centerY + pos, pos, multiFlag)
			window.addstr(0,0, "beg time")
			#validate the beginning time
			try:
				begTime = datetime.strptime(queryArray[pos - 1], '%H:%M')
			except:
				placeMenu(window, "Incorrect date format, please insert it as HH:MM." , centerX, centerY - 3, redOnBlack)
				queryArray[pos - 1] = None
		if pos == 4:
			placeUserInput(window, centerX, centerY + pos, pos, multiFlag)
			window.addstr(0,0, "end date")
			#validate the ending date
			try:
				endDate = datetime.strptime(queryArray[pos - 1], '%Y-%m-%d')
			except:
				placeMenu(window, "Incorrect date format, please insert it as YYYY-MM-DD." , centerX, centerY - 3, redOnBlack)
				queryArray[pos - 1] = None
		if pos == 5:
			placeUserInput(window, centerX, centerY + pos, pos, multiFlag)
			window.addstr(0,0, "end time")
			#validate the ending time
			try:
				begTime = datetime.strptime(queryArray[pos - 1], '%H:%M')
			except:
				placeMenu(window, "Incorrect date format, please insert it as HH:MM." , centerX, centerY - 3, redOnBlack)
				queryArray[pos - 1] = None
		if pos == 6:
			pos = 'Back'
			window.addstr(0,0, "back")
	else:
		curses.beep
		window.addstr(0,0, "%s" %char)
			
	return pos

def singleUserTime(stdscr):
	stdscr.clear()
	stdscr.border()
	#setup our large window and box it
	singleUserScreen = stdscr.subwin(0,0)
	singleUserScreen.box()
	#get the max x and y so we can do the center
	y, x = singleUserScreen.getmaxyx() 
	singleUserScreen.refresh()
	#find the center of the screen
	centerY, centerX = center(singleUserScreen)
	#set the position to 1 initially
	pos = 1
	
	while True:
		
		#place the meny items in the center and center it on the middle item
		string = "All Open Times with the Users Listed"
		thisX = centerX - len(string) / 2
		singleUserScreen.addstr(centerY - 6, thisX, string, curses.A_BOLD | curses.A_UNDERLINE)
		
		
		#places the screen for the user to see
		placeUserMenu(singleUserScreen, centerX, centerY, pos, stdscr)
		
		#refresh to show the new style and get char to pause
		singleUserScreen.refresh()
		char = singleUserScreen.getch()
		
		#get the users input for what to do
		pos = getInput(singleUserScreen, char, pos, stdscr, "single", "time")
		
		
		if pos == 'Back':
			#refresh the queryarray so we don't keep it around
			for i in range(len(queryArray)):
				queryArray[i] = None
			#refresh the screen		
			stdscr.clear()
			stdscr.refresh()
			stdscr.box()
			return
 
	return
	
def multipleUserUser(stdscr):
	stdscr.clear()
	stdscr.border()
	#setup our large window and box it
	multiUserScreen = stdscr.subwin(0,0)
	multiUserScreen.box()
	#get the max x and y so we can do the center
	y, x = multiUserScreen.getmaxyx() 
	multiUserScreen.refresh()
	#find the center of the screen
	centerY, centerX = center(multiUserScreen)
	#set the position to 1 initially
	pos = 1
	
	while True:
		#place the meny items in the center and center it on the middle item
		string = "All Open Times with the Users Listed"
		thisX = centerX - len(string) / 2
		multiUserScreen.addstr(centerY - 6, thisX, string, curses.A_BOLD | curses.A_UNDERLINE)
		
		#places the screen for the user to see
		placeUserMenu(multiUserScreen, centerX, centerY, pos, stdscr)
		
		#refresh to show the new style and get char to pause
		multiUserScreen.refresh()
		char = multiUserScreen.getch()
	
		#get the users input for what to do
		pos = getInput(multiUserScreen, char, pos, stdscr, "multi", "user")
			
		if pos == 'Back':
			#refresh the queryarray so we don't keep it around
			for i in range(len(queryArray)):
				queryArray[i] = None
			#refresh the screen		
			stdscr.clear()
			stdscr.refresh()
			stdscr.box()
			return	
			
	return

def multipleUserTime(stdscr):
	stdscr.clear()
	stdscr.border()
	#setup our large window and box it
	multiTimeScreen = stdscr.subwin(0,0)
	multiTimeScreen.box()
	#get the max x and y so we can do the center
	y, x = multiTimeScreen.getmaxyx() 
	multiTimeScreen.refresh()
	#find the center of the screen
	centerY, centerX = center(multiTimeScreen)
	#set the position to 1 initially
	pos = 1
	
	while True:
		#place the meny items in the center and center it on the middle item
		string = "All Open Times with the Users Listed"
		thisX = centerX - len(string) / 2
		multiTimeScreen.addstr(centerY - 6, thisX, string, curses.A_BOLD | curses.A_UNDERLINE)
		
		#places the screen for the user to see
		placeUserMenu(multiTimeScreen, centerX, centerY, pos, stdscr)
		#refresh to show the new style and get char to pause
		multiTimeScreen.refresh()
		char = multiTimeScreen.getch()
	
		#get the users input for what to do
		pos = getInput(multiTimeScreen, char, pos, stdscr, "multi", "time")
			
		if pos == 'Back':
			#refresh the queryarray so we don't keep it around
			for i in range(len(queryArray)):
				queryArray[i] = None
			#refresh the screen		
			stdscr.clear()
			stdscr.refresh()
			stdscr.box()
			return	

	return
	


def refreshUser(stdscr):
	stdscr.clear()
	stdscr.border()
	#setup our large window and box it
	refreshUserScreen = stdscr.subwin(0,0)
	refreshUserScreen.box()
	#get the max x and y so we can do the center
	y, x = refreshUserScreen.getmaxyx() 
	refreshUserScreen.refresh()
	#find the center of the screen
	centerY, centerX = center(refreshUserScreen)
		
	#set the input to nothing
	yesNo = ""
	
	#not using a menu so there aren't weird bolded items except for back
	string = "Refresh Users"
	thisX = centerX - len(string) / 2
	refreshUserScreen.addstr(centerY - 3, thisX, string)
	
	string = "Are you sure? (Y/N)"
	thisX = centerX - len(string) / 2
	refreshUserScreen.addstr(centerY - 1, thisX, string[:15])
	refreshUserScreen.addstr(centerY - 1, thisX + 15, string[15:16], curses.A_BOLD | curses.A_UNDERLINE)
	refreshUserScreen.addstr(centerY - 1, thisX + 16, string[16:17])
	refreshUserScreen.addstr(centerY - 1, thisX + 17, string[17:18], curses.A_BOLD | curses.A_UNDERLINE)
	refreshUserScreen.addstr(centerY - 1, thisX + 18, string[18:19])

	string = "This will take XX minutes, or so." 
	thisX = centerX - len(string) / 2
	refreshUserScreen.addstr(centerY, thisX, string)
	
	string = "Back to Home"
	thisX = centerX - len(string) / 2
	refreshUserScreen.addstr(centerY + 1, thisX, string[:1], curses.A_BOLD | curses.A_UNDERLINE)
	refreshUserScreen.addstr(centerY + 1, thisX + 1, string[1:])
	
	
	while True:
		#post all and get char
		refreshUserScreen.refresh()
		char = refreshUserScreen.getch()
		
		#get the users input
		if char == ord('Y') or char == ord('y'):
			refreshUserScreen.addstr(0,0,"yes")
			yesNo = "yes"
		elif char == ord('N') or char == ord('n'):
			refreshUserScreen.addstr(0,0,"no")
			refreshUserScreen.clear()
			stdscr.box()
			return
		elif char == ord('b') or char == ord('B') or char == ord('q') or char == ord('Q'):
			refreshUserScreen.addstr(0,0,"back")
			refreshUserScreen.clear()
			stdscr.box()
			return
			#homeScreen(stdscr) #back to the homescreen
		elif char == ord('\n') or char == curses.KEY_ENTER:
			if yesNo == "yes":
				refreshUserScreen.addstr(0,0,"yes2")
				refreshUserScreen.refresh()
				#run the couse refresh code
		else:
			curses.beep
			refreshUserScreen.addstr(0,0,"not used")
	
	return
	
def refreshCourses(stdscr):
	stdscr.clear()
	stdscr.border()
	#setup our large window and box it
	refreshCourseScreen = stdscr.subwin(0,0)
	refreshCourseScreen.box()
	#get the max x and y so we can do the center
	y, x = refreshCourseScreen.getmaxyx() 
	refreshCourseScreen.refresh()
	#find the center of the screen
	centerY, centerX = center(refreshCourseScreen)
	#set the input to nothing
	yesNo = ""
	
	#not using a menu so there aren't bolded menu items except for back
	string = "Refresh Courses"
	thisX = centerX - len(string) / 2
	refreshCourseScreen.addstr(centerY - 3, thisX, string)
	
	string = "Are you sure? (Y/N)"
	thisX = centerX - len(string) / 2
	refreshCourseScreen.addstr(centerY - 1, thisX, string[:15])
	refreshCourseScreen.addstr(centerY - 1, thisX + 15, string[15:16], curses.A_BOLD | curses.A_UNDERLINE)
	refreshCourseScreen.addstr(centerY - 1, thisX + 16, string[16:17])
	refreshCourseScreen.addstr(centerY - 1, thisX + 17, string[17:18], curses.A_BOLD | curses.A_UNDERLINE)
	refreshCourseScreen.addstr(centerY - 1, thisX + 18, string[18:19])

	string = "This will take XX minutes, or so." 
	thisX = centerX - len(string) / 2
	refreshCourseScreen.addstr(centerY, thisX, string)
	
	string = "Back to Home"
	thisX = centerX - len(string) / 2
	refreshCourseScreen.addstr(centerY + 1, thisX, string[:1], curses.A_BOLD | curses.A_UNDERLINE)
	refreshCourseScreen.addstr(centerY + 1, thisX + 1, string[1:])
		
	while True:
		#post everything
		refreshCourseScreen.refresh()
		char = refreshCourseScreen.getch()
		#get the users input
		if char == ord('Y') or char == ord('y'):
			refreshCourseScreen.addstr(0,0,"yes")
			yesNo = "yes"
		elif char == ord('N') or char == ord('n'):
			refreshCourseScreen.addstr(0,0,"no")
			refreshCourseScreen.clear()
			stdscr.box()
			return
		elif char == ord('b') or char == ord('B') or char == ord('q') or char == ord('Q'):
			refreshCourseScreen.addstr(0,0,"back")
			refreshCourseScreen.clear()
			stdscr.box()
			return
			#homeScreen(stdscr) #back to the homescreen
		elif char == ord('\n') or char == curses.KEY_ENTER:
			if yesNo == "yes":
				refreshCourseScreen.addstr(0,0,"yes2")
				refreshCourseScreen.refresh()
				#run the couse refresh code
		else:
			curses.beep
			refreshCourseScreen.addstr(0,0,"not used")
	
	#end
	return
	
def homeScreen(stdscr):
	#setup the colors for the text
	curses.init_pair(1, curses.COLOR_BLUE , curses.COLOR_WHITE)
	curses.init_pair(2, curses.COLOR_GREEN , curses.COLOR_BLACK)
	
	blueOnWhite = 1
	greenOnBlack = 2

	#setup our large window and box it
	bigScreen = stdscr.subwin(0,0)
	bigScreen.box()
	bigScreen.keypad(1)
	#get the max x and y so we can do the center
	y, x = bigScreen.getmaxyx() 
	bigScreen.refresh()
	#find the center of the screen
	centerY, centerX = center(bigScreen)
	#set the position to 1 initially
	pos = 1
	
	
	while True:
		#place the menu items in the center and center it on the middle item
		string = "Home Page"
		thisX = centerX - len(string) / 2
		bigScreen.addstr(centerY - 5, thisX, string, curses.A_BOLD | curses.A_UNDERLINE)
		
		#shows where we are based on arrows and position 
		if pos == 1:
			placeMenu(bigScreen, "1 - Find Open Time, Single" , centerX, centerY - 2, blueOnWhite)
		else:
			placeMenu(bigScreen, "1 - Find Open Time, Single" , centerX, centerY - 2, greenOnBlack)
		if pos == 2:
			placeMenu(bigScreen, "2 - Find Available Users", centerX, centerY - 1, blueOnWhite)
		else:
			placeMenu(bigScreen, "2 - Find Available Users", centerX, centerY - 1, greenOnBlack)
		if pos == 3:
			placeMenu(bigScreen, "3 - Find Open Time, Group", centerX, centerY, blueOnWhite)
		else:
			placeMenu(bigScreen, "3 - Find Open Time, Group", centerX, centerY, greenOnBlack)
		if pos == 4:
			placeMenu(bigScreen, "4 - Refresh User", centerX, centerY + 1, blueOnWhite)
		else:
			placeMenu(bigScreen, "4 - Refresh User", centerX, centerY + 1, greenOnBlack)
		if pos == 5:
			placeMenu(bigScreen, "5 - Refresh Catalog", centerX, centerY + 2, blueOnWhite)
		else:
			placeMenu(bigScreen, "5 - Refresh Catalog", centerX, centerY + 2, greenOnBlack)
		if pos == 6:
			placeMenu(bigScreen, "6 - Quit", centerX, centerY + 3, blueOnWhite) 
		else:
			placeMenu(bigScreen, "6 - Quit", centerX, centerY + 3, greenOnBlack)
	
		bigScreen.addstr(0,0, "%s" % pos)
		#gets the character and chooses or moves it
		bigScreen.refresh()
		char = bigScreen.getch()

		#get the users input 
		if char == ord('1'):
			pos = 1
		elif char == ord('2'):
			pos = 2
		elif char == ord('3'):
			pos = 3
		elif char == ord('4'):
			pos = 4
		elif char == ord('5'):
			pos = 5
		elif char == ord('6'):
			pos = 6
		elif char == ord('q'):
			break #exits the program
		elif char == curses.KEY_DOWN:
			#wrap around positions going down
			if pos < 6:
				pos += 1
			else: 
				pos = 1
		elif char == curses.KEY_UP:
			#wrap around positions going up
			if pos > 1:
				pos -= 1
			else: 
				pos = 6
		#when the user hits enter
		elif char == ord('\n') or char == curses.KEY_ENTER:
			#depending on the position do the certain functions
			if pos == 1:
				singleUserTime(stdscr)
			if pos == 2:
				multipleUserUser(stdscr)
			if pos == 3:
				multipleUserTime(stdscr)
			if pos == 4:
				refreshUser(stdscr)
			if pos == 5:
				refreshCourses(stdscr)
			if pos == 6:
				#quit the progran
				break
		else:
			curses.beep
			bigScreen.addstr(0,0, "none")

	#end the main/all program
	return
		
if __name__ == '__main__':
	try:
		#initialize the screen
		stdscr = curses.initscr() 
		curses.start_color()
		#turn off the echo
		curses.noecho()
		#make it so they have to hit enter first
		curses.cbreak()
		#enable the keypad
		stdscr.keypad(1)

		#go to the home screen (ie main basically)
		homeScreen(stdscr)
		
		#when they com out of main terminate curses
		curses.nocbreak()
		stdscr.keypad(0)
		curses.echo()
		curses.endwin()
	except:
		#to terminate curses if something fails
		curses.nocbreak()
		stdscr.keypad(0)
		curses.echo()
		curses.endwin()
		

		'''
def addUser(stdscr):
	stdscr.clear()
	stdscr.border()
	#setup the colors for the text
	curses.init_pair(1, curses.COLOR_BLUE , curses.COLOR_WHITE)
	curses.init_pair(2, curses.COLOR_GREEN , curses.COLOR_BLACK)

	blueOnWhite = 1
	greenOnBlack = 2


	#setup our large window and box it
	addUserScreen = stdscr.subwin(0,0)
	addUserScreen.box()
	#get the max x and y so we can do the center
	y, x = addUserScreen.getmaxyx() 
	addUserScreen.refresh()
	#find the center of the screen
	y,x = center(addUserScreen)
	#set the position to 1 initially
	pos = 1

	

	while True:
		#place the meny items in the center and center it on the middle item
		string = "Add a User"
		thisX = x - len(string) / 2
		addUserScreen.addstr(y - 3, thisX, string, curses.A_BOLD | curses.A_UNDERLINE)

		#shows where we are based on arrows and position 
		if pos == 1:
			placeMenu(addUserScreen, "1 - Username" , x, y - 2, blueOnWhite)
		else:
			placeMenu(addUserScreen, "1 - Username" , x, y - 2, greenOnBlack)
		if pos == 2:
			placeMenu(addUserScreen, "2 - First Name", x, y - 1, blueOnWhite)
		else:
			placeMenu(addUserScreen, "2 - First Name", x, y - 1, greenOnBlack)
		if pos == 3:
			placeMenu(addUserScreen, "3 - Last Name", x, y, blueOnWhite)
		else:
			placeMenu(addUserScreen, "3 - Last Name", x, y, greenOnBlack)
		if pos == 4:
			placeMenu(addUserScreen, "4 - Division (Of the form College of X)", x, y + 1, blueOnWhite)
		else:
			placeMenu(addUserScreen, "4 - Division (Of the form College of X)", x, y + 1, greenOnBlack)
		if pos == 5:
			placeMenu(addUserScreen, "5 - Insert", x, y + 2, blueOnWhite)
		else:
			placeMenu(addUserScreen, "5 - Insert", x, y + 2, greenOnBlack)
		if pos == 6:
			#special for back to have B go back as well
			string = "6 - Back to Home"

			placeMenu(addUserScreen, string, x, y + 3, blueOnWhite)
			thisX = x - 30
			addUserScreen.addstr(y + 3, thisX + 4, string[4:5], curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(blueOnWhite))
			
			addUserScreen.addstr(y + 3, x, string[:1], curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(greenOnBlack))
			addUserScreen.addstr(y + 3, x + 1, string[1:4], curses.color_pair(blueOnWhite))
			addUserScreen.addstr(y + 3, x + 4, string[4:5], curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(blueOnWhite))
			addUserScreen.addstr(y + 3, x + 5, string[5:], curses.color_pair(blueOnWhite))
		else:
			string = "6 - Back to Home"
			placeMenu(addUserScreen, string, x, y + 3, greenOnBlack)
			thisX = x - 30
			addUserScreen.addstr(y + 3, thisX + 4, string[4:5], curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(greenOnBlack))
			
			addUserScreen.addstr(y + 3, x, string[:1], curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(greenOnBlack))
			addUserScreen.addstr(y + 3, x + 1, string[1:4], curses.color_pair(greenOnBlack))
			addUserScreen.addstr(y + 3, x + 4, string[4:5], curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(greenOnBlack))
			addUserScreen.addstr(y + 3, x + 5, string[5:], curses.color_pair(greenOnBlack))
			
			
		addUserScreen.refresh()
		char = addUserScreen.getch()
	
		#get the users input 
		if char == ord('1'):
			pos = 1
		elif char == ord('2'):
			pos = 2
		elif char == ord('3'):
			pos = 3
		elif char == ord('4'):
			pos = 4
		elif char == ord('5'):
			pos = 5
		elif char == ord('6'):
			pos = 6		
		elif char == curses.KEY_DOWN or char == 66:
			#wrap around positions going down
			if pos < 6:
				pos += 1
			else: 
				pos = 1
		elif char == curses.KEY_UP or char == 65:
			#wrap around positions going up
			if pos > 1:
				pos -= 1
			else: 
				pos = 6
		elif char == ord('b') or char == ord('B'):
			addUserScreen.clear()
			stdscr.box()
			return
		#when the user hits enter
		elif char == ord('\n') or char == curses.KEY_ENTER:
			#depending on the position do the certain functions
			if pos == 1:
				addUserScreen.addstr(0,0, "user")
			if pos == 2:
				addUserScreen.addstr(0,0, "first")
			if pos == 3:
				addUserScreen.addstr(0,0, "last")
			if pos == 4:
				addUserScreen.addstr(0,0, "division")
			if pos == 5:
				addUserScreen.addstr(0,0, "insert")
			if pos == 6:
				addUserScreen.clear()
				stdscr.box()
				return
		else:
			curses.beep
			addUserScreen.addstr(0,0, "none")
	
	return
'''

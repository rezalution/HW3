#!/usr/bin/env python

import curses
from curses import wrapper 


def center (window):
	y, x = window.getmaxyx()

	
	centerY = (y / 2)
	centerX = (x / 2)

	return centerY,  centerX

def placeMenu(window, string, x, y, colorPair):
	

	thisX = x - len(string) / 2
	#print "%s" % colorPair
	#window.getch()
	window.addstr(y, thisX, string[:1], curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(colorPair))
	window.addstr(y, thisX + 1, string[1:], curses.color_pair(colorPair))

	return
	

def placeUserMenu(window, centerX, centerY, pos, singleOrMulti, stdscr):
	#setup the colors for the text
	curses.init_pair(1, curses.COLOR_BLUE , curses.COLOR_WHITE)
	curses.init_pair(2, curses.COLOR_GREEN , curses.COLOR_BLACK)

	blueOnWhite = 1
	greenOnBlack = 2	
	#shows where we are based on arrows and position 
	if pos == 1:
		placeMenu(window, "1 - User email or onid id:", centerX, centerY - 4, blueOnWhite)
		#add directions if it is the multi user search
		if multi == "multi":
			thisX = x - len("1 - User email or onid id:") / 2
			thisX += len("1 - User email or onid id:")
			window.addstr(centerY - 4, thisX, "(Use comma to separate users)", blueOnWhite)
	else:
		placeMenu(window, "1 - User email or onid id:" , centerX, centerY - 4, greenOnBlack)
		#add directions if it is the multi user search
		if multi == "multi":
			thisX = x - len("1 - User email or onid id:") / 2
			thisX += len("1 - User email or onid id:")
			window.addstr(centerY - 4, thisX, "(Use comma to separate users)", greenOnBlack)
	if pos == 2:
		placeMenu(window, "2 - Beginning Date", centerX, centerY - 3, blueOnWhite)
	else:
		placeMenu(window, "2 - Beginning Date", centerX, centerY - 3, greenOnBlack)
	if pos == 3:
		placeMenu(window, "3 - Beginning Time", centerX, centerY - 2, blueOnWhite)
	else:
		placeMenu(window, "3 - Beginning Time", centerX, centerY - 2, greenOnBlack)
	if pos == 4:
		placeMenu(window, "4 - End Date", centerX, centerY - 1, blueOnWhite)
	else:
		placeMenu(window, "4 - End Date", centerX, centerY - 1, greenOnBlack)
	if pos == 5:
		placeMenu(window, "5 - End Time", centerX, centerY, blueOnWhite)
	else:
		placeMenu(window, "5 - End Time", centerX, centerY, greenOnBlack)
	if pos == 6:
		placeMenu(window, "6 - Earliest Time of Day", centerX, centerY + 1, blueOnWhite)
	else:
		placeMenu(window, "6 - Earliest Time of Day", centerX, centerY + 1, greenOnBlack)
	if pos == 7:
		placeMenu(window, "7 - Latest Time of Day", centerX, centerY + 2, blueOnWhite)
	else:
		placeMenu(window, "7 - Latest Time of Day", centerX, centerY + 2, greenOnBlack)
	if pos == 8:
		placeMenu(window, "8 - Days to Search (any mix of UMTWRFS)", centerX, centerY + 3, blueOnWhite)
	else:
		placeMenu(window, "8 - Days to Search (any mix of UMTWRFS)", centerX, centerY + 3, greenOnBlack)
	if pos == 9:
		#special for back to have B go back as well
		string = "9 - Back to Home"
		thisX = x - len(string) / 2
		window.addstr(centerY + 4, thisX, string[:1], curses.A_BOLD | curses.A_UNDERLINE | greenOnBlack)
		window.addstr(centerY + 4, thisX + 1, string[1:4], greenOnBlack)
		window.addstr(centerY + 4, this + 4, string[4:5], curses.A_BOLD | curses.A_UNDERLINE | greenOnBlack)
		window.addstr(centerY + 4, this + 5, string[5:], greenOnBlack)
	else:
		string = "9 - Back to Home"
		thisX = x - len(string) / 2
		window.addstr(centerY + 4, thisX, string[:1], curses.A_BOLD | curses.A_UNDERLINE | greenOnBlack)
		window.addstr(centerY + 4, thisX + 1, string[1:4], greenOnBlack)
		window.addstr(centerY + 4, this + 4, string[4:5], curses.A_BOLD | curses.A_UNDERLINE | greenOnBlack)
		window.addstr(centerY + 4, this + 5, string[5:], greenOnBlack)

	return
	
	
def getInput(window, char, pos, stdscr):
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
	elif char == ord('7'):
		pos = 7
	elif char == ord('8'):
		pos = 8
	elif char == ord('9'):
		pos = 9
	elif char == ord('b') or char == ord('B'):
		homeScreen(stdscr) #exits
	elif char == curses.KEY_DOWN:
		#wrap around positions going down
		if pos < 9:
			pos += 1
		else: 
			pos = 1
	elif char == curses.KEY_UP:
		#wrap around positions going up
		if pos > 1:
			pos -= 1
		else: 
			pos = 9
	#when the user hits enter
	elif char == ord('\n') or char == curses.KEY_ENTER:
		#depending on the position do the certain functions
		if pos == 1:
			window.addstr(0,0, "user")
		if pos == 2:
			window.addstr(0,0, "beg date")
		if pos == 3:
			window.addstr(0,0, "beg time")
		if pos == 4:
			window.addstr(0,0, "end date")
		if pos == 5:
			window.addstr(0,0, "end time")
		if pos == 6:
			window.addstr(0,0, "early time")
		if pos == 7:
			window.addstr(0,0, "latest time")
		if pos == 8:
			window.addstr(0,0, "days")
		if pos == 9:
			window.addstr(0,0, "back")
			homeScreen(stdscr)
	else:
		curses.beep
		window.addstr(0,0, "none")
			
	
	return pos
		

def singleUserTime(stdscr):

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
		placeMenu(singleUserScreen, "All Open Times with the Users Listed", centerX, centerY - 6)
		
		#places the screen for the user to see
		placeUserMenu(singleUserScreen, centerX, centerY, pos, "single", stdscr)
			
		#refresh to show the new style and get char to pause
		singleUserScreen.refresh()
		char = singleUserScreen.getch()
	
		#get the users input for what to do
		pos = getInput(singleUserScreen, char, pos, stdscr)
	
	return
	
def multipleUserUser(stdscr):

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
		placeMenu(multiUserScreen, "All Open Times with the Users Listed", centerX, centerY - 6)
		
		#places the screen for the user to see
		placeUserMenu(multiUserScreen, centerX, centerY, pos, "multi", stdscr)
		
		#refresh to show the new style and get char to pause
		multiUserScreen.refresh()
		char = multiUserScreen.getch()
	
		#get the users input for what to do
		pos = getInput(singleUserScreen, char, pos, stdscr)
			
			
	
def multipleUserTime(stdscr):
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
		placeMenu(multiTimeScreen, "All Open Times with the Users Listed", centerX, centerY - 6)
		
		#places the screen for the user to see
		placeUserMenu(multiTimeScreen, centerX, centerY, pos, "multi", stdscr)
		#refresh to show the new style and get char to pause
		multiTimeScreen.refresh()
		char = multiTimeScreen.getch()
	
		#get the users input for what to do
		pos = getInput(singleUserScreen, char, pos, stdscr)
			
			
	return
	
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
	centerY, centerX = center(addUserScreen)
	#set the position to 1 initially
	pos = 1

	

	while True:
		#place the meny items in the center and center it on the middle item
		string = "Add a User"
		thisX = centerX - len(string) / 2
		addUserScreen.addstr(centerY - 3, thisX, string, curses.A_BOLD | curses.A_UNDERLINE)

		#shows where we are based on arrows and position 
		if pos == 1:
			placeMenu(addUserScreen, "1 - Username" , centerX, centerY - 2, blueOnWhite)
		else:
			placeMenu(addUserScreen, "1 - Username" , centerX, centerY - 2, greenOnBlack)
		if pos == 2:
			placeMenu(addUserScreen, "2 - First Name", centerX, centerY - 1, blueOnWhite)
		else:
			placeMenu(addUserScreen, "2 - First Name", centerX, centerY - 1, greenOnBlack)
		if pos == 3:
			placeMenu(addUserScreen, "3 - Last Name", centerX, centerY, blueOnWhite)
		else:
			placeMenu(addUserScreen, "3 - Last Name", centerX, centerY, greenOnBlack)
		if pos == 4:
			placeMenu(addUserScreen, "4 - Division (Of the form College of X)", centerX, centerY + 1, blueOnWhite)
		else:
			placeMenu(addUserScreen, "4 - Division (Of the form College of X)", centerX, centerY + 1, greenOnBlack)
		if pos == 5:
			placeMenu(addUserScreen, "5 - Insert", centerX, centerY + 2, blueOnWhite)
		else:
			placeMenu(addUserScreen, "5 - Insert", centerX, centerY + 2, greenOnBlack)
		if pos == 6:
			#special for back to have B go back as well
			string = "6 - Back to Home"
			thisX = centerX - len(string) / 2
			
			addUserScreen.addstr(centerY + 3, thisX, string[:1], curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(greenOnBlack))
			addUserScreen.addstr(centerY + 3, thisX + 1, string[1:4], curses.color_pair(blueOnWhite))
			addUserScreen.addstr(centerY + 3, thisX + 4, string[4:5], curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(blueOnWhite))
			addUserScreen.addstr(centerY + 3, thisX + 5, string[5:], curses.color_pair(blueOnWhite))
		else:
			string = "6 - Back to Home"
			thisX = centerX - len(string) / 2
			addUserScreen.addstr(centerY + 3, thisX, string[:1], curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(greenOnBlack))
			addUserScreen.addstr(centerY + 3, thisX + 1, string[1:4], curses.color_pair(greenOnBlack))
			addUserScreen.addstr(centerY + 3, thisX + 4, string[4:5], curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(greenOnBlack))
			addUserScreen.addstr(centerY + 3, thisX + 5, string[5:], curses.color_pair(greenOnBlack))
			
			
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
		elif char == ord('b') or char == ord('B'):
			addUserScreen.clear()
			stdscr.box()
			return
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
	
	#post everything
	#print "yo"
	
	
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
			refreshUserScreen.addstr(0,0,"nack")
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
	
	
	#not using a menu so there aren't weird bolded items except for back
	string = "Refresh Courses"
	thisX = centerX - len(string) / 2
	refreshCourseScreen.addstr(centerY - 3, thisX, string)
	
	string = "Are you sure? (Y/N)"
	thisX = centerX - len(string) / 2
	refreshCourseScreen.addstr(centerY - 1, thisX, string)
	
	string = "This will take 15 minutes, or so." 
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
			refreshCourseScreen.addstr(0,0,"nack")
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
		#place the meny items in the center and center it on the middle item
		string = "Home Page"
		thisX = centerX - len(string) / 2
		bigScreen.addstr(centerY - 5, thisX, string, curses.A_BOLD | curses.A_UNDERLINE)
		
		#shows where we are based on arrows and position 
		if pos == 1:
			placeMenu(bigScreen, "1 - Find Open Time, Single" , centerX, centerY - 3, blueOnWhite)
		else:
			placeMenu(bigScreen, "1 - Find Open Time, Single" , centerX, centerY - 3, greenOnBlack)
		if pos == 2:
			placeMenu(bigScreen, "2 - Find Available Users", centerX, centerY - 2, blueOnWhite)
		else:
			placeMenu(bigScreen, "2 - Find Available Users", centerX, centerY - 2, greenOnBlack)
		if pos == 3:
			placeMenu(bigScreen, "3 - Find Open Time, Group", centerX, centerY - 1, blueOnWhite)
		else:
			placeMenu(bigScreen, "3 - Find Open Time, Group", centerX, centerY - 1, greenOnBlack)
		if pos == 4:
			placeMenu(bigScreen, "4 - Add User", centerX, centerY, blueOnWhite)
		else:
			placeMenu(bigScreen, "4 - Add User", centerX, centerY, greenOnBlack)
		if pos == 5:
			placeMenu(bigScreen, "5 - Refresh User", centerX, centerY + 1, blueOnWhite)
		else:
			placeMenu(bigScreen, "5 - Refresh User", centerX, centerY + 1, greenOnBlack)
		if pos == 6:
			placeMenu(bigScreen, "6 - Refresh Catalog", centerX, centerY + 2, blueOnWhite)
		else:
			placeMenu(bigScreen, "6 - Refresh Catalog", centerX, centerY + 2, greenOnBlack)
		if pos == 7:
			placeMenu(bigScreen, "7 - Quit", centerX, centerY + 3, blueOnWhite) 
		else:
			placeMenu(bigScreen, "7 - Quit", centerX, centerY + 3, greenOnBlack)
	
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
		elif char == ord('7'):
			pos = 7
		elif char == ord('q'):
			break #exits
		elif char == curses.KEY_DOWN:
			#wrap around positions going down
			if pos < 7:
				pos += 1
			else: 
				pos = 1
		elif char == curses.KEY_UP:
			#wrap around positions going up
			if pos > 1:
				pos -= 1
			else: 
				pos = 7
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
				addUser(stdscr)
			if pos == 5:
				refreshUser(stdscr)
			if pos == 6:
				refreshCourses(stdscr)
			if pos == 7:
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
		

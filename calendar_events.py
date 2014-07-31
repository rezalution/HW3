from authorize_calendar import *
import time

calendar_id = 'cs419.team4@gmail.com'

# calendar_list_entry = service.calendarList().get(calendarId=calendar_id).execute()


def list_calendar_events():
	page_token = None
	while True:
		events = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
		if events['items']:
	  		events_list = []
	  		today = time.strftime("%Y-%m-%d")
	    	for event in events['items']:
	    		if event['start']['dateTime'][:10] == today:
	    			# print event['summary']
	    			events_list.append(event)
	    	return events_list
		page_token = events.get('nextPageToken')
		if not page_token:
			break

def get_event_by_id(event_id):
	events_list = list_calendar_events()
	for event in events_list:
		if event['id'] == event_id:
			return event

def twilio_info():
	# saves the list of today's events to a variable when the user syncs their calendar with the app
	events_today = list_calendar_events()
	# print events_today
	# print events_today
	description = []
	title = []
	start_time = []
	for event in events_today:
		description.append(event['description'])
		title.append(event['summary'])
		start_time.append(event['start']['dateTime'])
	all_events = zip(title, description, start_time)
	# returns a list of tuples with all the information ready for Twilio's API to use
	return all_events

# def debrief():
# 	events_today = list_calendar_events()
# 	titles = []
# 	dates = []
# 	formatted_dates = []
# 	for event in events_today:
# 		titles.append(event['summary'])
# 		dates.append(event['start']['dateTime'])
# 	for date in dates:
# 		time_1 = int(date[11:13]) - 12
# 		adjusted_time = str(time_1) + ":" + str(date[14:16])
# 		formatted_dates.append(adjusted_time)
# 	debriefing_info = zip(titles, formatted_dates)
# 	return debriefing_info 

# debrief()
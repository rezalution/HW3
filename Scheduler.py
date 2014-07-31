# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

print "hello world"

# <codecell>

from apiclient.discovery import build

# <codecell>

from oauth2client.client import OAuth2WebServerFlow

# <codecell>

import httplib2

# <codecell>

import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret can be found in Google Cloud Console

#Fetch client id and client secret from a file
lines = open("API_CREDENTIALS","r").readlines()
client_id_from_file = lines[0].strip("\r").strip("\n").trim(" ")
clinet_secret_from_file = lines[1].strip("\r").strip("\n").trim(" ")
FLOW = OAuth2WebServerFlow(
    client_id=client_id_from_file,
    client_secret=clinet_secret_from_file,
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='Scheduler/1.0')

# To disable the local server feature, uncomment the following line:
FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage('calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google Cloud Console
# to get a developerKey for your own application.
service = build(serviceName='calendar', version='v3', http=http)
#,
       #developerKey='AIzaSyCeELBlxSDK_26Y3WKW4VeesKZ5vYTU2uM')

# <codecell>

#Note: Created a new client ID with native application as an API which corrected the redirect URL.

# <codecell>

calendar = service.calendars().get(calendarId='cs419.team4@gmail.com').execute()

# <codecell>

print calendar['summary']

# <codecell>

#Note: if you ever get the error: Google Calendar API - (403) Access Not Configured', then comment "developerKey" in build function()

# <codecell>

#source:http://stackoverflow.com/questions/16173295/google-calendar-api-403-access-not-configured

# <codecell>

print [item for item in calendar.iteritems()]

# <codecell>

#Let's test printing event details

# <codecell>

page_token = None
while True:
  events = service.events().list(calendarId='primary', pageToken=page_token).execute()
  for event in events['items']:
    print event['summary']
  page_token = events.get('nextPageToken')
  if not page_token:
    break

# <codecell>

#Let's quick add

# <codecell>

created_event = service.events().quickAdd(
    calendarId='primary',
    text='Eat food at home on January 17th 1pm-1:25pm').execute()

print created_event['id']

# <codecell>


# <codecell>

#Try to take list of items and schedule them (write a function)

# <codecell>

class Task:
    """
    This class has important variables and functions related to individual tasks.
    """
    task_name = ""
    task_label = ""
    task_priority = 0 #should be between 0 to 9 (low to high priority)
    task_time_start = 0
    task_time_end = 0
    task_time_zone = "" #evening, afternoon, morning, night
    task_deadline = "" #deadline of the task
    task_score = 0 #should be 0 to 9 (low to high)
    
    def __init__(self, task_name="", task_label="", task_priority=0, task_time_start=0, task_time_end=0, task_time_zone="", task_deadline="", task_score=0):
        """
        This function adds task to the queue
        """
        self.task_name = task_name
        self.task_label = task_label
        self.task_priority = task_priority
        self.task_time_start = task_time_start
        self.task_time_end = task_time_end
        self.task_time_zone = task_time_zone
        self.task_deadline = task_deadline
        self.task_score = task_score
        
class TaskList:
    """
    This class operates on tasks
    """
    taskList = [] #Queue of all tasks
    
    def __init__(self):
        print 'Created operations task object'
        self.taskList = []
    
    def addTask(self, task):
        """
        Adding task to the task list
        """
        self.taskList.append(task)
        print "Added task: ",task.task_name
    
    def removeTask(self, task):
        """
        Remove task from the task list
        """
        print "Remove task: ",task.task_name
    
    def showAllTasks(self):
        """
        Shows all tasks
        """
        for task in self.taskList:
            print task.task_name

# <codecell>

if __name__ == "__main__":
    """
    main function
    """
    print "Testing task list"
    task1 = Task("eat food")
    task2 = Task("read book")
    taskList = TaskList()
    taskList.addTask(task1)
    taskList.addTask(task2)
    print "\nAll tasks:"
    taskList.showAllTasks()

# <codecell>



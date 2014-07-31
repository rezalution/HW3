from google.appengine.ext import ndb
from datetime import datetime

def task_from_event(event):
    task = Task(event=str(event))
    
    if 'summary' in event:
        task.title = event['summary']
    elif 'parentEvent' in event and 'summary' in event['parentEvent']:
        task.title = event['parentEvent']['summary']
    else:
        task.title = 'unavailable'
    
    if 'start' in event:
        #u'2013-11-06T18:00:00-05:00'
        dateTime = event['start']['dateTime'][:-6]
        task.scheduledStart = datetime.strptime(dateTime, '%Y-%m-%dT%H:%M:%S')
    elif 'originalStartTime' in event and 'dateTime' in event['originalStartTime']:
        dateTime = event['originalStartTime']['dateTime'][:-6]
        task.scheduledStart = datetime.strptime(dateTime, '%Y-%m-%dT%H:%M:%S')
    
    return task
    



class Task(ndb.Model):
    title = ndb.StringProperty()
    status = ndb.StringProperty()
    done = ndb.BooleanProperty()
    scheduledStart = ndb.DateTimeProperty()
    providerType = ndb.StringProperty()
    providerId = ndb.StringProperty()
    event = ndb.BlobProperty()
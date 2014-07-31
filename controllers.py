import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
from models import Task
import json
from datetime import datetime
import time

def user_key():
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('User', users.get_current_user().user_id())

def for_json(entity):
    json_obj = entity.to_dict()
    json_obj["id"] = entity.key.id()
    if (entity.scheduledStart):
        json_obj["scheduledStart"] = int(time.mktime(entity.scheduledStart.timetuple())) * 1000
    return json_obj

class TaskCollectionController(webapp2.RequestHandler):
    def get(self):
        tasks = Task.query(ancestor=user_key()).fetch()
        self.response.write(json.dumps([for_json(task) for task in tasks]))
    def post(self):
        payload = json.loads(self.request.body)
        task = Task(parent=user_key())
                    #scheduledStart = datetime.fromtimestamp(int(payload['scheduledStart'] / 1000)),
                    #title = payload['title'])                    
        task.put()
        self.response.write(json.dumps(for_json(task)))
        
class TaskController(webapp2.RequestHandler):
    def put(self, taskId):
        taskKey = ndb.Key('User', users.get_current_user().user_id(), 'Task', int(taskId))
        task = taskKey.get()
        payload = json.loads(self.request.body)
        if 'status' in payload: task.status = payload['status']
        task.title = payload['title']
        #task.scheduledStart = datetime.fromtimestamp(int(payload['scheduledStart']) / 1000)
        task.put()
        self.response.write(json.dumps(for_json(task)))
    def get(self, taskId):
        taskKey = ndb.Key('User', users.get_current_user().user_id(), 'Task', int(taskId))
        task = taskKey.get()
        self.response.write(json.dumps(for_json(task)))
    def delete(self, taskId):
        taskKey = ndb.Key('User', users.get_current_user().user_id(), 'Task', int(taskId))
        taskKey.delete()
        self.response.write("OK")
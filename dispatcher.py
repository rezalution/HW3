from google.appengine.ext import webapp
import jinja2
import os
from google.appengine.api import users
from controllers import TaskController, TaskCollectionController
from google.appengine.ext.ndb.utils import decorator
from oauth2client.appengine import OAuth2DecoratorFromClientSecrets
from apiclient.discovery import build
from models import Task, task_from_event


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'])

decorator = OAuth2DecoratorFromClientSecrets(
  os.path.join(os.path.dirname(__file__), 'client_secrets.json'),
  scope='https://www.googleapis.com/auth/calendar')

service = build('calendar', 'v3')


class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render([]))

class CalendarTestController(webapp.RequestHandler):
    
    @decorator.oauth_required
    def get(self):
        http = decorator.http()
        # Call the service using the authorized Http object.

        eventMap = {}
        
        page_token = None
        while True:
            #events = service.events().instances(calendarId='primary', eventId='cnvv0uak8vh6ies1ap7eif8ee0', pageToken=page_token).execute(http=http)
            events = service.events().list(calendarId='primary', pageToken=page_token).execute(http=http)
            for event in events['items']:
                eventMap[event['id']] = event
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        
        eventTasks = []
        for id, event in eventMap.items():
            if 'recurringEventId' in event:
                parentId = event['recurringEventId']
                if not parentId in eventMap:
                    try:
                        eventMap[parentId] = service.events().get(calendarId='primary', eventId=parentId).execute(http=http)
                    except:
                        eventMap[parentId] = 'error'
                event['parentEvent'] = eventMap[parentId]
 
           
            eventTasks.append(task_from_event(event))

        template = JINJA_ENVIRONMENT.get_template('calTest.html')
        self.response.write(template.render(eventTasks=eventTasks))
        

application = webapp.WSGIApplication([
    ('/api/tasks/(\d+)', TaskController),
    ('/api/tasks', TaskCollectionController),
    ('/calTest', CalendarTestController),
    (decorator.callback_path, decorator.callback_handler()),
    ('/.*', MainPage)
], debug=True)
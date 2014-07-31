import webapp2
from webapp2_extras import sessions
import datetime
import models
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import operator

DEFAULT_CALENDAR_NAME = 'default_name'
def calendar_key(calendar_name=DEFAULT_CALENDAR_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return db.Key.from_path("User's Calendar", calendar_name)

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()
 
# Checking if the user is being registered or not. If yes, retrieve events
class CheckUser(BaseHandler):  
    def post(self):

        username = self.request.get('user_name_log')
        self.session['username'] = username

        q = db.GqlQuery("SELECT * FROM Username WHERE username = :1", username)
        db_user = q.get()

        if (db_user != None):
            #retrieve all the events associated with the username
            db_events = db_user.calendar_entries

            #sort all the events by date
            db_events_sorted = sorted(db_events, key=operator.attrgetter('date'))  
        
            template_values = {
            'events': db_events_sorted,
            }
            #send events to template for rendering
            path = os.path.join(os.path.dirname(__file__),  'templates/events_display.html')
            self.response.out.write(template.render(path, template_values))

        else:
            #add a new user and redirect to add_event page
            new_username = models.Username()
            new_username.username = username  
            new_username.put()
            self.redirect("/static/add_event.html")

#adds events to the database for a specific username        
class Add_Event(BaseHandler):
    def post(self):
        username = self.session.get('username')

        #create a Calendar entity, set the parent key 
        calendar = models.Calendar(parent=calendar_key(username))
        username_get = db.GqlQuery("SELECT * FROM Username WHERE username = :1", username)
        my_username = username_get.get()
        calendar.username = my_username
        calendar.event_description = self.request.get('event_desc')
        #date format
        calendar.date = datetime.datetime.strptime(self.request.get('the_date'),"%Y-%m-%dT%H:%M")
        #save to database
        calendar.put()

        self.redirect("/get")


class Get_Events(BaseHandler):  
    def get(self):
        username = self.session.get('username')
        #
        calendars = db.GqlQuery("SELECT * FROM Calendar WHERE ANCESTOR IS :1", calendar_key(username) )
        calendars_get = calendars.run()

        template_values = {
            'events': calendars_get, 
        }
        
        #send sorted events to template for rendering
        path = os.path.join(os.path.dirname(__file__),  'templates/events_display.html')
        self.response.out.write(template.render(path, template_values))



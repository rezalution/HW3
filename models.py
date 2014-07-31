from google.appengine.ext import db

class Username(db.Model): 
    username = db.StringProperty(default=None)
      
class Calendar (db.Model):
    username =  db.ReferenceProperty(Username, collection_name='calendar_entries')  
    date = db.DateTimeProperty()
    event_description = db.StringProperty(multiline=True)
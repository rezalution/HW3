import gflags
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow

flags = gflags.FLAGS
flow = OAuth2WebServerFlow(
      client_id = 'some_id.apps.googleusercontent.com',
      client_secret = 'some_secret-32ijfsnfkj2jf',
      scope='https://www.googleapis.com/auth/calendar',
      user_agent='Python/2.7')

# to get a link for authentication in a terminal,
# which needs to be opened in a browser anyway
flags.auth_local_webserver = False

# store auth token in a file 'calendar.dat' if it doesn't exist,
# otherwise just use it for authentication
base = os.path.dirname(__file__)
storage = Storage(os.path.join(base, 'calendar.dat'))
credentials = storage.get()
if credentials is None or credentials.invalid == True:
    credentials = run(FLOW, storage)

http = httplib2.Http()
http = credentials.authorize(http)
service = build(serviceName='calendar', version='v3', http=http,
   developerKey='AIzaSyCqjqmwmfCiPgPYBp_hhjmIlabCBO1RxhU')
   
events = service.events().list(calendarId='cs419.team4@gmail.com').execute()
print events
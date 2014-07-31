from flask import Flask, request, redirect, url_for, render_template, request, session  
import twilio.twiml
from client import client
from google_calendar_output import google_calendar_output
from calendar_events import *
import dateutil.parser
from datetime import datetime

app = Flask(__name__)

# ideally for actual app - store users in the database and query them for the personalized greeting
users = {
    "+13057616377": "group4"
}


@app.route("/", methods=['GET','POST'])
def homepage():
    return render_template("home.html", title="Welcome")


@app.route("/choose_event", methods=['GET','POST'])
def calendar_events():
    # list_calendar_events() function calls Google Calendar API to retrieve events for the day
    # Looping over/parsing the start time for each event in the list 
    todays_events = list_calendar_events()
    for event in todays_events:
        dtstr = event['start']['dateTime']
        event['start'] = dateutil.parser.parse(dtstr)
    # In the template - Jinja takes it and loops over it to make each event a link 
    # It also saves the event id from the event and constructs a URL with it to pass over to the next function
    # By doing: url_for("calling_phone", event_id=event.id)
    return render_template("calendar_events.html", title="Today's Events", 
                            events=todays_events, today=datetime.now())


@app.route("/call_me/<string:event_id>", methods=['GET'])
def calling_phone(event_id):
    print event_id
    # /2010-04-01/Accounts/{AccountsSid}/Calls
    # APP - me (server) make a POST Request (to call list resource URI) to start the call
    # After the call is connected - Twilio makes a POST Request on the URL specified
    call = client.calls.create(to="+13057616377", from_="+17866296415", url=url_for("hello_user", event_id=event_id, _external=True))
    return call.sid


@app.route("/redirect_call/<string:event_id>", methods=['GET', 'POST'])
def hello_user(event_id):
    """Transfer user to call"""
    # Use the get() method to find value at that key from POST Request data
    to_number = request.values.get('To', None)
    if to_number in users:
        user = users[to_number]
    else:
        user = "Anonymous"
    # grabs the event by its ID (function in calendar_events.py) and saves it to event variable
    event = get_event_by_id(event_id)

    # My App (server) - HTTP Response with TwiML on what Twilio should do with this call
    response = twilio.twiml.Response()
    response.say("Hello " + user)

    # gets the title of the Google calendar event
    call_info = event['summary']

    # Specify the method here and the url to POST it to
    with response.gather(numDigits=1, action=url_for("handle_key", event_id=event_id), method="POST") as g:
    	g.say("To go through with" + " " + str(call_info) + " " + "Press 1. To postpone the call: Press 2")

    return str(response)
 

@app.route("/dial_number/<string:event_id>", methods=['GET', 'POST'])
def handle_key(event_id):
    """Decides what to do with input gathered - which key is pressed."""

    # Tells it to get the 'Digits' parameter value in the POST Request Body Twilio sent over to this URL
    number_chosen = request.values.get('Digits', None)

    # HTTP Response from server (my app) depends on the number chosen by user
    
    if number_chosen == "1":
        # user choose "1" so HTTP Response from my app (server) is <dial> TwiML
        response = twilio.twiml.Response()

        # here it takes the number from the description in calendar event
        event = get_event_by_id(event_id)
        number_to_call = event['description']

        # HTTP Response with TwiML is <dial>
        # Dials the number 
        response.dial(number_to_call) 
        
        # If <dial> fails then:
        response.say("The call failed, or the remote party hung up. Goodbye.") 
        return str(response)

    elif number_chosen == "2":
        # If user chooses 2 then they are redirected 
        return redirect(url_for("delay_call", event_id=event_id))

    # If the caller pressed anything but 1 or 2, redirect them to the homepage.
    else:
        return redirect("/call_me")


@app.route("/postpone_call/<string:event_id>", methods=['GET','POST'])
def delay_call(event_id):
    """Lets user decide how long to postpone the call for"""
    # my app redirected to this url
    # HTTP Response from my app (server) with TwiML instructions
    # POST Request (Twilio-Client) - sends parameters over to action URL 
    response = twilio.twiml.Response()
    event = get_event_by_id(event_id)
    with response.gather(numDigits=2, action=url_for("sms_to_caller", event_id=event_id), method="POST") as g:
        g.say("Enter how long you want to delay the call for")
    # response.say("You are lazy!")
    return str(response)
 

@app.route("/send_message/<string:event_id>", methods=['GET', 'POST'])
def sms_to_caller(event_id):
    """Sends SMS to person notifying them of the delay"""
    
    # gets the 'digits' data sent over in POST Request 
    delay = request.values.get('Digits', 0)
    delayed_minutes = delay + (' minutes' if delay > 1 else ' minute')

    # constructs the body of the text message
    message = "Hey, just letting you know I am running %s late for our call. Speak to you soon!" % delayed_minutes
    
    # Get number to text from calendar event description
    # event = get_event_by_id(event_id)
    # number_to_text = event['description']
    number_to_text = "+13057616377"

    # texts the call recipient that the person is running late - by the amount of time they entered
    # my app (server) sends a HTTP POST Request to SMS Resource URI
    text = client.sms.messages.create(to=number_to_text, from_="+17866296415",
                                     body=message)

    # TwiML instructions returned after text is sent out
    response = twilio.twiml.Response()
    response.say("This message has been sent, Goodbye!")
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
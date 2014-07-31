# Download the library from twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
 
# Get these credentials from http://twilio.com/user/account
account_sid = "AC7f7948d83b22d3fb77427b825d3851c9"
auth_token = "a3ac2718c31963c84388861a7afbe2c8"
client = TwilioRestClient(account_sid, auth_token)
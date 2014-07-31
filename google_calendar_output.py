import datetime 

google_calendar_output = {
  "kind": "calendar#event",
  "etag": 'etag',
  "id": 'string',
  "status": 'string',
  "htmlLink": 'string',
  "created": datetime.date,
  "updated": datetime.date,
  "summary": 'string',
  "description": '+16155124024',
  "location": 'string',
  "colorId": 'string',
  "creator": {
    "id": 'string',
    "email": 'string',
    "displayName": 'string',
    "self": True
  },
  "organizer": {
    "id": 'string',
    "email": 'string',
    "displayName": 'string',
    "self": True
  },
  "start": {
    "date": 'date',
    "dateTime": datetime.date,
    "timeZone": 'string'
  },
  "end": {
    "date": 'date',
    "dateTime": datetime.date,
    "timeZone": 'string'
  },
  "endTimeUnspecified": False,
  "recurrence": [
    'string'
  ],
  "recurringEventId": 'string',
  "originalStartTime": {
    "date": 'date',
    "dateTime": datetime.date,
    "timeZone": 'string'
  },
  "transparency": 'string',
  "visibility": 'string',
  "iCalUID": 'string',
  "sequence": 10,
  "attendees": [
    {
      "id": 'string',
      "email": 'string',
      "displayName": 'Jesse',
      "organizer": True,
      "self": True,
      "resource": True,
      "optional": True,
      "responseStatus": 'string',
      "comment": 'string',
      "additionalGuests": 0
    }
  ],
  "attendeesOmitted": False,
  "extendedProperties": {
    "private": {
      ('key'): 'string'
    },
    "shared": {
      ('key'): 'string'
    }
  },
  "hangoutLink": 'string',
  "gadget": {
    "type": 'string',
    "title": 'string',
    "link": 'string',
    "iconLink": 'string',
    "width": 30,
    "height": 30,
    "display": 'string',
    "preferences": {
      ('key'): 'string'
    }
  },
  "anyoneCanAddSelf": True,
  "guestsCanInviteOthers": True,
  "guestsCanModify": False,
  "guestsCanSeeOtherGuests": True,
  "privateCopy": False,
  "locked": False,
  "reminders": {
    "useDefault": True,
    "overrides": [
      {
        "method": 'string',
        "minutes": 120
      }
    ]
  }
}
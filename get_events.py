page_token = None
while True:
  events = service.events().list(calendarId='cs419.team4@gmail.com', pageToken=page_token).execute()
  if events['items']:
    for event in events['items']:
      print event['summary']
  page_token = events.get('nextPageToken')
  if not page_token:
    breaks
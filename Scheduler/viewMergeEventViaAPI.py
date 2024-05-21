from collections import defaultdict
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

#The merge block algorithm
def find_available_time_blocks(time_blocks):
    if not time_blocks:
        return []

    merged_blocks = []
    time_blocks.sort(key=lambda x: x[0])  # Sort by start time

    start, end = time_blocks[0]
    print(start,end)
    for block in time_blocks[1:]:
        if block[0] <= end:  # Overlapping or adjacent blocks
            end = max(end, block[1])
        else:  # Non-overlapping block
            merged_blocks.append([start, end])
            start, end = block

    merged_blocks.append([start, end])  # Add the last merged block

    return merged_blocks


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.now()
    over = now + datetime.timedelta(days = 1)
    print(now.isoformat() + "Z" ) # 'Z' indicates UTC time)
    print(over.isoformat() + "Z")  # 'Z' indicates UTC time)
    print("Getting the upcoming 10 events from now to the next day at same time")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now.isoformat() + "Z",  # 'Z' indicates UTC time,
            timeMax=over.isoformat() + "Z",  # 'Z' indicates UTC time,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return
    memberMap = defaultdict(list)
    # Prints the start and name of the next 10 events
    # for event in events:
    #   members = set()
    #   #get the start time, the format is 2024-05-18T08:00:00-04:00
    #   start = datetime.datetime.strptime(event["start"].get("dateTime") , '%Y-%m-%dT%H:%M:%S%z')
    #   end = datetime.datetime.strptime(event["end"].get("dateTime"), '%Y-%m-%dT%H:%M:%S%z') #get the end time
    #   if "attendees" in event:          #use all attnedees as the key if attendees exist
    #      for attendee in event["attendees"]:
    #         members.add(attendee.get("email"))
    #   else:                             #otherwise, only use organizer as the key
    #      members.add(event["organizer"].get("email"))
    #   memberMap[frozenset(members)].append(((start.hour, start.minute, start.second), (end.hour, end.minute, end.second)))
    for event in events:
      members = set()
      #get the start time, the format is 2024-05-18T08:00:00-04:00
      start = event["start"].get("dateTime")
      end = event["end"].get("dateTime")
      if "attendees" in event:          #use all attnedees as the key if attendees exist
         for attendee in event["attendees"]:
            members.add(attendee.get("email"))
      else:                             #otherwise, only use organizer as the key
         members.add(event["organizer"].get("email"))
      memberMap[frozenset(members)].append((start, end))

    # print(memberMap) #To view all the keys and values in the map
    
    for key, blocks in memberMap.items():
      result_block = find_available_time_blocks(blocks) #calling the merge block algorithm
      print(result_block)

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()

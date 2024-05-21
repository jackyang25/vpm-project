from collections import defaultdict
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

#The merge block algorithm
def find_available_time_blocks(time_blocks):
    """
    The input should be valid time blocks in a list form, and the output is a dictionary containing the merged time blocks. The input is garenteed to be none empty
    
    :param time_blocks: The list of time blocks
    :returns: A dictionary with id as key and a list of merged time blocks as value
    
    """


    merged_blocks = defaultdict(list)
    time_blocks.sort(key=lambda x: x[0])  # Sort by start time

    start, end, id = time_blocks[0]
    
    for block in time_blocks[1:]:
        if block[0] <= end:  # Overlapping or adjacent blocks
            end = max(end, block[1])
        else:  # Non-overlapping block
            merged_blocks[id] = (start, end)
            start, end, id = block

    merged_blocks[id] = (start, end)  # Add the last merged block
   
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
      memberMap[frozenset(members)].append((start, end, event["id"]))

    # print(memberMap) #To view all the keys and values in the map
    
    #To find the opt blocks:
    for key, blocks in memberMap.items():
   
      result_block = find_available_time_blocks(blocks) #calling the merge block algorithm
      print(result_block)
  
       #To perform the merge for each block within the same members:
      for block in blocks:

        if block[2] in result_block: #if id is in result, check if the end time has changed or not. if changed, then update
          if result_block[block[2]][1] != block[1]:
            #get the event from api,, update the end time, then execute the update
            target_event = service.events().get(calendarId='primary', eventId=block[2]).execute()
            target_event["end"]["dateTime"] = result_block[block[2]][1]
            service.events().update(calendarId='primary', eventId=block[2], body=target_event).execute() #should be update
        else:
          #call the delete function from the api
          service.events().delete(calendarId='primary', eventId=block[2]).execute() #delete the event otherwise
       

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()

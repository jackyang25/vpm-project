#Setting up the environment:
https://developers.google.com/calendar/api/quickstart/python

##The OAuth client information is stored in credentials.json. 

##Install the google client library:
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


##The initial python code using the google calendar api is in quickstart.py
Run the code using python3 quickstart.py
It requires one to manually login into their google calendar account, and it shows the next 10 upcoming events in terminal.
The initial scope is read only, needs to modify the scope along with adding the necessary merging algorithm code to perform the merge. It was modified to take datetime.time as input, which is more stright forward in respect of google api time conversion

##The final output
The without merge version is in viewMergeEventViaAPI.py
The merging version is in mergeEventViaAPI.py, which updates the event if it is in the final output from the algorithm, otherwise delete that event.


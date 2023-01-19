import requests
import json

print("#########################################################")
print("## ADD PEOPLE IN SPECIFIC GROUPS TO SPECIFIC SESSIONS  ##")
print("##                                                     ##")
print("## This script will ask you for your API key that you  ##")
print("## will get from the integrations tab. Then it will    ##")
print("## show you all your events. Take the event id from    ##")
print("## there. Next, it will list all the groups set up     ##")
print("## in your event. Copy and paste the group id to the   ##")
print("## prompt. Then we will list all sessions and their id ##")
print("## where you copy the id to the next prompt.           ##")
print("## Lean back and watch your attendees being added to   ##")
print("## the session of your choice                          ##")
print("#########################################################")
print()
print()
print()




# Prompt for API key
api_key = input("Please enter your API key: ")
print()
print("#########################################################")
print("## This is the list of events available                ##")
print("#########################################################")
print()
# Prompt for event ID
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/vnd.eventmobi+json; version=3"
}

events_url = "https://uapi.eventmobi.com/events"
events_response = requests.get(events_url, headers=headers)
events_data = events_response.json()

for event in events_data['data']:
    event_name = event['name']
    event_id = event['id']
    print(f"Event Name: {event_name} - Event ID: {event_id}")

print()
print()
print("From the list above, please paste the event ID (usually 5 digit number) below:")
event_id = input("Please enter the event ID: ")
print()
print("#########################################################")
print("## This is the list of groups available                ##")
print("#########################################################")
print()
# Make request to list all groups
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/vnd.eventmobi+json; version=3"
}
groups_url = f"https://uapi.eventmobi.com/events/{event_id}/people/groups"
groups_response = requests.get(groups_url, headers=headers)
groups_data = groups_response.json()

# Print list of group name and external_id

for group in groups_data['data']:
    print(f"Group Name: {group['name']} - Group ID: {group['id']}")


# Prompt for group ID
print()
print()
print("From the list above, please enter the ID of the group you want to add to a session. It is usually a long weird string with dashes.")
group_id = input("Please enter the group ID: ")

print()
print("#########################################################")
print("## This is the list of sessions available              ##")
print("#########################################################")
print()

# Make request to list all sessions
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/vnd.eventmobi+json; version=3"
}
sessions_url = f"https://uapi.eventmobi.com/events/{event_id}/sessions"
sessions_response = requests.get(sessions_url, headers=headers)
sessions_data = sessions_response.json()

# Print list of session titles and ids
for session in sessions_data['data']:
    print(f"Session Title: {session['name']} - Session ID: {session['id']}")
# Prompt for session ID
print()
print()
print("From the list above, please enter the ID of the session you want the group to attend. It is usually a long weird string with dashes.")
session_id = input("Please enter the session ID: ")

# Make request to list all people in the group
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/vnd.eventmobi+json; version=3"
}
people_url = f"https://uapi.eventmobi.com/events/{event_id}/people?group_id={group_id}"
people_response = requests.get(people_url, headers=headers)
people_data = people_response.json()

# Iterate through each person and add them to the session
print()
print("#########################################################")
print("## From here, we'll do the work for you                ##")
print("#########################################################")
print()
attendee_count = 0
for person in people_data['data']:
    print(f"Adding person with ID: {person['id']} to session with ID: {session_id} for event with ID: {event_id}")
    schedule_url = f"https://uapi.eventmobi.com/events/{event_id}/people/{person['id']}/schedule"
    schedule_data = {"id": session_id}
    schedule_response = requests.post(schedule_url, headers=headers, json=schedule_data)
    if schedule_response.status_code == 201:
        attendee_count += 1


# Report the result
if attendee_count > 0:
    print()
    print()
    print("#########################################################")
    print(f"Successfully added {attendee_count} attendees to the session.")
    print("#########################################################")
    print()
    print()
    print()
    print()
else:
    print()
    print()
    print("#########################################################")
    print("Failed to add any attendees to the session. Please check the IDs or if the attendees were already added.")
    print("#########################################################")
    print()
    print()
    print()
    print()
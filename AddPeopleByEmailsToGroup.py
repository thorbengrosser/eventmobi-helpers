import requests
import json

#Welcome banner
print()
print("    _      _    _   ___            _ _      _                                   ")
print("   /_\  __| |__| | | __|_ __  __ _(_) |___ | |_ ___   __ _ _ _ ___ _  _ _ __ ___")
print("  / _ \/ _` / _` | | _|| '  \/ _` | | (_-< |  _/ _ \ / _` | '_/ _ \ || | '_ (_-<")
print(" /_/ \_\__,_\__,_| |___|_|_|_\__,_|_|_/__/  \__\___/ \__, |_| \___/\_,_| .__/__/")
print("                                                     |___/             |_|      ")
print()
print()
print()
print("This tool allows you to use the EventMobi API to add people with specific email ")
print("adresses to one group of your choice. You will need your organizations API key  ")
print("to get started. The tool will provide you the available events and their IDs,   ")
print("the available groups and their IDs and will then prompt you for a comma-separated")
print("list of email addresses.")
print("NOT AN OFFICIAL EVENTMOBI ADD-ON. DO NOT USE FOR LIVE EVENTS. ALWAYS CREATE BACKUPS")
print()
print()

# Get the API key from the user
print("First, please get the API key from your integrations tab and enter it below.")
api_key = input("Enter the API key: ")

# Use the endpoint to get a list of all events
headers = {
    "Accept": "application/vnd.eventmobi+json; version=3",
    "Authorization": f"Bearer {api_key}"
}

response = requests.get("https://uapi.eventmobi.com/events", headers=headers)
events = response.json()["data"]

# Output the events as a list with the event name and the event id
print()
print()
print("## The following events are available with your API key ##")
for event in events:
    print(f"Name: {event['name']}, ID: {event['id']}")

# Ask the user for the event ID
print()
print()
print("Please select an event ID for the event in question.")
print("This should be a five digit number.")
event_id = input("Enter the event ID: ")

# Use the endpoint to get a list of all people groups for the event
response = requests.get(f"https://uapi.eventmobi.com/events/{event_id}/people/groups", headers=headers)
groups = response.json()["data"]

# List each element within the data object with the group name and the group id
print()
print()
print("## The following groups are available within your event ##")
for group in groups:
    print(f"Name: {group['name']}, ID: {group['id']}")

# Ask the user for the group ID
print()
print()
print("Please select an group ID for the event in question. This should be a long,")
print("weird-looking string. Do not paste any spaces before or after.")
new_group_id = input("Enter the group ID to add people to: ")

# Ask the user for a comma separated list of email addresses
print()
print()
print("Great, final step. Please enter the email addresses, which you")
print("would like to add to the group below. This needs to be one line")
print("and each email address should be separated by a comma. If your")
print("e-mail addresses are in any other format, use a tool such as")
print("https://delim.co/ to properly format them. This is important.")
emails = input("Enter a comma separated list of email addresses: ").split(",")

print()
print()
print("Thanks, I'll take it from here.")
# Create an array to store people to be updated
people_to_be_updated = []
for email in emails:
    response = requests.get(f"https://uapi.eventmobi.com/events/{event_id}/people?include=groups&email={email}", headers=headers)
    if response.status_code != 200:
        print(f"No person found with email {email}")
        continue
    data = response.json()["data"]
    if len(data) == 0:
        print(f"No person found with email {email}")
        continue
    person = data[0]
    person_id = person["id"]
    current_groups = person["groups"]
    current_groups.append({"id": new_group_id})
    people_to_be_updated.append({"id": person_id, "groups": current_groups, "email": email})

#Initialize variables to track success and failure
success_count = 0
failure_count = 0
failed_emails = []

# For each object in the people_to_be_updated array, use the API patch endpoint
for person in people_to_be_updated:

    response = requests.patch(f"https://uapi.eventmobi.com/events/{event_id}/people/{person['id']}", json=person, headers=headers)
    if response.status_code == 200:
        print(f"Successfully added person with email {person['email']} to group {new_group_id}")
        success_count += 1
    else:
        response_data = response.json()
        print(f"Error adding person with email {person['email']} to group. API response message: {response_data['errors'][0]['message']}")
        failure_count += 1
        failed_emails.append(person['email'])



# Provide a final status update
print()
print()
if failure_count == 0:
    print("All people have been added to the specified group.")
else:
    print(f"Added {success_count} of {len(people_to_be_updated)} to the group. {failure_count} email addresses could not be added. Please check the errors above. The email addresses not added were: {', '.join(failed_emails)}")

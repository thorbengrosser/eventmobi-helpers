import requests
import json
import sys

# ASCII art for the script launch
print(r"""

██████╗░██╗░██████╗░█████╗░██████╗░██╗░░░░░███████╗  ░█████╗░██╗░░██╗░█████╗░████████╗
██╔══██╗██║██╔════╝██╔══██╗██╔══██╗██║░░░░░██╔════╝  ██╔══██╗██║░░██║██╔══██╗╚══██╔══╝
██║░░██║██║╚█████╗░███████║██████╦╝██║░░░░░█████╗░░  ██║░░╚═╝███████║███████║░░░██║░░░
██║░░██║██║░╚═══██╗██╔══██║██╔══██╗██║░░░░░██╔══╝░░  ██║░░██╗██╔══██║██╔══██║░░░██║░░░
██████╔╝██║██████╔╝██║░░██║██████╦╝███████╗███████╗  ╚█████╔╝██║░░██║██║░░██║░░░██║░░░
╚═════╝░╚═╝╚═════╝░╚═╝░░╚═╝╚═════╝░╚══════╝╚══════╝  ░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░

██████╗░██╗░░░██╗  ░██████╗░██████╗░░█████╗░██╗░░░██╗██████╗░
██╔══██╗╚██╗░██╔╝  ██╔════╝░██╔══██╗██╔══██╗██║░░░██║██╔══██╗
██████╦╝░╚████╔╝░  ██║░░██╗░██████╔╝██║░░██║██║░░░██║██████╔╝
██╔══██╗░░╚██╔╝░░  ██║░░╚██╗██╔══██╗██║░░██║██║░░░██║██╔═══╝░
██████╦╝░░░██║░░░  ╚██████╔╝██║░░██║╚█████╔╝╚██████╔╝██║░░░░░
╚═════╝░░░░╚═╝░░░  ░╚═════╝░╚═╝░░╚═╝░╚════╝░░╚═════╝░╚═╝░░░░░

Do not use for live events. If you don't know where you get your API key or your event id
from, maybe don't use this?        
""")

# Function to get user inputs for API key and Event ID
def get_user_input():
    api_key = input("Enter the API Key: ")
    event_id = input("Enter the Event ID: ")
    return api_key, event_id

# Function to get groups
def get_groups(api_key, event_id):
    url = f"https://uapi.eventmobi.com/events/{event_id}/people/groups"
    headers = {
        "Accept": "application/vnd.eventmobi+json; version=3",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch groups. Status code: {response.status_code}")
        sys.exit(1)

    try:
        groups_data = response.json()
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
        sys.exit(1)

    # Assuming the groups are in a list under a key, modify as per actual response structure
    return groups_data.get('data', [])


# Function to get people in a group
def get_people_in_group(api_key, event_id, group_id):
    url = f"https://uapi.eventmobi.com/events/{event_id}/people"
    querystring = {"group_id": group_id}
    headers = {
        "Accept": "application/vnd.eventmobi+json; version=3",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        print(f"Failed to fetch people in group. Status code: {response.status_code}")
        sys.exit(1)

    try:
        people_data = response.json()
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
        sys.exit(1)

    # Assuming the people are in a list under a key, modify as per actual response structure
    return people_data.get('data', [])

# Function to update chat settings for a person
def update_chat_settings(api_key, event_id, person_id, chat_enabled):
    url = f"https://uapi.eventmobi.com/events/{event_id}/people/{person_id}"
    payload = { "public_preferences": { "chat_enabled": chat_enabled } }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/vnd.eventmobi+json; version=3",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.patch(url, json=payload, headers=headers)
    return response.json()

# Main function
def main():
    api_key, event_id = get_user_input()

    # Get groups
    groups = get_groups(api_key, event_id)
    for index, group in enumerate(groups, start=1):
        print(f"{index}. {group['name']}")

    group_choice = int(input("Select a group number to disable chat: "))
    group_id = groups[group_choice - 1]['id']

    # Get people in the group
    people = get_people_in_group(api_key, event_id, group_id)
    if people:
        print("First person's data structure:", people[0])  # Print the structure of the first person object

    print(f"Disabling chat for {len(people)} people in the group '{groups[group_choice - 1]['name']}'...")

    # Update chat settings for each person
    for person in people:
        person_id = person['id']  # Assuming 'id' is the correct key for person's ID
        update_chat_settings(api_key, event_id, person_id, False)

        # Construct the full name and email string
        first_name = person.get('first_name', '')
        last_name = person.get('last_name', '')
        email = person.get('email', 'No email')
        full_name_email = f"{first_name} {last_name} ({email})"
        
        print(f"Chat disabled for {full_name_email}")

    print("Chat disabled for all members in the selected group.")


if __name__ == "__main__":
    main()

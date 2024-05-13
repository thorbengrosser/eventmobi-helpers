import sys
import uuid
from faker import Faker
import random
from datetime import datetime, timedelta
import requests
import json
import pytz
import threading
import itertools
import time

print(r"""

███╗░░░███╗░█████╗░██████╗░██╗
████╗░████║██╔══██╗██╔══██╗██║
██╔████╔██║██║░░██║██████╦╝██║
██║╚██╔╝██║██║░░██║██╔══██╗██║
██║░╚═╝░██║╚█████╔╝██████╦╝██║
╚═╝░░░░░╚═╝░╚════╝░╚═════╝░╚═╝

░██████╗░█████╗░███╗░░░███╗██████╗░██╗░░░░░███████╗
██╔════╝██╔══██╗████╗░████║██╔══██╗██║░░░░░██╔════╝
╚█████╗░███████║██╔████╔██║██████╔╝██║░░░░░█████╗░░
░╚═══██╗██╔══██║██║╚██╔╝██║██╔═══╝░██║░░░░░██╔══╝░░
██████╔╝██║░░██║██║░╚═╝░██║██║░░░░░███████╗███████╗
╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░░░░╚══════╝╚══════╝

██████╗░░█████╗░████████╗░█████╗░  ░██████╗░███████╗███╗░░██╗
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗  ██╔════╝░██╔════╝████╗░██║
██║░░██║███████║░░░██║░░░███████║  ██║░░██╗░█████╗░░██╔██╗██║
██║░░██║██╔══██║░░░██║░░░██╔══██║  ██║░░╚██╗██╔══╝░░██║╚████║
██████╔╝██║░░██║░░░██║░░░██║░░██║  ╚██████╔╝███████╗██║░╚███║
╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝  ░╚═════╝░╚══════╝╚═╝░░╚══╝

DO NOT USE THIS ON A LIVE EVENT. THIS IS NOT AN OFFICIAL EVENTMOBI ADD-ON.
      
If you were to use this regardless of the warning, this is a dummy data generator
for EventMobi events. Please keep your event id and API key ready. Next, you will
be prompted to enter the number of dummy people you'd like to create, as well as
the number of sessions and companies. Please note that approximately 10% of
attendees will be tagged as speakers, and will be attached to the sessions at 
random. All names are fictuous. The session names seem valid but are non-sensical.
      
            """)

def spinner(message="Processing...", stop_event=threading.Event()):
    while not stop_event.is_set():
        for char in '|/-\\':
            status = f"\r{message} {char}"
            sys.stdout.write(status)
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write('\r')

def start_spinner(message="Processing..."):
    stop_event = threading.Event()
    spin_thread = threading.Thread(target=spinner, args=(message, stop_event))
    spin_thread.start()
    return spin_thread, stop_event

def stop_spinner(spin_thread, stop_event):
    stop_event.set()  # Signal the thread to stop
    spin_thread.join()  # Wait for the thread to finish


def patch_person_with_session(event_id, person_id, session_id, role_id, api_key):
    url = f"https://uapi.eventmobi.com/events/{event_id}/people/{person_id}"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.eventmobi+json; version=3'
    }
    payload = {
        "scheduled_sessions": [{"id": session_id}],
        "session_roles": [{
            "id": role_id,
            "sessions": [{"id": session_id}]
        }]
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    #if response.status_code == 200:
    #    print(f"Updated person {person_id} with session {session_id}")
    #else:
    #    print(f"Failed to update person {person_id}: {response.text}")

    return response

def fetch_session_roles(event_id, api_key):
    url = f"https://uapi.eventmobi.com/events/{event_id}/sessions/roles"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/vnd.eventmobi+json; version=3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        roles = response.json()['data']
        speaker_role_id = next((role['id'] for role in roles if role['name'].lower() == 'speaker'), None)
        if speaker_role_id:
            return speaker_role_id
        else:
            print("Speaker role not found.")
            return None
    else:
        print(f"Failed to fetch session roles: {response.text}")
        return None


def post_session_to_api(event_id, session_data, api_key):
    url = f"https://uapi.eventmobi.com/events/{event_id}/sessions"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/vnd.eventmobi+json; version=3',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=session_data)
    return response

def upload_sessions(event_id, sessions, api_key, speaker_role_id):
    session_ids = []
    spinner_thread, stop_event = start_spinner("Uploading sessions...")

    for session in sessions:
        if not validate_session_data(session):
            continue  # Skip this session if validation fails

        session_payload = {
            "external_id": str(uuid.uuid4()),  # This assumes you want a new UUID for each session
            "name": session["Session Name"],
            "description": session["Description"],
            "start_datetime": session["Start Time"],
            "end_datetime": session["End Time"],
        }

        #print("Uploading session with payload:", session_payload)  # Log the payload to debug

        response = post_session_to_api(event_id, session_payload, api_key)
        if response.status_code == 201:
            session_data = response.json()
            session_ids.append(session_data['data']['id'])  # Append the session id from the response
            #print(f"Uploaded session: {session['Session Name']}")
        else:
            print(f"Failed to upload session {session['Session Name']}: {response.text}")
    stop_spinner(spinner_thread, stop_event)
    return session_ids


def validate_session_data(session):
    required_fields = ['Session Name', 'Start Time', 'End Time']  # Match the keys exactly as used in the dict
    missing_fields = [field for field in required_fields if field not in session or not session[field]]
    if missing_fields:
        print("Missing required session fields:", missing_fields)
        return False
    return True


def post_company_to_api(event_id, company_data, api_key):
    url = f"https://uapi.eventmobi.com/events/{event_id}/companies"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/vnd.eventmobi+json; version=3',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=company_data)
    return response

def upload_companies(event_id, companies, api_key):
    spinner_thread, stop_event = start_spinner("Uploading companies...")

    for company in companies:
        company_data = {
            "external_id": str(uuid.uuid4()),  # Generating a new UUID for each company
            "name": company["Company Name"],
            "about": f"<p><strong>About {company['Company Name']}</strong></p>",
            "email": fake.email(),
            "phone": company["Phone Number"]
        }
        response = post_company_to_api(event_id, company_data, api_key)
    stop_spinner(spinner_thread, stop_event)
        #if response.status_code == 201:
        #    print(f"Uploaded company: {company['Company Name']}")
        #else:
        #    print(f"Failed to upload company {company['Company Name']}: {response.text}")


def post_person_to_api(event_id, person_data, api_key):
    url = f"https://uapi.eventmobi.com/events/{event_id}/people"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/vnd.eventmobi+json; version=3',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=person_data)
    return response

def upload_people(event_id, people, api_key):
    people_info = {}
    spinner_thread, stop_event = start_spinner("Uploading people...")

    for person in people:
        person_data = {
            "external_id": person["External ID"],
            "first_name": person["First Name"],
            "last_name": person["Last Name"],
            "pronouns": person["Pronouns"],
            "email": person["Email"],
            "title": person["Title"],
            "company_name": person["Company"],
            "groups": [{"name": person["Groups"]}]
        }
        response = post_person_to_api(event_id, person_data, api_key)
        if response.status_code == 201:
            returned_data = response.json()['data']
            people_info[person["External ID"]] = returned_data['id']  # Store the returned API ID
            #print(f"Uploaded: {person['First Name']} {person['Last Name']}")
        else:
            print(f"Failed to upload {person['First Name']} {person['Last Name']}: {response.text}")
    stop_spinner(spinner_thread, stop_event)
    return people_info



def fetch_event_details(event_id, api_key):
    url = f"https://uapi.eventmobi.com/events/{event_id}"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/vnd.eventmobi+json; version=3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        event_details = response.json()
        if event_details['errors']:
            print("Error in API response:", event_details['errors'])
            return None
        else:
            return event_details['data']
    except requests.RequestException as e:
        print(f"Failed to fetch event details: {e}")
        return None
    
def get_user_input():
    print("First, please provide your event details:")
    print()
    event_id = input("Enter the Event ID: ")
    api_key = input("Enter the EventMobi Organization API Key: ")
    #event_topic = input("Enter a rough topic for the event: ")
    print()
    print()
    print("Thanks. Next enter a number to define how many items of each category you'd like to create. Please note we suggest staying under 100 - more items will slow down the process:")
    print()
    num_participants = int(input("Enter the required number of participants: "))
    num_sessions = int(input("Enter the required number of sessions: "))
    num_companies = int(input("Enter the required number of companies: "))

    return event_id, api_key, num_participants, num_sessions, num_companies

fake = Faker()

def generate_people(num_participants):
    people = []
    num_speakers = int(num_participants * 0.1)
    num_attendees = num_participants - num_speakers

    for _ in range(num_speakers):
        people.append({
            "First Name": fake.first_name(),
            "Last Name": fake.last_name(),
            "Email": fake.email(),
            "Pronouns": random.choice(["He/Him", "She/Her", "They/Them"]),
            "Groups": "Speakers",
            "Company": fake.company(),
            "Title": fake.job(),
            "External ID": str(uuid.uuid4())
        })

    for _ in range(num_attendees):
        people.append({
            "First Name": fake.first_name(),
            "Last Name": fake.last_name(),
            "Email": fake.email(),
            "Pronouns": random.choice(["He/Him", "She/Her", "They/Them"]),
            "Groups": "Attendees",
            "Company": fake.company(),
            "Title": fake.job(),
            "External ID": str(uuid.uuid4())
        })

    return people

def generate_companies(num_companies):
    companies = []
    for _ in range(num_companies):
        companies.append({
            "Company Name": fake.company(),
            "About": fake.catch_phrase(),
            "Phone Number": fake.phone_number()
        })
    return companies

def generate_sessions(num_sessions, event_start_date, event_end_date, speakers):
    sessions = []
    start_date = datetime.strptime(event_start_date, "%Y-%m-%d")
    end_date = datetime.strptime(event_end_date, "%Y-%m-%d")
    current_start = start_date

    # Generate session times
    while len(sessions) < num_sessions and current_start + timedelta(hours=1) <= end_date:
        session_duration = random.choice([30, 60])  # minutes
        session_end = current_start + timedelta(minutes=session_duration)
        
        session = {
            "Session Name": f"{Faker().bs().title()} Session",
            "Description": Faker().text(max_nb_chars=200),
            "Start Time": current_start.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "End Time": session_end.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "Speaker": random.choice([sp["External ID"] for sp in speakers]) if speakers else None
        }
        sessions.append(session)
        current_start = session_end + timedelta(minutes=10)  # Adding a break time of 10 minutes

    return sessions



def main():
    event_id, api_key, num_participants, num_sessions, num_companies = get_user_input()
    event_details = fetch_event_details(event_id, api_key)
    print(f"Event '{event_details.get('name', 'N/A')}' details fetched successfully.")

    speaker_role_id = fetch_session_roles(event_id, api_key)
    if not speaker_role_id:
        print("Could not retrieve speaker role ID, sessions will not be uploaded.")
        return

    if num_participants > 0:
        people = generate_people(num_participants)
        people_info = upload_people(event_id, people, api_key)
        print(f"Uploaded {len(people)} participants.")

    if num_companies > 0:
        companies = generate_companies(num_companies)
        upload_companies(event_id, companies, api_key)
        print(f"Uploaded {len(companies)} companies.")

    if num_sessions > 0:
        speakers = [p for p in people if p['Groups'] == 'Speakers']
        sessions = generate_sessions(num_sessions, event_details['start_date'], event_details['end_date'], speakers)
        session_ids = upload_sessions(event_id, sessions, api_key, speaker_role_id)
        print(f"Uploaded {len(sessions)} sessions.")
        for session_id, speaker in zip(session_ids, speakers):
            speaker_api_id = people_info.get(speaker['External ID'])
            if speaker_api_id:
                patch_person_with_session(event_id, speaker_api_id, session_id, speaker_role_id, api_key)

if __name__ == "__main__":
    main()

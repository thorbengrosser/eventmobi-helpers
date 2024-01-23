import requests
import json
import sys
import concurrent.futures

# ASCII art for the script launch
print("""
      
██████╗░███████╗██╗░░░░░███████╗████████╗███████╗  ░██████╗███████╗░██████╗░██████╗██╗░█████╗░███╗░░██╗░██████╗
██╔══██╗██╔════╝██║░░░░░██╔════╝╚══██╔══╝██╔════╝  ██╔════╝██╔════╝██╔════╝██╔════╝██║██╔══██╗████╗░██║██╔════╝
██║░░██║█████╗░░██║░░░░░█████╗░░░░░██║░░░█████╗░░  ╚█████╗░█████╗░░╚█████╗░╚█████╗░██║██║░░██║██╔██╗██║╚█████╗░
██║░░██║██╔══╝░░██║░░░░░██╔══╝░░░░░██║░░░██╔══╝░░  ░╚═══██╗██╔══╝░░░╚═══██╗░╚═══██╗██║██║░░██║██║╚████║░╚═══██╗
██████╔╝███████╗███████╗███████╗░░░██║░░░███████╗  ██████╔╝███████╗██████╔╝██████╔╝██║╚█████╔╝██║░╚███║██████╔╝
╚═════╝░╚══════╝╚══════╝╚══════╝░░░╚═╝░░░╚══════╝  ╚═════╝░╚══════╝╚═════╝░╚═════╝░╚═╝░╚════╝░╚═╝░░╚══╝╚═════╝░

░██╗░░░░░░░██╗██╗████████╗██╗░░██╗  ████████╗██████╗░░█████╗░░█████╗░██╗░░██╗
░██║░░██╗░░██║██║╚══██╔══╝██║░░██║  ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║░██╔╝
░╚██╗████╗██╔╝██║░░░██║░░░███████║  ░░░██║░░░██████╔╝███████║██║░░╚═╝█████═╝░
░░████╔═████║░██║░░░██║░░░██╔══██║  ░░░██║░░░██╔══██╗██╔══██║██║░░██╗██╔═██╗░
░░╚██╔╝░╚██╔╝░██║░░░██║░░░██║░░██║  ░░░██║░░░██║░░██║██║░░██║╚█████╔╝██║░╚██╗
░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝  ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
      
NOT AN OFFICIAL EVENTMOBI ADD-ON. DO NOT USE IN PRODUCTION.

""")

# Function to get user inputs for API key and Event ID
def get_user_input():
    api_key = input("Enter the API Key: ")
    event_id = input("Enter the Event ID: ")
    return api_key, event_id

# Function to get sessions with tracks
def get_sessions_with_tracks(api_key, event_id):
    url = f"https://uapi.eventmobi.com/events/{event_id}/sessions"
    querystring = {"include": "tracks"}
    headers = {
        "Accept": "application/vnd.eventmobi+json; version=3",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        print(f"Failed to fetch sessions. Status code: {response.status_code}")
        sys.exit(1)

    try:
        sessions_data = response.json()
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
        sys.exit(1)

    return sessions_data.get('data', [])

# Function to delete a session
def delete_session(api_key, event_id, session_id):
    url = f"https://uapi.eventmobi.com/events/{event_id}/sessions/{session_id}"
    headers = {
        "Accept": "application/vnd.eventmobi+json; version=3",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.delete(url, headers=headers)
    return session_id, response.status_code

# Main function
def main():
    api_key, event_id = get_user_input()

    # Get sessions with tracks
    sessions = get_sessions_with_tracks(api_key, event_id)

    # Extract tracks and allow user to choose one
    tracks = {}
    for session in sessions:
        for track in session.get('tracks', []):
            tracks[track['id']] = track['name']

    for track_id, track_name in tracks.items():
        print(f"Track ID: {track_id}, Track Name: {track_name}")

    track_id_to_delete = input("Enter the Track ID for which you want to delete sessions: ")

    # Filter the sessions to delete based on the selected track
    sessions_to_delete = [session for session in sessions if any(track['id'] == track_id_to_delete for track in session.get('tracks', []))]

    print(f"Deleting {len(sessions_to_delete)} sessions associated with track ID {track_id_to_delete}...")

    # Deleting sessions in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(delete_session, api_key, event_id, session['id']) for session in sessions_to_delete]
        for future in concurrent.futures.as_completed(futures):
            session_id, status_code = future.result()
            if status_code == 204:
                print(f"Session {session_id} deleted successfully.")
            else:
                print(f"Failed to delete session {session_id}. Status code: {status_code}")

    print("Deletion process completed.")

if __name__ == "__main__":
    main()

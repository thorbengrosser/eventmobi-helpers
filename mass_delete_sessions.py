import csv
import asyncio
import aiohttp
import argparse

async def get_session_uuid(session, event_id, session_external_id, auth_token):
    url = f"https://uapi.eventmobi.com/events/{event_id}/sessions"
    headers = {
        "Accept": "application/vnd.eventmobi+json; version=3",
        "Authorization": f"Bearer {auth_token}"
    }
    params = {
        "external_id": session_external_id
    }
    async with session.get(url, headers=headers, params=params) as response:
        data = await response.json()
        if response.status == 200 and data.get("data"):
            return data["data"][0]["id"]
        else:
            return None

async def delete_session(session, event_id, uuid, auth_token):
    url = f"https://uapi.eventmobi.com/events/{event_id}/sessions/{uuid}"
    headers = {
        "Accept": "application/vnd.eventmobi+json; version=3",
        "Authorization": f"Bearer {auth_token}"
    }
    async with session.delete(url, headers=headers) as response:
        return await response.json()

async def handle_session(session, event_id, session_external_id, auth_token):
    uuid = await get_session_uuid(session, event_id, session_external_id, auth_token)
    if uuid:
        response = await delete_session(session, event_id, uuid, auth_token)
        print(f"Deleting session {session_external_id} (UUID: {uuid}): {response}")
    else:
        print(f"Failed to retrieve UUID for session {session_external_id}")

async def main(args):
    event_id = args.event_id
    auth_token = args.api_key
    csv_file_path = args.csv_file

    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        session_external_ids = [row[0] for row in reader]

    async with aiohttp.ClientSession() as session:
        tasks = []
        for session_external_id in session_external_ids:
            tasks.append(handle_session(session, event_id, session_external_id, auth_token))
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":

    # Print cool ASCII graphic
    print("""
 


█▄░█ █▀█ ▀█▀   ▄▀█ █▄░█   █▀█ █▀▀ █▀▀ █ █▀▀ █ ▄▀█ █░░   █▀▀ █░█ █▀▀ █▄░█ ▀█▀ █▀▄▀█ █▀█ █▄▄ █
█░▀█ █▄█ ░█░   █▀█ █░▀█   █▄█ █▀░ █▀░ █ █▄▄ █ █▀█ █▄▄   ██▄ ▀▄▀ ██▄ █░▀█ ░█░ █░▀░█ █▄█ █▄█ █
          
░██████╗███████╗░██████╗░██████╗██╗░█████╗░███╗░░██╗  ███╗░░░███╗░█████╗░░██████╗░██████╗
██╔════╝██╔════╝██╔════╝██╔════╝██║██╔══██╗████╗░██║  ████╗░████║██╔══██╗██╔════╝██╔════╝
╚█████╗░█████╗░░╚█████╗░╚█████╗░██║██║░░██║██╔██╗██║  ██╔████╔██║███████║╚█████╗░╚█████╗░
░╚═══██╗██╔══╝░░░╚═══██╗░╚═══██╗██║██║░░██║██║╚████║  ██║╚██╔╝██║██╔══██║░╚═══██╗░╚═══██╗
██████╔╝███████╗██████╔╝██████╔╝██║╚█████╔╝██║░╚███║  ██║░╚═╝░██║██║░░██║██████╔╝██████╔╝
╚═════╝░╚══════╝╚═════╝░╚═════╝░╚═╝░╚════╝░╚═╝░░╚══╝  ╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═════╝░╚═════╝░

██████╗░███████╗██╗░░░░░███████╗████████╗██╗░█████╗░███╗░░██╗
██╔══██╗██╔════╝██║░░░░░██╔════╝╚══██╔══╝██║██╔══██╗████╗░██║
██║░░██║█████╗░░██║░░░░░█████╗░░░░░██║░░░██║██║░░██║██╔██╗██║
██║░░██║██╔══╝░░██║░░░░░██╔══╝░░░░░██║░░░██║██║░░██║██║╚████║
██████╔╝███████╗███████╗███████╗░░░██║░░░██║╚█████╔╝██║░╚███║
╚═════╝░╚══════╝╚══════╝╚══════╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝         
          
This tool allows you to use the EventMobi API to mass-delete sessions from your event
space. All you need is a CSV file which, in the first column, holds all the external
IDs, your event ID and your API key. This tool will then blitz through the sessions.
Please understand that this action cannot be undone. Deleted sessions are gone.
          
THIS IS NOT AN OFFICIAL EVENTMOBI ADD-ON. DO NOT USE FOR LIVE EVENTS. ALWAYS CREATE BACKUPS.
      

    """)

    parser = argparse.ArgumentParser(description="Delete sessions using API calls based on CSV entries.")
    parser.add_argument("--api-key", help="API key for authentication", type=str)
    parser.add_argument("--csv-file", help="Path to the CSV file containing session external IDs", type=str)
    parser.add_argument("--event-id", help="Event ID", type=str)
    
    args = parser.parse_args()

    # If no arguments provided, prompt the user interactively
    if not args.api_key:
        args.api_key = input("Please enter the API key: ")
    if not args.csv_file:
        args.csv_file = input("Please enter the path to the CSV file: ")
    if not args.event_id:
        args.event_id = input("Please enter the event ID: ")

    asyncio.run(main(args))

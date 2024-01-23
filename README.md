# eventmobi-helpers
This is a collection of different scripts that can help you getting more use from the EventMobi platform. Do not use any of those scripts on live events. Using these scripts is not endorsed by EventMobi. This repository does not contain any official EventMobi code and features. This is meant as a playground for EventMobi power users.

Again, this is not an official EventMobi resource and, unless you know what you are doing, this may break your EventMobi setup.

## DeleteSessionsWithGroup.py
Deletes Sessions from EventMobi events that are part of a specific group.

## DoubleSideMyBadge.py
Makes single-sided badges into butterfly badges. Please check the directory for the readme file

## TurnChatOffForGroups.py
Turns attendee chat off for people in specific groups. Please check the directory for the readme file

## mass_delete_sessions.py

This Python script allows users to batch delete sessions from an event system using their API. The script takes session IDs from a CSV file, retrieves the associated UUID for each session via the API, and then sends a DELETE request to remove the session. It employs asynchronous programming techniques to enhance speed, especially when processing a large number of sessions.

### Usage:

1. **Installation**:
   - Ensure Python is installed on your machine.
   - Install required libraries using pip:
     ```bash
     pip install aiohttp
     ```

2. **Parameters**:
   - The script can take command-line arguments or prompt the user for input if arguments are not provided.
     - `--api-key`: Your API key for authentication.
     - `--csv-file`: Path to the CSV file containing the session external IDs.
     - `--event-id`: The event ID.

3. **Command-line Execution**:
   Run the script with command-line arguments:
   ```bash
   python script_name.py --api-key YOUR_API_KEY --csv-file path_to_csv_file.csv --event-id EVENT_ID
   ```
   If you run the script without any arguments, it will prompt you to enter the required details interactively.

4. **Interactive Mode**:
   Simply run the script:
   ```bash
   python script_name.py
   ```
   And then follow the on-screen prompts to provide the API key, CSV file path, and event ID.

---

Replace `script_name.py` with the actual name you've given to the script. This should give a clear overview and usage instructions for anyone visiting your GitHub page.

## AddGroupsToSession.py
This is a Python script which uses the EventMobi API to add people, who are part of specific groups, to a selected session manually. In order to run the script, simply download it and execute it with 
__python3 AddGroupsToSession.py__ 
and follow the instructions. This code was almost entirely written by ChatGPT and has not gone through any code reviews. Use at your own risk.

Uses the json and requests library.

## AddPeopleByEmailsToGroup.py
This is a Python script which uses the EventMobi API to add people to specific groups by simply providing it with the email addresses of those people. The script will ask for your API key, and then guide you step by step. It will then ask you for a *comma-separated* list of emails, will search for those emails and, if they exist, add them to the group. If an email address is not findable in your people list, it will report those back to you. In order to run the script, simply download it and execute it with 
__python3 AddPeopleByEmailsToGroup.py__ 
and follow the instructions. This code was almost entirely written by ChatGPT and has not gone through any code reviews. Use at your own risk.

## checkin.html
A HTML file with JavaScript that runs locally. You can use it to calculate how long attendees, who checked in and out of your event, were on-site. This is deprecated, if you need these reports, refer to your EventMobi support team.

# System requirements
Any HTML file will run in modern browsers. Simply download and double click.

The Python scripts need to be run locally on your machine. You need to have Python 3 installed, alongside the libraries "json" and "requests".

- How to install Python on Windows 10: https://www.digitalocean.com/community/tutorials/install-python-windows-10
- How to install Python on MacOS: https://docs.python-guide.org/starting/install3/osx/
- How to install Python on Linux: https://docs.python-guide.org/starting/install3/linux/

Once you have Python up and running,  make sure the request module is properly installed.
- On Windows: python -m pip install requests
- On Linux: pip install requests
- On Mac: python3 pip install requests

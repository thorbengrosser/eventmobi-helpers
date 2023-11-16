# README: Chat Disabling Script for EventMobi API

## Overview
This script is designed to disable the chat feature for users belonging to a specific group in an EventMobi event. It interacts with the EventMobi API to fetch groups, list members of a selected group, and update their chat settings.

## Features
- Displays ASCII art on launch.
- Prompts for API key and Event ID input.
- Lists all groups and allows selection of a target group.
- Retrieves all members of the selected group.
- Disables the chat feature for each member of the group.
- Displays progress and confirmation for each operation.

## Prerequisites
- Python 3.x
- `requests` library (Install using `pip install requests`)

## Usage
1. **Launch the Script**: Run the script using Python.
2. **Enter API Key and Event ID**: When prompted, input the valid API key and Event ID.
3. **Select a Group**: Choose a group from the listed options to disable chat for its members.
4. **Execution**: The script will process each member of the chosen group and disable their chat feature, displaying progress along the way.

## Important Notes
- Ensure the correct API version is used in the headers.
- The script requires a stable internet connection to interact with the EventMobi API.
- Handle sensitive data (like API keys) with care.

## Troubleshooting
- If you encounter errors, check the API key, Event ID, and your internet connection.
- For a 400 HTTP status error, verify the API version and the structure of your request.
- Ensure the script is run in an environment where Python and the required packages are installed.

